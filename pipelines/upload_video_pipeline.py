from pipelines.video_generation_pipeline import generate_video_pipeline
from components.upload_to_youtube import upload_video

from components.model_configuration import model_config
from utils.utils import PATH_TRANSCRIBED

def upload_video_pipeline(fact):
    generated_fact=generate_video_pipeline(fact)
    model = model_config()

    prompt = f"""Here is a fact : {generated_fact},this is a script of a youtube short., generate me some title starting with did you know, description with some #tags, and tags for the same. provide them comma seperated one by one. do not write anything else like salutation or something
    NOTE:
    keep the title short, and give it in this way
    here :
    TItle: did you know this about mayank ?
    description: mayank is a person who like cats and this short explains why
    tags: mayank,cats,loves,
    so the output should be:
    here / seperates them

    did you know this about mayank ?/mayank is a person who like cats and this short explains why/mayank,cats,loves
    do not include headings like title, tags, description, just straigh forward the output
    """

    response=model.generate_content(prompt)
    output=response.text
    output_list=(output.replace("\n","")).split("/")
    video_title = output_list[0]
    video_description = output_list[1]
    video_tags = output_list[2]
    video_tags= video_tags.split(",")


    upload_video(
        video_path=PATH_TRANSCRIBED,
        title=video_title,
        description=video_description,
        tags=video_tags
    )
    message=print("Wohoo! Video just got uploaded !")
    return message

#upload_video_pipeline()

