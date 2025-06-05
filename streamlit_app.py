import streamlit as st
import pandas as pd
import datetime
import requests

st.set_page_config(page_title="Student Travel Planner", layout="centered")

SAVE_TO_DATABASE = False  # Optional feature

# Meteoblue API
def get_weather_forecast(lat, lon):
    api_key = "eCxmdVKbkipLMnzR"  # Replace with your Meteoblue API key
    url = f"https://my.meteoblue.com/packages/basic-1h_basic-day?apikey={api_key}&lat={lat}&lon={lon}&asl=53&format=json"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None

# Location coordinates for destinations
location_coords = {
    "Kuala Lumpur": (3.139, 101.6869),
    "Langkawi": (6.35, 99.8),
    "Penang": (5.4164, 100.3327),
    "Singapore": (1.3521, 103.8198),
    "Cameron Highlands": (4.4711, 101.3766)
}

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

# UI
st.title("🎒 Student Travel Planner")
st.subheader("Plan your next student adventure easily!")

destination = st.selectbox("🌍 Select Destination", list(location_coords.keys()))
days = st.slider("📅 Number of Days", 1, 14, 3)
start_date = st.date_input("📆 Start Date", datetime.date.today())
budget = st.number_input("💸 Enter your total budget (MYR)", value=500)

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

    # Weather Forecast
    st.markdown("### 🌦️ Weather Forecast")
    lat, lon = location_coords[destination]
    weather_data = get_weather_forecast(lat, lon)

    if weather_data:
        daily = weather_data.get("daily", {})
        dates = daily.get("time", [])
        temps = daily.get("temperature_max", [])

        if dates and temps:
            df_weather = pd.DataFrame({
                "Date": dates,
                "Max Temp (°C)": temps
            })
            df_weather["Date"] = pd.to_datetime(df_weather["Date"])
            df_trip = df_weather[(df_weather["Date"] >= pd.to_datetime(start_date)) & 
                                 (df_weather["Date"] <= pd.to_datetime(end_date))]

            st.dataframe(df_trip.set_index("Date"))
        else:
            st.warning("⚠️ Weather data not available for this period.")
    else:
        st.error("❌ Failed to retrieve weather data.")

    st.markdown("### 💡 Student Travel Tips")
    st.info("Use student ID for travel & museum discounts!")
    st.info("Book accommodations early for cheaper rates!")

    if SAVE_TO_DATABASE:
        st.write("🛠 Saving trip to database... (Simulated)")


