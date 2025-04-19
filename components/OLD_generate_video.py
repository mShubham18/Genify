from PIL import Image
import os

import tempfile
import cv2
import numpy as np
#from moviepy.editor import ImageClip
#os.environ["IMAGEMAGICK_BINARY"] = "/usr/bin/magick"

from moviepy.config import change_settings
import os

# Auto-detect ImageMagick path
change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/magick"})

from moviepy import *



from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.fx import all as vfx
from moviepy.audio.fx.all import volumex

"""from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})
"""

"""def load_images(folder="downloaded_images"):
    image_files = sorted(os.listdir(folder))  # Sort to maintain order
    loaded_images = [Image.open(os.path.join(folder, img)) for img in image_files]

    print(f"Loaded {len(loaded_images)} images")
    return loaded_images  # Returns a list of PIL objects


# Test loading images
loaded_images = load_images()
img_list = loaded_images
"""


def process_images(image_list, voiceover_duration, max_duration_per_image=4):
    """
    Selects images to fit the duration of the voiceover and applies zoom-out effect.
    Handles PIL images by saving them as temporary files.
    """
    num_images = min(len(image_list), int(voiceover_duration / max_duration_per_image))
    selected_images = image_list[:num_images]

    clips = []
    temp_files = []

    for img_index, img in enumerate(selected_images):
        # ✅ Convert PIL Image to a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        img.save(temp_file, format="JPEG")
        temp_file.close()  # Close file to allow other programs to access it
        temp_files.append(temp_file.name)

        # ✅ Open the saved image with OpenCV to avoid errors
        cv_img = cv2.imread(temp_file.name)
        if cv_img is None:
            print(f"Error: Unable to read {temp_file.name}")
            continue

        # ✅ Apply a zoom-out effect (slight scale change)
        #clip = ImageClip(temp_file.name).set_duration(max_duration_per_image).resize(lambda t: 1 + 0.05 * t)

        clip = (
            ImageClip(temp_file.name)
            .set_duration(max_duration_per_image)
            .fx(vfx.resize, lambda t: 1 + 0.05 * t)  # Apply dynamic resizing
            )
        

        clips.append(clip)

    return clips


#from moviepy.editor import AudioFileClip, CompositeAudioClip


def process_audio(voiceover_path, bgm_path):
    """
    Load the voiceover and background music and mix them properly.
    """
    voiceover = AudioFileClip(voiceover_path)
    #bgm = AudioFileClip(bgm_path).subclip(0, voiceover.duration).volumex(0.4)  # Reduce BGM volume
    bgm = AudioFileClip(bgm_path).subclip(0, voiceover.duration).fx(volumex, 0.4)

    final_audio = CompositeAudioClip([voiceover, bgm])
    return final_audio


#from moviepy.editor import concatenate_videoclips, CompositeVideoClip
#from moviepy.editor import AudioFileClip, CompositeAudioClip


def create_final_video(images, voiceover_path, bgm_path, output_path="shorts/final_video.mp4"):
    """
    Combines images, voiceover, and background music into a final video.
    """
    voiceover = AudioFileClip(voiceover_path)
    clips = process_images(images, voiceover.duration)

    # Concatenate video clips
    video = concatenate_videoclips(clips, method="compose")
    video = video.set_audio(process_audio(voiceover_path, bgm_path))

    # Save output
    os.makedirs("shorts", exist_ok=True)
    video.write_videofile(output_path, fps=24, codec="libx264")


# Run the final video generation
#create_final_video(images=img_list, voiceover_path="outputs/output.mp3", bgm_path="Resources/bgm.mp3")
