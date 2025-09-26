"""
PDF to Lecture Generator
Convert PDF documents into educational presentations and videos.
"""

__version__ = "1.0.0"
__author__ = "Aneesh Narayan Bandaru"
__email__ = "aneeshnarayanbandaru@gmail.com"

from .extractor import extract_text, extract_images
from .summarizer import Summarizer
from .slides import create_pptx, create_slide_images
from .tts import tts_gtts, tts_pyttsx3, group_texts_to_single_audio
from .video import make_video_from_images_and_audio
from .utils import clean_whitespace, chunk_text