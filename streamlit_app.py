import streamlit as st
import pandas as pd
import datetime
import requests

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
            "humidity": data["main"]["humidity"]
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
    else:
        st.warning("Could not fetch weather data. Please check your API key or destination name.")

    # Travel Tips
    st.markdown("### 💡 Student Travel Tips")
    st.info("🎟️ Use your student ID for discounts on transport and museum entries.")
    st.info("🏨 Book accommodation early for better deals.")



