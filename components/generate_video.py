import os
import tempfile
import cv2
import numpy as np
import streamlit as st
from PIL import Image
import imageio_ffmpeg

# ✅ Ensure FFmpeg is available to moviepy and whisper
ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path
os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)

# ✅ MoviePy imports
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.fx import all as vfx
from moviepy.audio.fx.all import volumex

# ✅ Function to process images and apply zoom-out effect
def process_images(image_list, voiceover_duration, max_duration_per_image=4):
    num_images = min(len(image_list), int(voiceover_duration / max_duration_per_image))
    selected_images = image_list[:num_images]

    clips = []
    temp_files = []

    for img in selected_images:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        img.save(temp_file, format="JPEG")
        temp_file.close()
        temp_files.append(temp_file.name)

        cv_img = cv2.imread(temp_file.name)
        if cv_img is None:
            continue

        clip = (
            ImageClip(temp_file.name)
            .set_duration(max_duration_per_image)
            .fx(vfx.resize, lambda t: 1 + 0.05 * t)
        )

        clips.append(clip)

    return clips

# ✅ Function to mix voiceover and background music
def process_audio(voiceover_path, bgm_path):
    voiceover = AudioFileClip(voiceover_path)
    bgm = AudioFileClip(bgm_path).subclip(0, voiceover.duration).fx(volumex, 0.4)
    final_audio = CompositeAudioClip([voiceover, bgm])
    return final_audio

# ✅ Final video creation function
def create_final_video(images, voiceover_path, bgm_path, output_path="shorts/final_video.mp4"):
    voiceover = AudioFileClip(voiceover_path)
    clips = process_images(images, voiceover.duration)
    video = concatenate_videoclips(clips, method="compose")
    video = video.set_audio(process_audio(voiceover_path, bgm_path))

    os.makedirs("shorts", exist_ok=True)
    video.write_videofile(output_path, fps=24, codec="libx264")