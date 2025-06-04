import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Baca fail .env untuk API key

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Background dan style baru untuk travel
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1950&q=80");
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

st.title("✈️ TravelPlanner – Weather & Trip Helper")
st.write("Plan your trips by checking current weather in any city!")

city = st.text_input("Enter a city name:", "Kuala Lumpur")

if st.button("Get Weather"):
    if city:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            st.subheader(f"Weather in {city.capitalize()}:")
            st.write(f"Temperature: {data['main']['temp']} °C")
            st.write(f"Weather: {data['weather'][0]['description'].capitalize()}")
            st.write(f"Humidity: {data['main']['humidity']}%")
            st.write(f"Wind Speed: {data['wind']['speed']} m/s")
        else:
            st.error("❌ City not found or API error. Please try another city.")
    else:
        st.warning("⚠️ Please enter a city name.")

st.markdown("<br><hr><center>🌏 TravelPlanner – University Project</center>", unsafe_allow_html=True)


