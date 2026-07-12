
import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return normalize_text(text)

def normalize_text(text):
    # Remove extra whitespaces and newlines
    text = re.sub(r'\s+', ' ', text)
    return text.strip()