import streamlit as st
import pandas as pd
import datetime
import requests

st.set_page_config(page_title="Student Travel Planner", layout="centered")

# Supabase - Optional config (mocked here)
SAVE_TO_DATABASE = False  # Toggle True if Supabase is configured

# Google Maps Embed function
def show_map(destination):
    base_url = "https://www.google.com/maps/embed/v1/place"
    api_key = "YOUR_GOOGLE_MAPS_API_KEY"  # Replace with your key
    return f"{base_url}?key={api_key}&q={destination}"

# Packing list generator
def generate_packing_list(destination):
    general = ["🧥 Clothes", "🎧 Earphones", "🔌 Power bank", "🎫 Student ID"]
    beach_items = ["🩱 Swimsuit", "🧴 Sunscreen", "🕶 Sunglasses"]
    cold_items = ["🧤 Gloves", "🧣 Scarf", "🧥 Jacket"]

    if destination.lower() in ["langkawi", "penang"]:
        return general + beach_items
    elif destination.lower() in ["cameron highlands"]:
        return general + cold_items
    else:
        return general

# Weather forecast from Malaysia government API
def get_malaysia_weather_forecast(destination):
    try:
        response = requests.get("https://api.data.gov.my/weather/forecast?contains=<prefix>@location__location_id")
        if response.status_code == 200:
            data = response.json()
            for entry in data:
                if destination.lower() in entry["area"].lower():
                    return entry
        else:
            st.error(f"❌ Failed to fetch weather data. Status: {response.status_code}")
    except Exception as e:
        st.error(f"⚠️ Error fetching weather data: {e}")
    return None

# UI
st.title("🎒 Student Travel Planner")
st.subheader("Plan your next student adventure easily!")

destination = st.selectbox("🌍 Select Destination", ["Kuala Lumpur", "Langkawi", "Penang", "Singapore", "Cameron Highlands"])
days = st.slider("📅 Number of Days", 1, 14, 3)
start_date = st.date_input("📆 Start Date", datetime.date.today())
budget = st.number_input("💸 Enter your total budget (MYR)", value=500)

# Google Maps iframe
with st.expander("📍 Show Map"):
    if "YOUR_GOOGLE_MAPS_API_KEY" in show_map(destination):
        st.warning("🔑 Add your Google Maps API key to see the embedded map.")
    else:
        st.components.v1.iframe(show_map(destination), height=400)

# Button
if st.button("✨ Generate Trip Plan"):
    daily_budget = budget / days
    end_date = start_date + datetime.timedelta(days=days - 1)

    st.success("✅ Trip Summary")
    st.write(f"📍 *Destination*: {destination}")
    st.write(f"📅 *From*: {start_date.strftime('%b %d, %Y')} to {end_date.strftime('%b %d, %Y')}")
    st.write(f"💸 *Daily Budget*: RM {daily_budget:.2f}")

    st.markdown("### 🧳 Packing List")
    for item in generate_packing_list(destination):
        st.write(f"- {item}")

    st.markdown("### 🌦️ Weather Forecast (Malaysia Gov API)")
    if destination.lower() not in ["kuala lumpur", "langkawi", "penang", "cameron highlands"]:
        st.warning("⚠️ Weather forecast is only available for locations in Malaysia.")
    else:
        forecast = get_malaysia_weather_forecast(destination)
        if forecast:
            st.write(f"📍 **Area**: {forecast['area']}")
            st.write(f"🗓️ **Forecast Date**: {forecast['forecast_date']}")
            for item in forecast['forecast']:
                st.write(f"- {item['day']} ({item['date']}): **{item['forecast']}**")
        else:
            st.warning("⚠️ Weather forecast not available for this location.")

    st.markdown("### 💡 Student Travel Tips")
    st.info("Use student ID for travel & museum discounts!")
    st.info("Book accommodations early for cheaper rates!")

    # Optional: Save to Supabase (mocked)
    if SAVE_TO_DATABASE:
        st.write("🛠 Saving trip to database... (Simulated)")



