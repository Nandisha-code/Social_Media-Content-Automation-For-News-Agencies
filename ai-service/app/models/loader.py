import torch
from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration,
    BartTokenizer,
    BartForConditionalGeneration,
    BitsAndBytesConfig
)

device = "cuda" if torch.cuda.is_available() else "cpu"

print("🔹 Loading AI models on device:", device)

# -------------------------------
# BLIP – Image Captioning Model
# Better parameters for accurate captions
# -------------------------------
blip_processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

blip_model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
).to(device)

# Set to eval mode for consistent inference
blip_model.eval()


# -------------------------------
# BART – News Summarization & Paraphrasing
# Better suited for news content than FLAN-T5
# -------------------------------
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

text_model = BartForConditionalGeneration.from_pretrained(
    "facebook/bart-large-cnn"
).to(device)

# Set to eval mode
text_model.eval()

print("✅ Models loaded successfully")
print(f"   - BLIP Processor: {type(blip_processor).__name__}")
print(f"   - BLIP Model: {type(blip_model).__name__}")
print(f"   - BART Tokenizer: {type(tokenizer).__name__}")
print(f"   - BART Model: {type(text_model).__name__}")
print(f"   - Device: {device}")