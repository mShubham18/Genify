from components.generate_response import generate_fact
import requests
import os
from dotenv import load_dotenv
load_dotenv()
# Your Speechify API Key
API_KEY = os.getenv("SPEECHIFY_API_KEY")

# Speechify API Endpoint
API_URL = os.getenv("API_URL")
import requests
import base64
import html


api_key = API_KEY

api_url = "https://api.sws.speechify.com/v1/audio/speech"


response_str = "Remember when Aizen was all about transcending? Did you know that in the light novels, it's revealed that his ultimate goal wasn't just power, but to create a key, a king's key capable of opening the gates to the Royal Realm without needing the ritual involving the souls of one hundred thousand people from Rukongai. In other words, Aizen wanted to dethrone the Soul King not for absolute power, but to change the very system. He wanted to find a different way to open the realm. This ambition, shrouded in his twisted methods, makes Aizen less of a power-hungry villain and more of a revolutionary, albeit a deeply flawed and dangerous one."
#response_str = html.escape(response_str)  # Escape special characters
def generate_voice(fact,path):

    

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    

    ssml_text = f"""<speak>
        <speechify:style emotion="terrified">
            {fact}
        </speechify:style>
    </speak>"""

    data = {
    "input": ssml_text,
    "voice_id": "donald",  # Ensure "henry" is a valid voice ID
    }

    response = requests.post(api_url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        response_json = response.json()
        if "audio_data" in response_json:
            # Decode base64 audio data
            audio_mp3 = base64.b64decode(response_json["audio_data"])
            # Save the audio content to a file
            #return audio_mp3

            with open(path, "wb") as audio_file:
                audio_file.write(audio_mp3)
        else:
            print("Error: 'audio_data' not found in the response.")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

