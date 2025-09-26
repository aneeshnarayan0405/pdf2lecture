# pdf2lecture/pdfplumber_extractor.py
import os
from typing import List
import pdfplumber

def extract_text(pdf_path: str) -> str:
    """
    Extract text from PDF using only pdfplumber.
    """
    text_parts = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # Try multiple extraction methods
                text = page.extract_text()
                if not text or not text.strip():
                    # Fallback: extract words and reconstruct
                    words = page.extract_words()
                    if words:
                        text = ' '.join(word['text'] for word in words)
                
                if text and text.strip():
                    text_parts.append(text.strip())
                    
    except Exception as e:
        print(f"PDF extraction error: {e}")
        return ""
    
    return "\n\n".join(text_parts)

def get_pdf_info(pdf_path: str) -> dict:
    """
    Get basic PDF information using pdfplumber.
    """
    info = {"pages": 0, "title": "", "author": "", "subject": ""}
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            info["pages"] = len(pdf.pages)
    except Exception as e:
        print(f"Error getting PDF info: {e}")
    
    return info

def extract_images(pdf_path: str, output_dir: str = "extracted_images") -> List[str]:
    """
    Basic image extraction (pdfplumber has limited image support).
    """
    print("Note: pdfplumber has limited image extraction capabilities.")
    print("For better image extraction, install PyMuPDF: pip install pymupdf")
    return []