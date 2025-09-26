# app.py - FIXED IMPORTS
#!/usr/bin/env python3
"""
PDF to Lecture Generator - Command Line Interface
Converts PDF files into PowerPoint presentations and narrated videos.
"""

import argparse
import os
import sys
from pathlib import Path

# Import from our fixed modules
from pdf2lecture.extractor import extract_text, extract_images, get_pdf_info
from pdf2lecture.utils import clean_whitespace

def test_dependencies():
    """Test if all required dependencies are available."""
    dependencies = {
        "pdfplumber": "PDF text extraction",
        "python-pptx": "PowerPoint generation", 
        "gTTS": "Google Text-to-Speech",
        "pyttsx3": "Offline Text-to-Speech",
        "moviepy": "Video creation",
        "PIL": "Image processing (Pillow)"
    }
    
    missing = []
    for dep, purpose in dependencies.items():
        try:
            if dep == "PIL":
                import PIL
            else:
                __import__(dep)
            print(f"✓ {dep}: {purpose}")
        except ImportError:
            print(f"✗ {dep}: {purpose} - MISSING")
            missing.append(dep)
    
    # Test optional dependencies
    optional_deps = {
        "fitz": "PyMuPDF (enhanced PDF processing)",
        "transformers": "AI summarization",
        "torch": "PyTorch (for AI models)"
    }
    
    for dep, purpose in optional_deps.items():
        try:
            __import__(dep)
            print(f"✓ {dep}: {purpose} (optional)")
        except ImportError:
            print(f"○ {dep}: {purpose} - Not available (will use fallbacks)")
    
    return missing

def simple_summarize(text: str, max_slides: int = 10) -> list:
    """
    Simple summarization fallback when transformers is not available.
    Creates slides by splitting text into chunks.
    """
    from pdf2lecture.utils import chunk_text
    
    # Clean and chunk the text
    cleaned = clean_whitespace(text)
    chunks = chunk_text(cleaned, max_chars=1000)
    
    # Limit to max_slides
    if len(chunks) > max_slides:
        chunks = chunks[:max_slides]
    
    # Simple summarization: take first 2 sentences or first 200 chars
    summaries = []
    for chunk in chunks:
        sentences = chunk.split('.')
        if len(sentences) >= 2:
            summary = '.'.join(sentences[:2]) + '.'
        else:
            summary = chunk[:200] + '...' if len(chunk) > 200 else chunk
        summaries.append(summary)
    
    return summaries

