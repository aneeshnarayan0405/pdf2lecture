# pdfplumber_extractor.py
import os
import pdfplumber

def extract_text(pdf_path: str) -> str:
    """Extract text using pdfplumber only"""
    text_parts = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text and text.strip():
                    text_parts.append(text.strip())
    except Exception as e:
        print(f"PDF extraction error: {e}")
        return ""
    
    return "\n\n".join(text_parts)

def get_pdf_info(pdf_path: str) -> dict:
    """Get PDF info using pdfplumber"""
    info = {"pages": 0, "title": "", "author": "", "subject": ""}
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            info["pages"] = len(pdf.pages)
    except Exception as e:
        print(f"Error getting PDF info: {e}")
    
    return info