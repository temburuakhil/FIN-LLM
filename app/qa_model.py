# app/qa_model.py
from transformers import pipeline

class QAModel:
    def __init__(self, model_name: str = "distilbert-base-uncased-distilled-squad"):
        self.qa_pipeline = pipeline("question-answering", model=model_name)

    def answer(self, query: str, context: str) -> str:
        try:
            result = self.qa_pipeline(question=query, context=context)
            return result["answer"]
        except Exception as e:
            print(f"[ERROR] QA failed: {e}")
            return "Sorry, I couldn't find an answer."
