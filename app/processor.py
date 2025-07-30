# app/processor.py
import os
import requests
import tempfile
import mimetypes
import PyPDF2
import docx

class DocumentProcessor:
    def __init__(self):
        pass

    def download_file(self, url: str) -> str:
        try:
            response = requests.get(url)
            response.raise_for_status()
            _, ext = os.path.splitext(url)
            if not ext:
                ext = mimetypes.guess_extension(response.headers.get('Content-Type', 'application/pdf'))

            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
                tmp.write(response.content)
                return tmp.name
        except Exception as e:
            print(f"[ERROR] Failed to download file: {e}")
            return None

    def extract_text_from_pdf(self, file_path: str) -> str:
        text = ""
        try:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            print(f"[ERROR] PDF extraction failed: {e}")
        return text

    def extract_text_from_docx(self, file_path: str) -> str:
        text = ""
        try:
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            print(f"[ERROR] DOCX extraction failed: {e}")
        return text

    def process(self, url: str) -> str:
        file_path = self.download_file(url)
        if not file_path:
            return ""

        ext = os.path.splitext(file_path)[-1].lower()
        if ext == ".pdf":
            return self.extract_text_from_pdf(file_path)
        elif ext == ".docx":
            return self.extract_text_from_docx(file_path)
        else:
            print(f"[WARN] Unsupported file type: {ext}")
            return ""
