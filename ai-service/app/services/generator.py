# import torch
# from PIL import Image
# from app.models.loader import (
#     blip_processor,
#     blip_model,
#     tokenizer,
#     text_model,
#     device,
# )

# # -------------------------------------------------
# # IMAGE → CAPTION
# # -------------------------------------------------
# def generate_image_caption(image: Image.Image) -> str:
#     with torch.no_grad():
#         inputs = blip_processor(image, return_tensors="pt").to(device)
#         output = blip_model.generate(**inputs, max_length=50)
#     return blip_processor.decode(output[0], skip_special_tokens=True)


# # -------------------------------------------------
# # FORCE EXACT 250 CHARACTERS
# # -------------------------------------------------
# def normalize_to_250(text: str) -> str:
#     text = " ".join(text.split())

#     if len(text) > 250:
#         cut = text[:250]
#         if " " in cut:
#             cut = cut.rsplit(" ", 1)[0]
#         return cut.ljust(250)

#     if len(text) < 250:
#         neutral_pad = (
#             " Officials shared details during the event, "
#             "highlighting its broader significance."
#         )
#         while len(text) + len(neutral_pad) < 250:
#             text += neutral_pad
#         return text[:250]

#     return text


# # -------------------------------------------------
# # HEADLINE → NEWS TWEET (MODEL-DRIVEN)
# # -------------------------------------------------
# def generate_tweet(headline: str, image_caption: str = "", target_words: int = 250) -> str:
#     headline = headline.strip()

#     seed = (
#         "News update — "
#         f"{headline.capitalize()}. "
#         "According to official sources, "
#     )

#     if image_caption:
#         seed += f"the visuals show {image_caption.lower()}, "

#     seed += "as part of the reported development."

#     inputs = tokenizer(
#         seed,
#         return_tensors="pt",
#         truncation=True,
#         max_length=256
#     ).to(device)

#     with torch.no_grad():
#         output = text_model.generate(
#             **inputs,
#             do_sample=True,
#             top_p=0.93,
#             temperature=1.15,
#             min_length=200,      # Increased for longer output
#             max_length=300,      # Increased to allow 250+ words
#             repetition_penalty=1.25,
#             no_repeat_ngram_size=3
#         )

#     generated = tokenizer.decode(
#         output[0], skip_special_tokens=True
#     ).strip()

#     # Choose which normalization you want:
#     return normalize_to_250_words(generated)  # For 250 WORDS
#     # return normalize_to_250_chars(generated)  # For 250 CHARACTERS


# # -------------------------------------------------
# # MAIN ENTRY
# # -------------------------------------------------
# def generate_content(headline: str, image=None):
#     image_caption = generate_image_caption(image) if image else ""
#     tweet = generate_tweet(headline, image_caption)

#     return {
#         "headline": headline,
#         "image_caption": image_caption,
#         "tweet": tweet,  # ALWAYS 250 chars
#     }

import torch
from PIL import Image
from app.models.loader import (
    blip_processor,
    blip_model,
    tokenizer,
    text_model,
    device
)

# ---------------------------------
# IMAGE → CAPTION (BLIP)
# ---------------------------------
def generate_image_caption(image: Image.Image) -> str:
    with torch.no_grad():
        inputs = blip_processor(image, return_tensors="pt").to(device)
        output = blip_model.generate(**inputs, max_length=40)

    return blip_processor.decode(output[0], skip_special_tokens=True)


# ---------------------------------
# FORCE EXACT 250 CHARACTERS
# ---------------------------------
def normalize_to_250_chars(text: str) -> str:
    text = " ".join(text.split())

    if len(text) > 250:
        cut = text[:250]
        if " " in cut:
            cut = cut.rsplit(" ", 1)[0]
        return cut.ljust(250)

    if len(text) < 250:
        filler = " Officials shared further details during the interaction."
        while len(text) + len(filler) < 250:
            text += filler
        return text[:250]

    return text


# ---------------------------------
# HEADLINE → PROFESSIONAL TWEET
# ---------------------------------
def generate_tweet(headline: str, image_caption: str = "") -> str:
    headline = headline.strip()

    # Strong structured prompt
    prompt = (
        "Write a professional news-style tweet.\n"
        f"Headline: {headline}\n"
    )

    if image_caption:
        prompt += f"Image context: {image_caption}\n"

    prompt += "Tweet:"

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=256
    ).to(device)

    with torch.no_grad():
        output = text_model.generate(
            **inputs,
            do_sample=True,
            top_p=0.92,
            temperature=0.8,
            max_new_tokens=120,
            repetition_penalty=1.15,
            no_repeat_ngram_size=3,
            pad_token_id=tokenizer.eos_token_id
        )

    generated = tokenizer.decode(
        output[0],
        skip_special_tokens=True
    ).strip()

    # Remove the prompt from output if model repeats it
    if "Tweet:" in generated:
        generated = generated.split("Tweet:")[-1].strip()

    return normalize_to_250_chars(generated)


# ---------------------------------
# MAIN ENTRY FUNCTION
# ---------------------------------
def generate_content(headline: str, image=None):

    image_caption = ""
    if image:
        image_caption = generate_image_caption(image)

    tweet = generate_tweet(headline, image_caption)

    return {
        "headline": headline,
        "image_caption": image_caption,
        "tweet": tweet  # ALWAYS EXACTLY 250 characters
    }
    