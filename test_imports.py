# test_imports.py
try:
    import pymupdf
    print("✓ pymupdf imported successfully")
except ImportError as e:
    print(f"✗ pymupdf import failed: {e}")

try:
    import transformers
    print("✓ transformers imported successfully")
except ImportError as e:
    print(f"✗ transformers import failed: {e}")

try:
    import torch
    print("✓ torch imported successfully")
except ImportError as e:
    print(f"✗ torch import failed: {e}")

try:
    from moviepy.editor import VideoFileClip
    print("✓ moviepy imported successfully")
except ImportError as e:
    print(f"✗ moviepy import failed: {e}")

try:
    from gtts import gTTS
    print("✓ gTTS imported successfully")
except ImportError as e:
    print(f"✗ gTTS import failed: {e}")

try:
    import pyttsx3
    print("✓ pyttsx3 imported successfully")
except ImportError as e:
    print(f"✗ pyttsx3 import failed: {e}")

print("\nTesting PDF extraction...")
try:
    import fitz  # PyMuPDF
    print("✓ PyMuPDF (fitz) available")
except ImportError as e:
    print(f"✗ PyMuPDF import failed: {e}")