# emergency_video.py
"""
Emergency video creation without moviepy dependency
"""
import os
import subprocess
from PIL import Image

def create_video_simple(images, audio_path, output_path, duration_per_slide=5):
    """
    Create video using FFmpeg directly (no moviepy required)
    """
    try:
        # Create a temporary file listing images
        with open("image_list.txt", "w") as f:
            for img in images:
                f.write(f"file '{os.path.abspath(img)}'\n")
                f.write(f"duration {duration_per_slide}\n")
        
        # Use FFmpeg to create video
        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-i', 'image_list.txt',
            '-i', audio_path,
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-pix_fmt', 'yuv420p',
            '-shortest',
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Cleanup
        if os.path.exists("image_list.txt"):
            os.remove("image_list.txt")
            
        if result.returncode == 0:
            return output_path
        else:
            raise Exception(f"FFmpeg failed: {result.stderr}")
            
    except Exception as e:
        print(f"Video creation fallback also failed: {e}")
        return create_static_video(images, output_path)

def create_static_video(images, output_path, duration=30):
    """
    Ultimate fallback: Create a simple slideshow using first image
    """
    try:
        if images:
            # Use first image for entire video
            img = images[0]
            cmd = [
                'ffmpeg',
                '-loop', '1',
                '-i', img,
                '-c:v', 'libx264',
                '-t', str(duration),
                '-pix_fmt', 'yuv420p',
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                return output_path
    except:
        pass
    
    return None

def check_ffmpeg():
    """Check if FFmpeg is available"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False