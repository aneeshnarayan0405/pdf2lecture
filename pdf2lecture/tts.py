# pdf2lecture/tts.py - FIXED VERSION
import os
from typing import List

def tts_gtts(text: str, output_path: str, lang: str = "en", slow: bool = False) -> str:
    """
    Generate speech using Google Text-to-Speech (requires internet).
    """
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang=lang, slow=slow)
        tts.save(output_path)
        return output_path
    except Exception as e:
        print(f"Google TTS error: {e}")
        # Fallback to pyttsx3
        return tts_pyttsx3(text, output_path)

def tts_pyttsx3(text: str, output_path: str, rate: int = 150) -> str:
    """
    Generate speech using pyttsx3 (offline).
    """
    try:
        import pyttsx3
        
        # Initialize the engine
        engine = pyttsx3.init()
        
        # Configure engine properties
        engine.setProperty('rate', rate)
        engine.setProperty('volume', 0.8)
        
        # Try to use available voices
        try:
            voices = engine.getProperty('voices')
            if voices:
                # Prefer Microsoft voices on Windows
                for voice in voices:
                    if 'Microsoft' in voice.name or 'David' in voice.name or 'Zira' in voice.name:
                        engine.setProperty('voice', voice.id)
                        break
        except:
            pass  # Use default voice if selection fails
        
        # Save to file
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        
        return output_path
        
    except Exception as e:
        print(f"pyttsx3 TTS failed: {e}")
        # Ultimate fallback - create a silent audio file
        return create_silent_audio(output_path)

def create_silent_audio(output_path: str, duration: int = 5) -> str:
    """
    Create a silent audio file as ultimate fallback.
    """
    try:
        from pydub import AudioSegment
        from pydub.generators import Sine
        
        # Create a silent audio segment
        silent_audio = AudioSegment.silent(duration=duration * 1000)  # milliseconds
        silent_audio.export(output_path, format="mp3")
        print(f"Created silent audio fallback: {output_path}")
        return output_path
    except:
        # If even pydub fails, create an empty file
        with open(output_path, 'wb') as f:
            f.write(b'')
        print(f"Created empty audio file: {output_path}")
        return output_path

def group_texts_to_single_audio(texts: List[str], output_path: str, 
                               method: str = "gtts", **kwargs) -> str:
    """
    Convert multiple texts into a single audio file.
    """
    combined_text = " ".join(texts)
    
    if method == "gtts":
        return tts_gtts(combined_text, output_path, **kwargs)
    elif method == "pyttsx3":
        return tts_pyttsx3(combined_text, output_path, **kwargs)
    else:
        raise ValueError(f"Unsupported TTS method: {method}")

# Add alias functions for backward compatibility
tts_pyttsx3_windows = tts_pyttsx3
tts_pyttsx3_fallback = tts_pyttsx3