import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Ini akan baca fail .env secara automatik

API_KEY = os.getenv("RAPIDAPI_KEY")


# 🌆 Inject background image & style
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1583454110551-21f2fa2f7ed3?auto=format&fit=crop&w=1950&q=80");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .block-container {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🏋️‍♂️ Title
st.title("🏋️ FitTrackU – Exercise Finder")
st.write("Welcome to FitTrackU! Search exercises by body part.")

# 🔌 API Headers
headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "exercisedb.p.rapidapi.com"
}

# 🧠 Fetch available body parts
@st.cache_data
def get_body_parts():
    url = "https://exercisedb.p.rapidapi.com/exercises/bodyPartList"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("❌ Failed to load body parts.")
        return []

# 📥 Fetch exercises by body part
@st.cache_data
def fetch_exercises(part):
    url = f"https://exercisedb.p.rapidapi.com/exercises/bodyPart/{part.lower()}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"❌ Failed to fetch data: {response.status_code}")
        st.text(response.text)
        return []

# 🔽 Body part dropdown
body_parts = get_body_parts()
if body_parts:
    selected_part = st.selectbox("Select body part:", body_parts)
    data = fetch_exercises(selected_part)

    if data:
        st.subheader(f"Showing exercises for **{selected_part.capitalize()}**:")
        for ex in data[:10]:  # Limit to 10 results
            st.markdown(f"### {ex['name'].capitalize()}")
            st.image(ex['gifUrl'], width=300)
            st.write(f"**Target:** {ex['target'].capitalize()}")
            st.write(f"**Equipment:** {ex['equipment'].capitalize()}")
            st.markdown("---")

# Footer
st.markdown("<br><hr><center>💪 FitTrackU – Built for University Project</center>", unsafe_allow_html=True)


