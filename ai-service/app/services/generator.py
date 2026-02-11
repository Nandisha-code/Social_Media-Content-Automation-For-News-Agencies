import torch
import re
from PIL import Image


# ---------------------------------
# IMAGE → CAPTION (BLIP)
# ---------------------------------
def generate_image_caption(image: Image.Image) -> str:
    from app.models.loader import blip_processor, blip_model, device

    with torch.no_grad():
        inputs = blip_processor(image, return_tensors="pt").to(device)
        output = blip_model.generate(**inputs, max_length=50)

    caption = blip_processor.decode(output[0], skip_special_tokens=True)
    return caption.strip()


# ---------------------------------
# TEXT NORMALIZATION
# ---------------------------------
def normalize_headline(headline: str) -> str:
    """Clean and normalize raw headline text"""
    headline = headline.lower()
    headline = re.sub(r"\s+", " ", headline)
    headline = headline.strip()
    return headline


# ---------------------------------
# CONTROLLED EXPANSION
# ---------------------------------
def controlled_expansion(headline: str) -> str:
    """
    Safely expand short headlines to near 300 characters
    without adding any new facts.
    """

    base = headline.capitalize()

    safe_fillers = (
        " This issue has attracted considerable public attention and continues to be "
        "a subject of ongoing discussion among sports followers and analysts. The matter "
        "has generated widespread reactions and remains an important talking point within "
        "relevant circles, keeping the focus firmly on the concerns being raised."
    )

    result = base + "." + safe_fillers

    return result[:295]


# ---------------------------------
# HEADLINE → 300 CHAR TWEET
# ---------------------------------
def generate_tweet(headline: str) -> str:
    """
    Generate professional tweet close to 300 characters
    while avoiding hallucination.
    """

    from app.models.loader import tokenizer, text_model, device

    headline = normalize_headline(headline)

    prompt = f"""
Create a professional news tweet of around 280 to 300 characters.

Rules:
- Use ONLY the information present in the headline
- Do NOT add any new facts, names, sources, times, or opinions
- Expand the sentence professionally to reach near 300 characters
- Use formal journalistic language
- Correct grammar and spelling
- Do not exceed 300 characters

Headline: {headline}

Tweet:
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=300
    ).to(device)

    with torch.no_grad():
        output = text_model.generate(
            **inputs,
            max_new_tokens=120,
            num_beams=8,
            do_sample=False,
            repetition_penalty=1.8,
            no_repeat_ngram_size=3,
            early_stopping=True
        )

    generated = tokenizer.decode(output[0], skip_special_tokens=True).strip()

    # ---------------------------------
    # HALLUCINATION SAFETY FILTER
    # ---------------------------------
    banned_terms = [
        "reported", "according to", "sources", "said",
        "ESPN", "BBC", "CNN", "GMT", "ET",
        "officials", "experts", "confirmed"
    ]

    for term in banned_terms:
        if term.lower() in generated.lower():
            return controlled_expansion(headline)

    generated = " ".join(generated.split()).strip()

    # If too short, use safe expansion
    if len(generated) < 220:
        generated = controlled_expansion(headline)

    # Enforce 300 char limit
    if len(generated) > 300:
        generated = generated[:300].rsplit(" ", 1)[0]

    if not generated.endswith((".", "!", "?")):
        generated += "."

    return generated


# ---------------------------------
# HASHTAG EXTRACTION
# ---------------------------------
def extract_hashtags(headline: str) -> str:
    """Extract relevant hashtags from headline"""

    headline_lower = headline.lower()

    hashtag_map = {
        # Sports
        "icc": "#ICC",
        "cricket": "#Cricket",
        "bcci": "#BCCI",
        "match": "#Cricket",
        "tournament": "#Tournament",
        "bowling": "#Cricket",

        # Military/Defense
        "rafale": "#Rafale",
        "fighter jet": "#FighterJet",
        "air force": "#AirForce",

        # Politics
        "prime minister": "#PM",
        "president": "#President",
        "minister": "#Minister",
        "india": "#India",

        # General
        "election": "#Election",
        "protest": "#Protest",
        "deal": "#Deal",
    }

    hashtags = []

    for keyword, tag in hashtag_map.items():
        if keyword in headline_lower:
            hashtags.append(tag)

    hashtags = list(dict.fromkeys(hashtags))

    return " ".join(hashtags[:3]) if hashtags else "#News"


# ---------------------------------
# MAIN ENTRY FUNCTION
# ---------------------------------
def generate_content(headline: str, image=None, image_caption: str = None):
    """
    Generate optimized content for news automation
    with tweet target close to 300 characters
    """

    generated_caption = ""

    if image:
        generated_caption = generate_image_caption(image)

    if image_caption:
        generated_caption = image_caption.strip()

    # Generate near-300 char tweet
    tweet = generate_tweet(headline)

    # Generate hashtags
    hashtags = extract_hashtags(headline)

    final_tweet = tweet

    # Attach hashtags only if within 300 limit
    if hashtags:
        if len(tweet) + len(hashtags) + 1 <= 300:
            final_tweet = f"{tweet} {hashtags}"

    return {
        "headline": headline,
        "image_caption": generated_caption,
        "tweet": final_tweet,
        "tweet_length": len(final_tweet)
    }
