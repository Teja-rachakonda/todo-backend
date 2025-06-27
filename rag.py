import chromadb
from chromadb.config import Settings
import uuid
from typing import List
from embeddings import embed
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
import os
from groq import Groq
from dotenv import load_dotenv
from langsmith import traceable  # ✅ LangSmith SDK

load_dotenv()

# Init GROQ + Chroma
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
vector_db = chromadb.Client()
collection = vector_db.get_or_create_collection("multimodal_docs")

# Image captioning setup (BLIP)
device = "cuda" if torch.cuda.is_available() else "cpu"
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

@traceable(name="Caption Image")
def caption_image(image: Image.Image) -> str:
    """Get caption for PIL image."""
    inputs = blip_processor(image, return_tensors="pt").to(device)
    caption = blip_model.generate(**inputs, max_new_tokens=100)
    return blip_processor.decode(caption[0], skip_special_tokens=True)

@traceable(name="Add Documents to ChromaDB")
def add_docs(texts: List[str], tables: List, images: List[Image.Image]):
    """Add text, table and images to the database."""
    ids, embeddings, documents = [], [], []

    # Text
    for text in texts:
        ids.append(str(uuid.uuid4()))
        embeddings.append(embed(text))
        documents.append(text)

    # Tables
    for table in tables:
        table_as_text = str(table)
        ids.append(str(uuid.uuid4()))
        embeddings.append(embed(table_as_text))
        documents.append(table_as_text)

    # Images
    for img in images:
        caption = caption_image(img)
        ids.append(str(uuid.uuid4()))
        embeddings.append(embed(caption))
        documents.append(caption)

    collection.add(ids=ids, embeddings=embeddings, documents=documents)

@traceable(name="RAG Query with GROQ")
def rag_query(query: str) -> str:
    """Perform RAG Retrieval and get answer from GROQ LLaMA3."""
    results = collection.query(query_embeddings=[embed(query)], n_results=5)
    context = "\n".join(results["documents"][0])

    prompt = f"Context:\n{context}\n\nQuery: {query}\nAnswer as precisely as possible."
    response = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192"
    )
    return response.choices[0].message.content
