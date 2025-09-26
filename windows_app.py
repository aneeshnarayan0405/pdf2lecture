# windows_app.py
#!/usr/bin/env python3
"""
Windows-optimized PDF to Lecture Generator
"""

import os
import sys
import argparse
from pdf2lecture.extractor import extract_text, get_pdf_info
from pdf2lecture.utils import clean_whitespace
from pdf2lecture.tts import get_best_tts_method, group_texts_to_single_audio

def windows_pipeline(pdf_path: str, output_dir: str = "windows_output"):
    """
    Windows-optimized pipeline with better error handling.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print("Windows PDF to Lecture Generator")
    print("=" * 60)
    
    # Auto-detect best TTS method
    tts_method = get_best_tts_method()
    print(f"Detected TTS method: {tts_method}")
    
    if tts_method == "none":
        print("WARNING: No TTS method available. Video will have no audio.")
    
    # Step 1: PDF Analysis
    print("\n[1/6] Analyzing PDF...")
    pdf_info = get_pdf_info(pdf_path)
    print(f"   Pages: {pdf_info['pages']}")
    
    # Step 2: Text Extraction
    print("\n[2/6] Extracting text...")
    raw_text = extract_text(pdf_path)
    cleaned_text = clean_whitespace(raw_text)
    print(f"   Extracted {len(cleaned_text)} characters")
    
    if len(cleaned_text) < 100:
        print("   ERROR: Insufficient text extracted")
        return
    
    # Step 3: Simple Summarization (skip AI to save time)
    print("\n[3/6] Creating slides...")
    from pdf2lecture.utils import chunk_text
    chunks = chunk_text(cleaned_text, max_chars=800)
    slides = chunks[:10]  # Limit to 10 slides
    
    # Simple summarization
    summaries = []
    for chunk in slides:
        # Take first sentence or first 150 chars
        sentences = chunk.split('.')
        if len(sentences) > 1:
            summary = sentences[0] + '.'
        else:
            summary = chunk[:150] + '...' if len(chunk) > 150 else chunk
        summaries.append(summary)
    
    print(f"   Created {len(summaries)} slides")
    
    # Save text summary
    with open(os.path.join(output_dir, "slides.txt"), "w", encoding="utf-8") as f:
        for i, summary in enumerate(summaries, 1):
            f.write(f"Slide {i}: {summary}\n\n")
    
    # Step 4: Create PowerPoint
    print("\n[4/6] Creating PowerPoint...")
    try:
        from pdf2lecture.slides import create_pptx
        pptx_path = os.path.join(output_dir, "presentation.pptx")
        create_pptx(summaries, pptx_path)
        print(f"   Saved: {pptx_path}")
    except Exception as e:
        print(f"   PowerPoint failed: {e}")
    
    # Step 5: Create Slide Images
    print("\n[5/6] Creating slide images...")
    try:
        from pdf2lecture.slides import create_slide_images
        images_dir = os.path.join(output_dir, "images")
        images = create_slide_images(summaries, images_dir)
        print(f"   Created {len(images)} images")
    except Exception as e:
        print(f"   Image creation failed: {e}")
        images = []
    
    # Step 6: Text-to-Speech and Video
    if tts_method != "none" and images:
        print("\n[6/6] Creating video...")
        try:
            # Generate audio
            audio_path = os.path.join(output_dir, "audio.mp3")
            group_texts_to_single_audio(summaries, audio_path, method=tts_method)
            print(f"   Audio created: {audio_path}")
            
            # Create video
            from pdf2lecture.video import make_video_from_images_and_audio
            video_path = os.path.join(output_dir, "lecture.mp4")
            make_video_from_images_and_audio(images, audio_path, video_path)
            print(f"   Video created: {video_path}")
            
        except Exception as e:
            print(f"   Audio/Video creation failed: {e}")
    else:
        print("\n[6/6] Skipping audio/video (no TTS or images available)")
    
    print("\n" + "=" * 60)
    print("PROCESS COMPLETE!")
    print(f"Output in: {output_dir}")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="Windows PDF to Lecture Generator")
    parser.add_argument("pdf_file", help="PDF file to process")
    parser.add_argument("--out", default="windows_output", help="Output directory")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.pdf_file):
        print(f"Error: PDF file '{args.pdf_file}' not found")
        return
    
    try:
        windows_pipeline(args.pdf_file, args.out)
    except Exception as e:
        print(f"Error: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure PDF is not password protected")
        print("2. Try a different PDF file")
        print("3. Check internet connection for gTTS")

if __name__ == "__main__":
    main()