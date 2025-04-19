import io
import requests  # Use requests instead of urllib
from duckduckgo_search import DDGS
from PIL import Image
from components.model_configuration import model_config
import os
from dotenv import load_dotenv
load_dotenv()
MIN_IMAGES = int(os.getenv("MIN_IMAGES","5"))

class ImageGeneration:
    def __init__(self):
        self.model = model_config()

    def generate_image(self, excerpt):
        prompt = f"""Consider this excerpt: {excerpt}
        Retrieve the list of keywords that I could feed into DuckDuckGo search API to get clean mobile-sized photos regarding the excerpt.
        Just a single line with comma-separated values.
        Modify the keywords such that it only fetches mobile-sized images. Like modifying the output words, such as output + "mobile wallpaper".
        For example, if the list has "Eiffel Tower", return "Eiffel Tower mobile wallpaper".

        I only want the response, I do not need any salutation.
        """
        keywords = self.model.generate_content(prompt)
        keywords_string=str(keywords.text)
        keywords_string = keywords_string.replace(",","")
        keywords_string=keywords_string.replace("\n","")

        return keywords_string

    def get_duckduckgo_images(self, query, num_images=30):
        image_list = []
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/91.0.4472.124 Safari/537.36"
        }

        with DDGS() as ddgs:
            results = ddgs.images(query, max_results=num_images)

        valid_images = 0
        for i, img in enumerate(results):
            if valid_images >= MIN_IMAGES:
                break
            try:
                image_url = img["image"]
                
                # ✅ Request with headers to avoid 403 errors
                response = requests.get(image_url, headers=headers, stream=True)
                response.raise_for_status()  # Raise error if request fails

                # Read image from response
                image = Image.open(io.BytesIO(response.content))

                # Convert to 9:16 with padding
                image = self.convert_to_9_16_with_padding(image)

                image_list.append(image)
                valid_images += 1
                print(f"Processed Image {valid_images}: {image_url} (Size: {image.size})")

            except requests.exceptions.RequestException as e:
                print(f"Skipping {image_url}: {e}")
            except Exception as e:
                print(f"Error processing {image_url}: {e}")

        return image_list

    def convert_to_9_16_with_padding(self, image, target_width=1080, target_height=1920):
        """ Convert image to 9:16 aspect ratio using padding instead of cropping """
        width, height = image.size
        target_aspect = 9 / 16
        image_aspect = width / height

        if image_aspect > target_aspect:
            new_height = int(width / target_aspect)
            padded_image = Image.new("RGB", (width, new_height), (0, 0, 0))  # Black background
            padded_image.paste(image, (0, (new_height - height) // 2))
        else:
            new_width = int(height * target_aspect)
            padded_image = Image.new("RGB", (new_width, height), (0, 0, 0))  # Black background
            padded_image.paste(image, ((new_width - width) // 2, 0))

        final_image = padded_image.resize((target_width, target_height), Image.LANCZOS)
        return final_image


# Example Usage
"""obj = ImageGeneration()
query = "Bleach Aizen Soul King Royal Realm"
excerpt = "Remember when Aizen was all about transcending? Did you know that in the light novels, it's revealed that his ultimate goal wasn't just power, but to create a key, a king's key capable of opening the gates to the Royal Realm without needing the ritual involving the souls of one hundred thousand people from Rukongai. In other words, Aizen wanted to dethrone the Soul King not for absolute power, but to change the very system. He wanted to find a different way to open the realm."

keywords = obj.generate_image(excerpt)
mobile_images = obj.get_duckduckgo_images(keywords, num_images=20)
print(f"Total Processed Images: {len(mobile_images)}")"""
