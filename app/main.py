# app/main.py
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List
from app.processor import DocumentProcessor
from app.chunker import TextChunker
from app.embedding import EmbeddingEngine
from app.qa_model import QAModel

app = FastAPI()
processor = DocumentProcessor()
chunker = TextChunker()
embedder = EmbeddingEngine()
qa_model = QAModel()

class QueryRequest(BaseModel):
    file_url: str
    query: str

@app.post("/query")
def query_handler(payload: QueryRequest):
    # Step 1: Extract text from document
    text = processor.process(payload.file_url)
    if not text:
        return {"error": "Failed to extract text from file"}

    # Step 2: Chunk text
    chunks = chunker.chunk_text(text, metadata={"source": payload.file_url})
    docs = [{"text": chunk.content, "metadata": chunk.metadata} for chunk in chunks]

    # Step 3: Embed chunks
    embedder.index_documents(docs)

    # Step 4: Retrieve top-k relevant chunks
    top_chunks = embedder.search(payload.query, top_k=3)
    combined_context = " ".join([doc["text"] for doc in top_chunks])

    # Step 5: Generate answer
    answer = qa_model.answer(payload.query, combined_context)
    return {
        "answer": answer,
        "context": combined_context,
        "sources": [doc["metadata"]["source"] for doc in top_chunks]
    }
