from fastapi import APIRouter, UploadFile, File, Form
from PIL import Image
from app.services.generator import generate_content

router = APIRouter()


@router.post("/generate")
async def generate(
    headline: str = Form(...),
    image: UploadFile | None = File(None)
):
    img = None

    if image:
        img = Image.open(image.file).convert("RGB")

    result = generate_content(
        headline=headline,
        image=img
    )

    return result
