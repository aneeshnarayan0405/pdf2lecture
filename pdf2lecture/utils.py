import re
import math
from textwrap import wrap
from typing import List

def clean_whitespace(text: str) -> str:
    """
    Normalize whitespace and clean up text formatting.
    
    Args:
        text: Raw extracted text from PDF
        
    Returns:
        Cleaned text with normalized spacing
    """
    # Replace carriage returns with newlines
    text = re.sub(r'\r', '\n', text)
    # Collapse multiple newlines
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    # Collapse multiple spaces/tabs
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def chunk_text(text: str, max_chars: int = 1200) -> List[str]:
    """
    Break text into chunks for summarization, respecting paragraph boundaries.
    
    Args:
        text: Input text to chunk
        max_chars: Maximum characters per chunk
        
    Returns:
        List of text chunks
    """
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    chunks = []
    current_chunk = ""
    
    for paragraph in paragraphs:
        # If adding this paragraph doesn't exceed max length
        if len(current_chunk) + len(paragraph) + 2 <= max_chars:
            if current_chunk:
                current_chunk += "\n\n" + paragraph
            else:
                current_chunk = paragraph
        else:
            # Save current chunk if it's not empty
            if current_chunk:
                chunks.append(current_chunk)
            
            # Handle very long paragraphs
            if len(paragraph) <= max_chars:
                current_chunk = paragraph
            else:
                # Split long paragraph into smaller chunks
                words = paragraph.split()
                current_words = []
                
                for word in words:
                    if len(' '.join(current_words + [word])) <= max_chars:
                        current_words.append(word)
                    else:
                        if current_words:
                            chunks.append(' '.join(current_words))
                        current_words = [word]
                
                if current_words:
                    chunks.append(' '.join(current_words))
                current_chunk = ""
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

def calculate_read_time(text: str, words_per_minute: int = 150) -> float:
    """
    Calculate estimated reading time for text.
    
    Args:
        text: Text to calculate reading time for
        words_per_minute: Average reading speed
        
    Returns:
        Estimated reading time in seconds
    """
    words = len(text.split())
    minutes = words / words_per_minute
    return minutes * 60