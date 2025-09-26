# app_ai.py
#!/usr/bin/env python3
"""
PDF to Lecture Generator with AI Summarization
"""

import argparse
import os

def run_ai_pipeline(pdf_path: str, output_dir: str = "ai_output"):
    """Pipeline with AI summarization"""
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print("PDF to Lecture Generator with AI")
    print("=" * 60)
    
    # Step 1: Extract text
    print("\n[1/6] Extracting text...")
    from pdfplumber_extractor import extract_text, get_pdf_info
    from pdf2lecture.utils import clean_whitespace
    
    pdf_info = get_pdf_info(pdf_path)
    print(f"   Pages: {pdf_info['pages']}")
    
    raw_text = extract_text(pdf_path)
    cleaned_text = clean_whitespace(raw_text)
    print(f"   Extracted {len(cleaned_text)} characters")
    
    # Step 2: AI Summarization
    print("\n[2/6] AI Summarization...")
    try:
        from transformers import pipeline
        
        # Use a smaller, faster model for summarization
        summarizer = pipeline("summarization", 
                            model="sshleifer/distilbart-cnn-12-6",
                            tokenizer="sshleifer/distilbart-cnn-12-6")
        
        # Split text into chunks for summarization
        from pdf2lecture.utils import chunk_text
        chunks = chunk_text(cleaned_text, max_chars=1000)
        
        summaries = []
        for i, chunk in enumerate(chunks[:5]):  # Limit to 5 chunks for speed
            print(f"   Summarizing chunk {i+1}/{len(chunks[:5])}")
            if len(chunk) > 50:
                summary = summarizer(chunk, max_length=120, min_length=30, do_sample=False)[0]['summary_text']
                summaries.append(summary)
            else:
                summaries.append(chunk)  # Keep short chunks as-is
        
        print(f"   Created {len(summaries)} AI summaries")
        
    except Exception as e:
        print(f"   AI summarization failed, using simple method: {e}")
        # Fallback to simple method
        from pdf2lecture.utils import chunk_text
        chunks = chunk_text(cleaned_text, max_chars=800)
        summaries = chunks[:8]
    
    # Step 3: Create PowerPoint
    print("\n[3/6] Creating PowerPoint...")
    try:
        from pdf2lecture.slides import create_pptx
        pptx_path = os.path.join(output_dir, "ai_presentation.pptx")
        create_pptx(summaries, pptx_path, title="AI Generated Lecture")
        print(f"   ✓ PowerPoint saved")
    except Exception as e:
        print(f"   ✗ PowerPoint failed: {e}")
    
    # Step 4: Create images
    print("\n[4/6] Creating slide images...")
    try:
        from pdf2lecture.slides import create_slide_images
        images = create_slide_images(summaries, os.path.join(output_dir, "images"))
        print(f"   ✓ Created {len(images)} images")
    except Exception as e:
        print(f"   ✗ Image creation failed: {e}")
        images = []
    
    # Step 5: Generate audio
    print("\n[5/6] Generating audio...")
    try:
        from gtts import gTTS
        combined_text = " ".join(summaries)
        if len(combined_text) > 4000:
            combined_text = combined_text[:4000]
        
        audio_path = os.path.join(output_dir, "ai_narration.mp3")
        tts = gTTS(combined_text)
        tts.save(audio_path)
        print(f"   ✓ Audio saved")
    except Exception as e:
        print(f"   ✗ Audio failed: {e}")
        audio_path = None
    
    # Step 6: Create video
    print("\n[6/6] Creating video...")
    if images and audio_path:
        try:
            from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
            audio = AudioFileClip(audio_path)
            slide_duration = audio.duration / len(images)
            
            clips = [ImageClip(img, duration=slide_duration) for img in images]
            video = concatenate_videoclips(clips).set_audio(audio)
            
            video_path = os.path.join(output_dir, "ai_lecture.mp4")
            video.write_videofile(video_path, fps=24, verbose=False)
            print(f"   ✓ Video saved")
        except Exception as e:
            print(f"   ✗ Video failed: {e}")
    
    print("\n" + "=" * 60)
    print("🤖 AI PROCESSING COMPLETE!")
    print(f"📁 Output: {output_dir}")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="AI PDF to Lecture Generator")
    parser.add_argument("pdf_file", help="PDF file to process")
    parser.add_argument("--out", default="ai_output", help="Output directory")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.pdf_file):
        print(f"Error: PDF file '{args.pdf_file}' not found")
        return
    
    run_ai_pipeline(args.pdf_file, args.out)

if __name__ == "__main__":
    main()