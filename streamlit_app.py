import streamlit as st
import pandas as pd
import datetime
import requests
import folium
from streamlit_folium import folium_static

# === Page Configuration ===
st.set_page_config(page_title="Student Travel Planner", layout="centered")

# === Weather Fetching Function ===
def get_weather(destination, api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": destination,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        weather = {
            "description": data["weather"][0]["description"].title(),
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "lat": data["coord"]["lat"],
            "lon": data["coord"]["lon"]
        }
        return weather
    else:
        return None

# === Packing List Generator ===
def generate_packing_list(destination):
    general = ["🧥 Clothes", "🎧 Earphones", "🔌 Power bank", "🎫 Student ID"]
    beach_items = ["🩱 Swimsuit", "🧴 Sunscreen", "🕶 Sunglasses"]
    cold_items = ["🧤 Gloves", "🧣 Scarf", "🧥 Jacket"]

    if destination.lower() in ["langkawi", "pulau pinang", "penang"]:
        return general + beach_items
    elif destination.lower() in ["cameron highlands"]:
        return general + cold_items
    else:
        return general

# === Destination Coordinates (for maps) ===
DESTINATION_COORDS = {
    "Kuala Lumpur": (3.1390, 101.6869),
    "Penang": (5.4164, 100.3327),
    "Langkawi": (6.3500, 99.8000),
    "Cameron Highlands": (4.4693, 101.3773),
    "Singapore": (1.3521, 103.8198)
}

# === App UI ===
st.title("🎒 Student Travel Planner")
st.subheader("Plan your next student adventure easily!")

# === Inputs ===
destination = st.selectbox("🌍 Select Destination", [
    "Kuala Lumpur",
    "Penang",
    "Langkawi",
    "Cameron Highlands",
    "Singapore"
])
days = st.slider("📅 Number of Days", 1, 14, 3)
start_date = st.date_input("📆 Start Date", datetime.date.today())
budget = st.number_input("💸 Enter your total budget (MYR)", value=500)

# Enter your OpenWeatherMap API key here
api_key = "8447cc1e7a0d0d0d8ceef48fbf8ddee2"

# === Trip Planner ===
if st.button("✨ Generate Trip Plan"):
    end_date = start_date + datetime.timedelta(days=days - 1)
    daily_budget = budget / days

    # Trip Summary
    st.success("✅ Trip Summary")
    st.write(f"📍 **Destination**: {destination}")
    st.write(f"📅 **From**: {start_date.strftime('%b %d, %Y')} to {end_date.strftime('%b %d, %Y')}")
    st.write(f"💸 **Daily Budget**: RM {daily_budget:.2f}")

    # Packing List
    st.markdown("### 🧳 Packing List")
    for item in generate_packing_list(destination):
        st.write(f"- {item}")

    # Weather Info
    st.markdown("### 🌦️ Current Weather")
    weather = get_weather(destination, api_key)
    if weather:
        st.write(f"🌤 **Condition**: {weather['description']}")
        st.write(f"🌡️ **Temperature**: {weather['temperature']}°C (Feels like {weather['feels_like']}°C)")
        st.write(f"💧 **Humidity**: {weather['humidity']}%")
        
        # Display Map
        st.markdown("### 🗺️ Destination Map")
        if destination in DESTINATION_COORDS:
            lat, lon = DESTINATION_COORDS[destination]
        else:
            lat, lon = weather['lat'], weather['lon']
        
        m = folium.Map(location=[lat, lon], zoom_start=12)
        folium.Marker(
            [lat, lon],
            popup=destination,
            tooltip="Your destination"
        ).add_to(m)
        
        # Add some tourist spots for popular destinations
        if destination == "Kuala Lumpur":
            folium.Marker(
                [3.1580, 101.7118],
                popup="Petronas Twin Towers",
                icon=folium.Icon(color='blue', icon='camera')
            ).add_to(m)
            folium.Marker(
                [3.1390, 101.6869],
                popup="KL Tower",
                icon=folium.Icon(color='red', icon='camera')
            ).add_to(m)
        elif destination == "Penang":
            folium.Marker(
                [5.4149, 100.3298],
                popup="Penang Hill",
                icon=folium.Icon(color='green', icon='camera')
            ).add_to(m)
            folium.Marker(
                [5.4205, 100.3382],
                popup="Kek Lok Si Temple",
                icon=folium.Icon(color='orange', icon='camera')
            ).add_to(m)
        
        folium_static(m, width=700, height=400)
    else:
        st.warning("Could not fetch weather data. Please check your API key or destination name.")

    # Travel Tips
    st.markdown("### 💡 Student Travel Tips")
    st.info("🎟️ Use your student ID for discounts on transport and museum entries.")
    st.info("🏨 Book accommodation early for better deals.")
    st.info("🗺️ Check the map above for key attractions in your destination.")
    

