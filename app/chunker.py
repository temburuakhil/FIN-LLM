# app/chunker.py
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Chunk:
    content: str
    metadata: Dict

class TextChunker:
    def __init__(self, chunk_size: int = 500, overlap: int = 100):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str, metadata: Dict) -> List[Chunk]:
        words = text.split()
        chunks = []
        start = 0
        while start < len(words):
            end = min(start + self.chunk_size, len(words))
            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)
            chunks.append(Chunk(content=chunk_text, metadata=metadata))
            start += self.chunk_size - self.overlap
        return chunks
