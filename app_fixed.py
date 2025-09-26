# app_fixed.py
#!/usr/bin/env python3
"""
PDF to Lecture Generator - Fixed imports version
"""

import os
import sys

# Try to import extractor with fallback
try:
    from pdf2lecture.extractor import extract_text, get_pdf_info
except ImportError as e:
    print(f"Import error: {e}")
    print("Trying alternative extractor...")
    
    # Use pdfplumber-only version
    from pdf2lecture.pdfplumber_extractor import extract_text, get_pdf_info

def main():
    print("Testing PDF extraction...")
    
    pdf_path = "examples/demo_sample.pdf"
    if not os.path.exists(pdf_path):
        print(f"PDF file not found: {pdf_path}")
        return
    
    # Test extraction
    info = get_pdf_info(pdf_path)
    print(f"PDF Info: {info}")
    
    text = extract_text(pdf_path)
    print(f"Extracted {len(text)} characters")
    
    if len(text) > 100:
        print("✓ PDF extraction successful!")
        print("\nFirst 200 characters:")
        print(text[:200] + "..." if len(text) > 200 else text)
    else:
        print("✗ PDF extraction failed")

if __name__ == "__main__":
    main()