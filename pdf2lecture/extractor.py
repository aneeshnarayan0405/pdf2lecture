# pdf2lecture/extractor.py - FIXED IMPORTS
import os
from typing import List
import pdfplumber

def extract_text(pdf_path: str, method: str = "pdfplumber") -> str:
    """
    Extract text from PDF using pdfplumber as primary method.
    """
    try:
        if method == "pdfplumber":
            return extract_text_pdfplumber(pdf_path)
        else:
            # Fallback to PyMuPDF (fitz) if available
            try:
                # CORRECT IMPORT: fitz is PyMuPDF
                import fitz
                return extract_text_fitz(pdf_path)
            except ImportError:
                print("PyMuPDF (fitz) not available, using pdfplumber")
                return extract_text_pdfplumber(pdf_path)
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""

def extract_text_pdfplumber(pdf_path: str) -> str:
    """
    Extract text using pdfplumber - more reliable for some PDFs.
    """
    text_parts = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text and text.strip():
                    text_parts.append(text.strip())
    except Exception as e:
        print(f"pdfplumber extraction error: {e}")
    
    return "\n\n".join(text_parts)

def extract_text_fitz(pdf_path: str) -> str:
    """
    Extract text using PyMuPDF (fitz).
    """
    try:
        # CORRECT IMPORT
        import fitz
        doc = fitz.open(pdf_path)
        text_parts = []
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            if text.strip():
                text_parts.append(text.strip())
        
        doc.close()
        return "\n\n".join(text_parts)
    except Exception as e:
        print(f"PyMuPDF (fitz) extraction error: {e}")
        return ""

def get_pdf_info(pdf_path: str) -> dict:
    """
    Get basic information about PDF.
    """
    info = {"pages": 0, "title": "", "author": "", "subject": ""}
    
    try:
        # Try pdfplumber first (more reliable)
        with pdfplumber.open(pdf_path) as pdf:
            info["pages"] = len(pdf.pages)
            
        # Try to get metadata from PyMuPDF if available
        try:
            import fitz
            doc = fitz.open(pdf_path)
            metadata = doc.metadata
            info["title"] = metadata.get("title", "")
            info["author"] = metadata.get("author", "")
            info["subject"] = metadata.get("subject", "")
            doc.close()
        except:
            pass
            
    except Exception as e:
        print(f"Error getting PDF info: {e}")
        # Fallback: try to count pages using file size estimation
        try:
            file_size = os.path.getsize(pdf_path)
            # Rough estimate: 1 page per 5KB
            info["pages"] = max(1, file_size // 5000)
        except:
            info["pages"] = 1
    
    return info

def extract_images(pdf_path: str, output_dir: str = "extracted_images") -> List[str]:
    """
    Extract images from PDF (optional functionality).
    """
    os.makedirs(output_dir, exist_ok=True)
    saved_images = []
    
    try:
        import fitz  # CORRECT IMPORT
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            image_list = page.get_images(full=True)
            
            for img_index, img in enumerate(image_list, start=1):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                filename = f"page_{page_num+1}_img_{img_index}.{image_ext}"
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, "wb") as f:
                    f.write(image_bytes)
                saved_images.append(filepath)
        
        doc.close()
    except Exception as e:
        print(f"Image extraction not available: {e}")
    
    return saved_images