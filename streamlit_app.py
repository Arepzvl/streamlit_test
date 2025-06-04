import streamlit as st
import requests

# 🌆 Inject background image
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

# 🏋️‍♂️ FitTrackU Title
st.title("🏋️ FitTrackU – Exercise Finder")

st.markdown("Welcome to FitTrackU! Find the best workouts for your fitness journey.")

# ✅ Choose body part
body_parts = ['abs', 'back', 'biceps', 'cardio', 'chest', 'legs', 'shoulders']
selected_part = st.selectbox("Select body part to train:", body_parts)

# 🔌 Setup API (ExerciseDB via RapidAPI)
import requests

muscle = 'biceps'
api_url = 'https://api.api-ninjas.com/v1/exercises?muscle={}'.format(muscle)
response = requests.get(api_url, headers={'X-Api-Key': 'YOUR_API_KEY'})
if response.status_code == requests.codes.ok:
    print(response.text)
else:
    print("Error:", response.status_code, response.text)

}

# 🧠 Fetch data from API
@st.cache_data
def fetch_exercises():
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to fetch data from API.")
            return []
    except Exception as e:
        st.error(f"Error occurred: {e}")
        return []

# 📋 Display exercises
data = fetch_exercises()
if data:
    st.markdown(f"### Showing exercises for **{selected_part.capitalize()}**:")
    for exercise in data[:10]:  # Limit to 10 items
        st.markdown(f"#### {exercise['name'].capitalize()}")
        st.image(exercise['gifUrl'], width=300)
        st.write(f"**Target Muscle:** {exercise['target'].capitalize()}")
        st.write(f"**Equipment:** {exercise['equipment'].capitalize()}")
        st.markdown("---")

# Footer
st.markdown("<br><hr><center>Made for University Project – FitTrackU 💪</center>", unsafe_allow_html=True)
