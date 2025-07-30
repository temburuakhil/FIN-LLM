# app/embedding.py
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class EmbeddingEngine:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = faiss.IndexFlatL2(384)  # 384 = vector size of MiniLM
        self.doc_store = []

    def index_documents(self, documents):
        texts = [doc["text"] for doc in documents]
        vectors = self.model.encode(texts, show_progress_bar=False)
        self.index.add(np.array(vectors).astype("float32"))
        for doc in documents:
            self.doc_store.append(doc)

    def search(self, query: str, top_k: int = 3):
        query_vector = self.model.encode([query]).astype("float32")
        distances, indices = self.index.search(query_vector, top_k)
        results = []
        for idx in indices[0]:
            if idx < len(self.doc_store):
                results.append(self.doc_store[idx])
        return results
