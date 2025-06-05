import streamlit as st
import pandas as pd
import datetime
import requests

st.set_page_config(page_title="Student Travel Planner", layout="centered")

# === Supabase (mock) ===
SAVE_TO_DATABASE = False  # Toggle True if Supabase is configured

# === Google Maps ===
def show_map(destination):
    base_url = "https://www.google.com/maps/embed/v1/place"
    api_key = "YOUR_GOOGLE_MAPS_API_KEY"  # Replace with your key
    return f"{base_url}?key={api_key}&q={destination}"

# === Packing List ===
def generate_packing_list(destination):
    general = ["🧥 Clothes", "🎧 Earphones", "🔌 Power bank", "🎫 Student ID"]
    beach_items = ["🩱 Swimsuit", "🧴 Sunscreen", "🕶 Sunglasses"]
    cold_items = ["🧤 Gloves", "🧣 Scarf", "🧥 Jacket"]

    if destination.lower() in ["langkawi", "pulau pinang"]:
        return general + beach_items
    elif destination.lower() in ["cameron highlands"]:
        return general + cold_items
    else:
        return general

# === Mapping Destinations ===
destination_mapping = {
    "Kuala Lumpur": "Kuala Lumpur",
    "Penang": "Pulau Pinang",  # official name in API
    "Pulau Pinang": "Pulau Pinang",
    "Langkawi": "Langkawi",
    "Cameron Highlands": "Cameron Highlands",  # might not be in API
    "Singapore": None  # not supported in MY API
}

# === Get Weather from data.gov.my ===
def get_malaysia_weather_forecast(api_area_name):
    if not api_area_name:
        return None  # outside Malaysia or unsupported area

    try:
        response = requests.get("https://api.data.gov.my/weather/forecast")
        if response.status_code == 200:
            data = response.json()
            for entry in data:
                if api_area_name.lower() == entry["area"].lower():
                    return entry
        else:
            st.error(f"❌ Gagal dapatkan data cuaca. Kod status: {response.status_code}")
    except Exception as e:
        st.error(f"⚠️ Ralat semasa akses API cuaca: {e}")
    return None

# === UI Starts ===
st.title("🎒 Student Travel Planner")
st.subheader("Plan your next student adventure easily!")

# UI Input
destination = st.selectbox("🌍 Select Destination", [
    "Kuala Lumpur", 
    "Penang", 
    "Langkawi", 
    "Cameron Highlands", 
    "singapore"
])
days = st.slider("📅 Number of Days", 1, 14, 3)
start_date = st.date_input("📆 Start Date", datetime.date.today())
budget = st.number_input("💸 Enter your total budget (MYR)", value=500)

# Map Display
with st.expander("📍 Show Map"):
    if "YOUR_GOOGLE_MAPS_API_KEY" in show_map(destination):
        st.warning("🔑 Add your Google Maps API key to see the embedded map.")
    else:
        st.components.v1.iframe(show_map(destination), height=400)

# Generate Trip
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

    st.markdown("### 🌦️ Weather Forecast")

    api_area = destination_mapping.get(destination)
    forecast = get_malaysia_weather_forecast(api_area)

    if destination == "Singapore":
        st.warning("⚠️ Cuaca untuk Singapore tidak disokong oleh API rasmi Malaysia.")
    elif forecast:
        st.info(f"📍 Lokasi: {forecast['area']}")
        st.write(f"📅 Tarikh Ramalan: {forecast['forecast_date']}")
        for item in forecast['forecast']:
            st.write(f"- {item['day']} ({item['date']}): **{item['forecast']}**")
    else:
        st.warning("⚠️ Ramalan cuaca tidak tersedia untuk lokasi ini atau luar tempoh 3 hari.")

    st.markdown("### 💡 Student Travel Tips")
    st.info("Gunakan kad pelajar untuk diskaun pengangkutan dan muzium.")
    st.info("Tempah penginapan awal untuk harga terbaik!")

    if SAVE_TO_DATABASE:
        st.write("🛠 Menyimpan pelan ke pangkalan data... (Simulasi)")



