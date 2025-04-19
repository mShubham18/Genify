from dotenv import load_dotenv
import os
import google.generativeai as genai
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
#‘[Back Propagation]’
#‘[Data Science]’
def generate_fact(title,domain):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")
    #prompt = "Generate me a rare, amazing, and mind-blowing fact from Bleach, Naruto, or Attack on Titan. The fact should not be common knowledge and must come from deep sources like light novels, manga, databooks, interviews, or supplementary materials that weren’t fully adapted into the anime. Rotate between different characters, including major and side characters, ensuring variety instead of focusing on just one or two. Keep the language simple yet engaging. The fact should be between 80 to 110 words. Use phrases like 'Did you know' or 'Remember when' to make it catchy and hook the audience instantly. Start right away without greetings or filler phrases. Merge the fact and the script into one seamless flow rather than separating them. Adapt names phonetically for accurate AI TTS pronunciation (e.g., Yhwach → Yuhabaha). Maintain a calm, mysterious, and to-the-point tone."
    prompt = f"""Write a short, engaging script about ‘[{title}]’ in the domain of ‘[{domain}]’.
    The script should be under [50] words. Begin with a hook that grabs attention and is easy to understand for a broad audience.
    Keep technical jargon to a minimum, and end with a subtle invitation for viewers to learn more,
    encouraging them to check the description for details about the creator and any related course."""
    response = model.generate_content(prompt)
    return response.text
