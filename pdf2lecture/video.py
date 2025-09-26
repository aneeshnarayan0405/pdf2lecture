from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, CompositeAudioClip
from pydub import AudioSegment
import os
from typing import List

def make_video_from_images_and_audio(image_files: List[str], audio_file: str,
                                   output_file: str = "lecture.mp4", 
                                   fps: int = 24) -> str:
    """
    Create video from slide images and audio narration.
    
    Args:
        image_files: List of paths to slide images
        audio_file: Path to audio narration file
        output_file: Output video file path
        fps: Video frames per second
        
    Returns:
        Path to created video file
    """
    # Load audio and calculate duration per slide
    audio = AudioFileClip(audio_file)
    total_duration = audio.duration
    slides_count = len(image_files)
    duration_per_slide = total_duration / slides_count
    
    # Create video clips for each slide
    clips = []
    for image_file in image_files:
        clip = ImageClip(image_file, duration=duration_per_slide)
        clips.append(clip)
    
    # Concatenate clips and add audio
    video = concatenate_videoclips(clips, method="compose")
    video = video.set_audio(audio)
    
    # Export video
    video.write_videofile(
        output_file,
        fps=fps,
        codec="libx264",
        audio_codec="aac",
        verbose=False,
        logger=None
    )
    
    return output_file

def make_video_with_precise_timing(image_files: List[str], audio_files: List[str],
                                 output_file: str = "lecture_precise.mp4",
                                 fps: int = 24) -> str:
    """
    Create video with precise timing using per-slide audio files.
    
    Args:
        image_files: List of slide image paths
        audio_files: List of slide audio paths (must match image_files)
        output_file: Output video path
        fps: Video frames per second
        
    Returns:
        Path to created video
    """
    if len(image_files) != len(audio_files):
        raise ValueError("Number of images and audio files must match")
    
    clips = []
    for img_path, audio_path in zip(image_files, audio_files):
        # Get audio duration
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        
        # Create image clip with audio duration
        img_clip = ImageClip(img_path, duration=duration)
        img_clip = img_clip.set_audio(audio)
        clips.append(img_clip)
    
    # Concatenate all clips
    video = concatenate_videoclips(clips, method="compose")
    video.write_videofile(
        output_file,
        fps=fps,
        codec="libx264",
        audio_codec="aac",
        verbose=False,
        logger=None
    )
    
    return output_file

def add_background_music(video_path: str, music_path: str, 
                        output_path: str, music_volume: float = 0.3) -> str:
    """
    Add background music to video (optional enhancement).
    
    Args:
        video_path: Path to original video
        music_path: Path to background music file
        output_path: Output video path
        music_volume: Music volume relative to narration (0.0-1.0)
        
    Returns:
        Path to enhanced video
    """
    from moviepy.editor import VideoFileClip
    
    video = VideoFileClip(video_path)
    music = AudioFileClip(music_path).volumex(music_volume)
    
    # Set music duration to match video
    music = music.subclip(0, video.duration)
    if music.duration < video.duration:
        music = music.loop(duration=video.duration)
    
    # Combine audio tracks
    final_audio = video.audio.volumex(1.0).audio_fadeout(1)
    mixed_audio = CompositeAudioClip([final_audio, music])
    
    # Apply mixed audio to video
    final_video = video.set_audio(mixed_audio)
    final_video.write_videofile(
        output_path,
        fps=video.fps,
        codec="libx264",
        audio_codec="aac"
    )
    
    return output_path