from components.generate_response import generate_fact
from components.generate_images import ImageGeneration
from components.voice_over import generate_voice

from components.generate_video import create_final_video
from components.generate_subtitle import VideoTranscriber

from utils.utils import (
    PATH_BGM,
    PATH_VOICE_OVER,
    PATH_UNTRANSCRIBED,
    PATH_MODEL,
    PATH_TRANSCRIBED
)

"""
PATH_BGM = "Resources/bgm.mp3"
PATH_VOICE_OVER = "outputs/output.mp3"
PATH_UNTRANSCRIBED = "shorts/initial_video_untranscribed.mp4"
PATH_MODEL = "base"
PATH_TRANSCRIBED = "shorts/transcribed.mp4"
"""
def generate_video_pipeline(fact):
    generate_voice(fact,PATH_VOICE_OVER)

    img_object = ImageGeneration()

    keywords = img_object.generate_image(fact)
    images_list = img_object.get_duckduckgo_images(keywords)



    create_final_video(images_list,PATH_VOICE_OVER,PATH_BGM,PATH_UNTRANSCRIBED)


    transcriber = VideoTranscriber(PATH_MODEL,PATH_UNTRANSCRIBED)
    transcriber.extract_audio()
    transcriber.transcribe_video()
    transcriber.create_video(PATH_TRANSCRIBED)

    return fact



