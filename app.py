from pipelines.upload_video_pipeline import upload_video_pipeline
from utils.utils import PATH_TRANSCRIBED,PATH_UNTRANSCRIBED,PATH_VOICE_OVER
import os

if __name__=="__main__":
    #Calling the entire pipeline
    try:
        final_message = upload_video_pipeline()
        if final_message:
            print(str(final_message))
            
            """residual_files = [PATH_VOICE_OVER,PATH_TRANSCRIBED,PATH_UNTRANSCRIBED]
            for path in residual_files:
                os.remove(path)
                """
    except Exception as e:
        print(f"An error Ocurred: {e}")