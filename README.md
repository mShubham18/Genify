# Automated Shinobi

## Overview
Automated Shinobi is a fully automated pipeline that generates short YouTube videos featuring rare and interesting facts about Anime like *Naruto*, *Bleach*, and *Attack on Titan*. The project is built entirely using Python with a modular coding approach.

## Features
- **Fact Generation**: Uses the Gemini API to generate rare and interesting facts about the selected anime series.
- **AI Voiceovers**: Converts the generated fact into speech using the Speechify API.
- **Image Fetching**: Uses the DuckDuckGo API to retrieve relevant images based on the generated fact.
- **Video Compilation**: Leverages the MoviePy module to merge the background music (BGM), images, and AI-generated voiceovers into a short video with animations.
- **Subtitle Generation**: Uses OpenAI's Whisper module to create subtitles based on the generated voiceover.
- **Metadata Generation**: Gemini API is used again to generate an appropriate title, description, and tags for the video.
- **YouTube Upload**: Utilizes the YouTube API to upload the generated video along with the metadata.
- **Automation (Optional)**: The workflow can be automated using GitHub Actions, but the script can also be executed manually.

## Dependencies
The project requires the following dependencies, specified in `requirements.txt`:
```
numpy
pandas
google-generativeai
python-dotenv  # For managing environment variables
duckduckgo_search
openai-whisper
opencv-python-headless  # Optimized for servers (instead of opencv-python)
moviepy==1.0.3
tqdm
Pillow  # Correct package name for PIL
google-auth
google-auth-oauthlib
google-auth-httplib2
google-api-python-client
imageio[ffmpeg]  # Ensures ffmpeg support for MoviePy
```

## Setting Up Environment Variables
Before running the project, create a `.env` file in the root directory and paste the following:

```
GEMINI_API_KEY=your_actual_gemini_api_key
SPEECHIFY_API_KEY=your_actual_speechify_api_key
API_URL=your_actual_api_url
MIN_IMAGES=20

GOOGLE_API_KEY=your_actual_google_api_key
GOOGLE_CSE_ID=your_actual_google_cse_id

YT_CLIENT_ID=your_actual_yt_client_id
YT_CLIENT_SECRET=your_actual_yt_client_secret
YT_PROJECT_ID=your_actual_yt_project_id
YT_AUTH_URI=your_actual_yt_auth_uri
YT_TOKEN_URI=your_actual_yt_token_uri
YT_REDIRECT_URI=your_actual_yt_redirect_uri
YT_REFRESH_TOKEN=your_actual_yt_refresh_token
```

Make sure to replace `your_actual_*` values with your real API keys. The `.env` file is used to store sensitive information securely and should **not** be committed to version control. You can add `.env` to your `.gitignore` file to prevent accidental commits.

## How It Works
1. **Fact Generation**: The script fetches a random interesting fact using the Gemini API.
2. **Voiceover Creation**: Converts the text into speech using the Speechify API.
3. **Image Fetching**: Searches for relevant images using the DuckDuckGo API.
4. **Video Compilation**: Combines images, BGM, and the voiceover into an animated video.
5. **Subtitle Generation**: Generates subtitles based on the voiceover.
6. **Metadata Creation**: Creates a title, description, and tags using Gemini.
7. **YouTube Upload**: Uploads the video using the YouTube API.
8. **Execution**: The process can be run manually using `python app.py`.

## Flow chart

<p align="center">
  <img src="Elements/Flowchart.png" alt="Flowchart" width="500"/>
</p>

## Running the Project Locally
To run the script manually on your local machine:
1. Clone the repository.
2. Set up API keys and environment variables in a `.env` file.
3. Install dependencies using `pip install -r requirements.txt`.
4. Run the script with `python app.py`.

## Deployment & Automation (Optional)
- If you wish to automate the process, configure GitHub Actions (`automation.yml`) to trigger the process on a schedule.
- Push the project to GitHub and enable Actions to start automation.

Contributions are welcome! Feel free to fork the repository, create a new branch, and submit a pull request with improvements or new features. 🙌🏻

Happy Coding !