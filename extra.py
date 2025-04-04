import streamlit as st
from streamlit_lottie import st_lottie
import requests

# Function to load Lottie animation from URL
def load_lottie_url(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

# Load Lottie animation (replace URL with a working animation's URL)
lottie_animation_url = "https://lottie.host/5a0b66ba-5a69-4fec-b58b-f53e15dea1db/RcvHRDxn8N.json"
lottie_animation = load_lottie_url(lottie_animation_url)

# Verify that the animation was loaded
if lottie_animation is not None:
    st.title("Searching Animation Example")
    st_lottie(lottie_animation, height=300, key="search_animation")
else:
    st.error("Failed to load Lottie animation. Please check the URL.")
