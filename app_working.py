# app_working.py
#!/usr/bin/env python3
"""
PDF to Lecture Generator - Working version with fixed imports
"""

import argparse
import os
import sys

# Import with proper error handling
try:
    from pdf2lecture.extractor import extract_text, get_pdf_info
    EXTRACTOR_AVAILABLE = True
except ImportError as e:
    print(f"Extractor import warning: {e}")
    # Use fallback extractor
    from pdfplumber_extractor import extract_text, get_pdf_info
    EXTRACTOR_AVAILABLE = False

from pdf2lecture.utils import clean_whitespace

def run_working_pipeline(pdf_path: str, output_dir: str = "working_output"):
    """Working pipeline with robust error handling"""
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print("PDF to Lecture Generator - WORKING VERSION")
    print("=" * 60)
    
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
        print("   ERROR: Insufficient text")
        return
    
    # Step 3: Simple Summarization
    print("\n[3/6] Creating slides...")
    from pdf2lecture.utils import chunk_text
    chunks = chunk_text(cleaned_text, max_chars=800)
    slides = chunks[:10]  # Limit to 10 slides
    
    # Simple summarization
    summaries = []
    for chunk in slides:
        sentences = chunk.split('.')
        if len(sentences) > 1:
            summary = sentences[0] + '.'
        else:
            summary = chunk[:150] + '...' if len(chunk) > 150 else chunk
        summaries.append(summary)
    
    print(f"   Created {len(summaries)} slides")
    
    # Save summary
    with open(os.path.join(output_dir, "slides.txt"), "w", encoding="utf-8") as f:
        for i, summary in enumerate(summaries, 1):
            f.write(f"Slide {i}: {summary}\n\n")
    
    # Step 4: Create PowerPoint
    print("\n[4/6] Creating PowerPoint...")
    try:
        from pdf2lecture.slides import create_pptx
        pptx_path = os.path.join(output_dir, "presentation.pptx")
        create_pptx(summaries, pptx_path)
        print(f"   ✓ PowerPoint saved: {pptx_path}")
    except Exception as e:
        print(f"   ✗ PowerPoint failed: {e}")
    
    # Step 5: Create Slide Images
    print("\n[5/6] Creating slide images...")
    try:
        from pdf2lecture.slides import create_slide_images
        images_dir = os.path.join(output_dir, "images")
        images = create_slide_images(summaries, images_dir)
        print(f"   ✓ Created {len(images)} slide images")
    except Exception as e:
        print(f"   ✗ Image creation failed: {e}")
        images = []
    
    # Step 6: Text-to-Speech and Video
    print("\n[6/6] Creating audio and video...")
    try:
        # Generate audio using gTTS
        from gtts import gTTS
        combined_text = " ".join(summaries)
        if len(combined_text) > 4000:
            combined_text = combined_text[:4000]
        
        audio_path = os.path.join(output_dir, "narration.mp3")
        tts = gTTS(combined_text)
        tts.save(audio_path)
        print(f"   ✓ Audio saved: {audio_path}")
        
        # Create video if images available
        if images:
            from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
            audio = AudioFileClip(audio_path)
            audio_duration = audio.duration
            slide_duration = audio_duration / len(images)
            
            clips = []
            for image_path in images:
                clip = ImageClip(image_path, duration=slide_duration)
                clips.append(clip)
            
            video = concatenate_videoclips(clips)
            video = video.set_audio(audio)
            
            video_path = os.path.join(output_dir, "lecture.mp4")
            video.write_videofile(video_path, fps=24, verbose=False, logger=None)
            print(f"   ✓ Video saved: {video_path}")
        
    except Exception as e:
        print(f"   ✗ Audio/Video failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 PROCESS COMPLETE!")
    print(f"📁 Output directory: {output_dir}")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="Working PDF to Lecture Generator")
    parser.add_argument("pdf_file", help="PDF file to process")
    parser.add_argument("--out", default="working_output", help="Output directory")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.pdf_file):
        print(f"Error: PDF file '{args.pdf_file}' not found")
        return
    
    try:
        run_working_pipeline(args.pdf_file, args.out)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()