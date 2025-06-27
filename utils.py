import pdfplumber
from PIL import Image
import os
import base64
import tempfile
from typing import List, Dict
from langsmith import traceable

@traceable(name="Extract PDF Elements")
def extract_elements(pdf_file: str) -> Dict:
    text_elements, table_elements, images = [], [], []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text_elements.append(page.extract_text())
            table_elements.extend(page.extract_tables())

            for img in page.images:
                cropped = page.crop((img["x0"], img["top"], img["x1"], img["bottom"]))
                pil_img = cropped.to_image(resolution=300).original
                images.append(pil_img)

    return {
        "texts": text_elements,
        "tables": table_elements,
        "images": images
    }

@traceable(name="Encode Image to Base64")
def encode_image(image: Image.Image) -> str:
    """Convert PIL image to Base64."""
    import io
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")
