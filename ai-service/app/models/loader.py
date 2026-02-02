# import torch
# from transformers import (
#     BlipProcessor,
#     BlipForConditionalGeneration,
#     AutoTokenizer,
#     AutoModelForSeq2SeqLM,
# )

# device = "cuda" if torch.cuda.is_available() else "cpu"

# print("🔹 Loading AI models...")

# # BLIP – Image → Caption
# blip_processor = BlipProcessor.from_pretrained(
#     "Salesforce/blip-image-captioning-base"
# )
# blip_model = BlipForConditionalGeneration.from_pretrained(
#     "Salesforce/blip-image-captioning-base"
# ).to(device)

# # T5 – Headline → Tweet
# tokenizer = AutoTokenizer.from_pretrained("t5-base")
# text_model = AutoModelForSeq2SeqLM.from_pretrained(
#     "t5-base"
# ).to(device)

# print("✅ Models loaded successfully")

import torch
from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration,
    AutoTokenizer,
    AutoModelForCausalLM
)

device = "cuda" if torch.cuda.is_available() else "cpu"

print("🔹 Loading AI models...")

# -------------------------------
# BLIP – Image Captioning Model
# -------------------------------
blip_processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)
blip_model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
).to(device)

# -------------------------------
# TEXT GENERATION MODEL (GPT-2)
# -------------------------------
tokenizer = AutoTokenizer.from_pretrained("gpt2")
text_model = AutoModelForCausalLM.from_pretrained("gpt2").to(device)

# GPT2 padding fix
tokenizer.pad_token = tokenizer.eos_token

print("✅ Models loaded successfully")