def run_pipeline(pdf_path: str, output_dir: str = "output", 
                use_tts: str = "gtts", model_name: str = "facebook/bart-large-cnn",
                precise_timing: bool = False) -> dict:
    """
    Main pipeline function to convert PDF to lecture materials.
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    results = {}
    
    print("=" * 60)
    print("PDF to Lecture Generator")
    print("=" * 60)
    
    # Step 1: PDF Information
    print("\n[1/7] Analyzing PDF...")
    pdf_info = get_pdf_info(pdf_path)
    print(f"   Pages: {pdf_info['pages']}")
    print(f"   Title: {pdf_info['title'] or 'N/A'}")
    
    # Step 2: Text Extraction
    print("\n[2/7] Extracting text from PDF...")
    raw_text = extract_text(pdf_path)
    raw_text = clean_whitespace(raw_text)
    print(f"   Extracted {len(raw_text)} characters")
    
    if len(raw_text) < 100:
        print("   ERROR: Very little text extracted. PDF may be scanned or image-based.")
        # Try alternative extraction method
        print("   Trying alternative extraction method...")
        raw_text = extract_text(pdf_path, method="fitz")
        raw_text = clean_whitespace(raw_text)
        print(f"   Alternative method extracted {len(raw_text)} characters")
    
    if len(raw_text) < 50:
        raise Exception("Cannot extract sufficient text from PDF. Please try a different PDF file.")
    
    # Step 3: Summarization
    print("\n[3/7] Summarizing content...")
    slide_summaries = []
    overall_summary = ""
    
    try:
        # Try using transformers if available
        from pdf2lecture.summarizer import Summarizer
        summarizer = Summarizer(model_name=model_name)
        slide_summaries, overall_summary = summarizer.hierarchical_summary(raw_text)
        print(f"   AI Summarization: Created {len(slide_summaries)} slide summaries")
    except ImportError:
        # Fallback to simple summarization
        print("   AI summarization not available, using simple text chunking...")
        slide_summaries = simple_summarize(raw_text)
        overall_summary = "Summary generated using text chunking (AI summarization not available)"
        print(f"   Simple Summarization: Created {len(slide_summaries)} slide summaries")
    
    # Save summaries
    summary_path = os.path.join(output_dir, "summaries.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("OVERALL SUMMARY:\n")
        f.write(overall_summary)
        f.write("\n\nSLIDE SUMMARIES:\n")
        for i, summary in enumerate(slide_summaries, 1):
            f.write(f"\nSlide {i}:\n{summary}\n")
    
    results["summary"] = summary_path
    
    # Step 4: PowerPoint Generation
    print("\n[4/7] Creating PowerPoint presentation...")
    try:
        from pdf2lecture.slides import create_pptx
        pptx_path = os.path.join(output_dir, "lecture.pptx")
        create_pptx(slide_summaries, output_path=pptx_path, 
                    title=pdf_info.get('title', 'Generated Lecture')[:50])
        print(f"   Saved: {pptx_path}")
        results["pptx"] = pptx_path
    except ImportError as e:
        print(f"   WARNING: PowerPoint generation failed: {e}")
        results["pptx"] = None
    
    # Step 5: Slide Images
    print("\n[5/7] Generating slide images...")
    try:
        from pdf2lecture.slides import create_slide_images
        images_dir = os.path.join(output_dir, "slide_images")
        slide_images = create_slide_images(slide_summaries, output_dir=images_dir)
        print(f"   Created {len(slide_images)} slide images")
        results["images"] = slide_images
    except ImportError as e:
        print(f"   WARNING: Slide image generation failed: {e}")
        results["images"] = []
    
    # Step 6: Text-to-Speech
    print("\n[6/7] Generating narration...")
    audio_path = os.path.join(output_dir, "narration.mp3")
    
    try:
        from pdf2lecture.tts import group_texts_to_single_audio
        group_texts_to_single_audio(slide_summaries, audio_path, method=use_tts)
        print(f"   Saved: {audio_path}")
        results["audio"] = audio_path
    except ImportError as e:
        print(f"   WARNING: TTS generation failed: {e}")
        results["audio"] = None
    
    # Step 7: Video Creation
    print("\n[7/7] Creating video lecture...")
    if results.get("images") and results.get("audio"):
        try:
            from pdf2lecture.video import make_video_from_images_and_audio
            video_path = os.path.join(output_dir, "lecture.mp4")
            make_video_from_images_and_audio(results["images"], results["audio"], video_path)
            print(f"   Saved: {video_path}")
            results["video"] = video_path
        except ImportError as e:
            print(f"   WARNING: Video creation failed: {e}")
            results["video"] = None
    else:
        print("   Skipping video creation (missing images or audio)")
        results["video"] = None
    
    print("\n" + "=" * 60)
    print("PROCESSING COMPLETE!")
    print("=" * 60)
    print(f"Output files saved in: {output_dir}")
    
    for key, path in results.items():
        if path:
            if isinstance(path, list):
                print(f" - {key}: {len(path)} items")
            else:
                print(f" - {key}: {os.path.basename(path)}")
    
    return results

def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF files into PowerPoint presentations and narrated videos.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.pdf
  %(prog)s lecture.pdf --out my_lecture --tts pyttsx3
  %(prog)s paper.pdf --model "sshleifer/distilbart-cnn-12-6"
        """
    )
    
    parser.add_argument("pdf_file", help="Path to the PDF file to process")
    parser.add_argument("--out", "-o", default="output", 
                       help="Output directory (default: output)")
    parser.add_argument("--tts", choices=["gtts", "pyttsx3"], default="gtts",
                       help="Text-to-speech engine (default: gtts)")
    parser.add_argument("--model", "-m", default="facebook/bart-large-cnn",
                       help="Summarization model name (default: facebook/bart-large-cnn)")
    parser.add_argument("--precise-timing", action="store_true",
                       help="Use precise per-slide audio timing")
    parser.add_argument("--test-deps", action="store_true",
                       help="Test dependencies before running")
    
    args = parser.parse_args()
    
    # Check if PDF file exists
    if not os.path.exists(args.pdf_file):
        print(f"Error: PDF file '{args.pdf_file}' not found.")
        sys.exit(1)
    
    # Test dependencies if requested
    if args.test_deps:
        print("Testing dependencies...")
        missing = test_dependencies()
        if missing:
            print(f"\nMissing required dependencies: {missing}")
            print("Please install them with: pip install " + " ".join(missing))
            if "fitz" in missing:
                print("Note: fitz is part of pymupdf. Install with: pip install pymupdf")
        print()
    
    try:
        results = run_pipeline(
            pdf_path=args.pdf_file,
            output_dir=args.out,
            use_tts=args.tts,
            model_name=args.model,
            precise_timing=args.precise_timing
        )
    except Exception as e:
        print(f"Error during processing: {e}")
        print("\nTroubleshooting tips:")
        print("1. Try with --test-deps to check dependencies")
        print("2. Ensure the PDF file is not password protected")
        print("3. Try a different PDF file")
        print("4. Use --tts pyttsx3 for offline TTS")
        sys.exit(1)

if __name__ == "__main__":
    main()