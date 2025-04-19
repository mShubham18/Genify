import streamlit as st
from components.model_configuration import model_config
from pipelines.video_generation_pipeline import generate_video_pipeline
from components.generate_response import generate_fact
from pipelines.upload_video_pipeline import upload_video_pipeline
import os
# Initialize the model
model = model_config()

# Page config
st.set_page_config(
    page_title="Genify - YouTube Scheduler",
    page_icon="🚀",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #1F1C2C, #928DAB);
            padding: 40px 20px;
            border-radius: 15px;
            color: white;
        }
        .stTextInput>div>div>input {
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
        }
        .stButton>button {
            border-radius: 10px;
            font-size: 16px;
            background-color: #4A90E2;
            color: white;
        }
        .stButton>button:hover {
            background-color: #3a78c2;
        }
    </style>
""", unsafe_allow_html=True)

# Container
with st.container():
    st.markdown("<div class='main'>", unsafe_allow_html=True)
    st.markdown("## 🚀 Genify - YouTube Video Scheduler")

    # Video title input
    video_title = st.text_input("🎬 Enter Video Title", placeholder="e.g. My Travel Vlog")
    domain = st.text_input("🌍 Enter Video Domain", placeholder="e.g. My Travel Vlog")
    
    # Schedule button
    if st.button("📤 Generate"):
        fact = generate_fact(video_title,domain)
        response = upload_video_pipeline(fact,domain)
        
        # Assuming the video is saved as 'generated_video.mp4' in the resource/output folder
        #video_path = os.path.join("resource", "output", "generated_video.mp4")
        video_path = "shorts/transcribed.mp4"
        # Check if the video exists
        if os.path.exists(video_path):
            st.success("Video generated successfully! Here it is:")
            # Display the video in the app
            st.video(video_path)
        else:
            st.error("Video generation failed. Please try again.")

    st.markdown("<br><p style='font-size:12px; color:lightgray;'>Genify will handle your video upload automatically. YouTube API integration required.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
