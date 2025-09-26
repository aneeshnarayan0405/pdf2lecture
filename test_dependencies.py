# test_dependencies.py
def test_imports():
    """Test all required imports"""
    dependencies = [
        ("pdfplumber", "PDF text extraction"),
        ("fitz", "PyMuPDF - enhanced PDF processing"), 
        ("pptx", "python-pptx - PowerPoint generation"),
        ("gtts", "gTTS - Google Text-to-Speech"),
        ("pyttsx3", "Offline Text-to-Speech"),
        ("moviepy.editor", "Video editing"),
        ("PIL", "Pillow - Image processing"),
        ("transformers", "Hugging Face Transformers"),
        ("torch", "PyTorch"),
    ]
    
    print("Testing dependencies...")
    print("=" * 50)
    
    for module_name, purpose in dependencies:
        try:
            if module_name == "fitz":
                # Special handling for PyMuPDF
                import fitz
                print(f"✓ fitz (PyMuPDF) v{fitz.VersionBind}: {purpose}")
            elif module_name == "PIL":
                import PIL
                print(f"✓ PIL (Pillow) v{PIL.__version__}: {purpose}")
            else:
                module = __import__(module_name)
                version = getattr(module, '__version__', 'unknown')
                print(f"✓ {module_name} v{version}: {purpose}")
        except ImportError as e:
            print(f"✗ {module_name}: {purpose}")
            print(f"  Error: {e}")
    
    print("=" * 50)

if __name__ == "__main__":
    test_imports()