from dotenv import load_dotenv
import os
import google.generativeai as genai
def model_config():
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")
    return model
