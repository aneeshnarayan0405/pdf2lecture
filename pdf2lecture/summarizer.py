from transformers import pipeline, AutoTokenizer
from typing import List, Tuple
import torch
from .utils import chunk_text

class Summarizer:
    """
    Text summarization using Transformer models.
    """
    
    def __init__(self, model_name: str = "facebook/bart-large-cnn", device: int = -1):
        """
        Initialize summarizer with specified model.
        
        Args:
            model_name: HuggingFace model name
            device: -1 for CPU, 0+ for GPU
        """
        self.model_name = model_name
        self.device = device
        
        # Check if GPU is available
        if device >= 0 and torch.cuda.is_available():
            self.device = device
        else:
            self.device = -1  # Use CPU
        
        try:
            self.pipeline = pipeline(
                "summarization",
                model=model_name,
                device=self.device,
                tokenizer=model_name
            )
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        except Exception as e:
            print(f"Error loading model {model_name}: {e}")
            # Fallback to a smaller model
            fallback_model = "sshleifer/distilbart-cnn-12-6"
            print(f"Trying fallback model: {fallback_model}")
            self.pipeline = pipeline(
                "summarization",
                model=fallback_model,
                device=self.device
            )
            self.tokenizer = AutoTokenizer.from_pretrained(fallback_model)
    
    def summarize_chunk(self, text: str, max_length: int = 150, min_length: int = 30) -> str:
        """
        Summarize a single chunk of text.
        
        Args:
            text: Input text to summarize
            max_length: Maximum summary length
            min_length: Minimum summary length
            
        Returns:
            Summarized text
        """
        try:
            # Tokenize to check length
            tokens = self.tokenizer.encode(text)
            if len(tokens) < 50:  # Very short text
                return text[:200]  # Just truncate
            
            summary = self.pipeline(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False,
                truncation=True
            )[0]["summary_text"]
            return summary.strip()
        except Exception as e:
            print(f"Summarization error: {e}")
            # Fallback: return first 150 characters
            return text[:150] + "..." if len(text) > 150 else text
    
    def summarize_chunks(self, text: str, chunk_max_chars: int = 1200) -> List[str]:
        """
        Summarize text by first chunking it.
        
        Args:
            text: Input text to summarize
            chunk_max_chars: Maximum characters per chunk
            
        Returns:
            List of slide summaries
        """
        chunks = chunk_text(text, max_chars=chunk_max_chars)
        summaries = []
        
        print(f"Summarizing {len(chunks)} chunks...")
        for i, chunk in enumerate(chunks, 1):
            print(f"  Chunk {i}/{len(chunks)} ({len(chunk)} chars)")
            summary = self.summarize_chunk(chunk)
            summaries.append(summary)
        
        return summaries
    
    def hierarchical_summary(self, text: str, chunk_max_chars: int = 1200) -> Tuple[List[str], str]:
        """
        Two-level summarization: chunk summaries + overall summary.
        
        Args:
            text: Input text
            chunk_max_chars: Maximum characters per chunk
            
        Returns:
            Tuple of (slide summaries, overall summary)
        """
        # First level: summarize chunks for slides
        slide_summaries = self.summarize_chunks(text, chunk_max_chars)
        
        # Second level: create overall summary from slide summaries
        combined_summaries = " ".join(slide_summaries)
        if len(combined_summaries) > 500:
            overall_summary = self.summarize_chunk(combined_summaries, max_length=200, min_length=50)
        else:
            overall_summary = combined_summaries[:300] + "..." if len(combined_summaries) > 300 else combined_summaries
        
        return slide_summaries, overall_summary

class OpenAISummarizer:
    """
    Alternative summarizer using OpenAI API (optional).
    """
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        # Implementation would go here for premium option
        pass