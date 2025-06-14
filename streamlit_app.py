import streamlit as st
import pandas as pd
import datetime
import requests
from datetime import timedelta

# === Page Configuration ===
st.set_page_config(page_title="Student Travel Planner", layout="centered")

# === Weather API Configuration ===
# (You'll need to sign up for a free API key at https://openweathermap.org/)
  # Replace with your actual API key
BASE_URL = "https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={time}&appid={8447cc1e7a0d0d0d8ceef48fbf8ddee2}"

# === Packing List Generator ===
def generate_packing_list(destination, weather_data=None):
    general = ["🧥 Clothes", "🎧 Earphones", "🔌 Power bank", "🎫 Student ID"]
    beach_items = ["🩱 Swimsuit", "🧴 Sunscreen", "🕶 Sunglasses"]
    cold_items = ["🧤 Gloves", "🧣 Scarf", "🧥 Jacket"]
    rain_items = ["☔ Umbrella", "🌧️ Raincoat", "👢 Waterproof shoes"]
    
    # Default packing list based on destination
    if destination.lower() in ["langkawi", "pulau pinang", "penang"]:
        packing_list = general + beach_items
    elif destination.lower() in ["cameron highlands"]:
        packing_list = general + cold_items
    else:
        packing_list = general
    
    # Enhance with weather data if available
    if weather_data:
        avg_temp = sum([day['temp'] for day in weather_data]) / len(weather_data)
        rainy_days = sum([1 for day in weather_data if day['weather'] == 'Rain'])
        
        if avg_temp < 15:
            packing_list.extend(cold_items)
        if rainy_days > 0:
            packing_list.extend(rain_items)
    
    return list(set(packing_list))  # Remove duplicates

# === Get Weather Forecast ===
def get_weather_forecast(destination, start_date, days):
    # Map destinations to city IDs or coordinates
    city_mapping = {
        "Kuala Lumpur": {"q": "Kuala Lumpur, MY"},
        "Penang": {"q": "Penang, MY"},
        "Langkawi": {"q": "Langkawi, MY"},
        "Cameron Highlands": {"q": "Cameron Highlands, MY"},
        "Singapore": {"q": "Singapore, SG"}
    }
    
    if destination not in city_mapping:
        return None
    
    params = {
        **city_mapping[destination],
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Process forecast data for the trip duration
        weather_forecast = []
        for i in range(days):
            forecast_date = start_date + timedelta(days=i)
            date_str = forecast_date.strftime('%Y-%m-%d')
            
            # Find forecasts for this date
            daily_forecasts = [item for item in data['list'] 
                             if item['dt_txt'].startswith(date_str)]
            
            if daily_forecasts:
                # Get average temp and most common weather condition for the day
                temps = [f['main']['temp'] for f in daily_forecasts]
                weathers = [f['weather'][0]['main'] for f in daily_forecasts]
                
                weather_forecast.append({
                    'date': forecast_date,
                    'temp': sum(temps)/len(temps),
                    'weather': max(set(weathers), key=weathers.count)
                })
        
        return weather_forecast
    except Exception as e:
        st.warning(f"Couldn't fetch weather data: {str(e)}")
        return None

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

# === Trip Planner ===
if st.button("✨ Generate Trip Plan"):
    end_date = start_date + datetime.timedelta(days=days - 1)
    daily_budget = budget / days

    # Get weather forecast
    weather_data = get_weather_forecast(destination, start_date, days)
    
    # Trip Summary
    st.success("✅ Trip Summary")
    st.write(f"📍 **Destination**: {destination}")
    st.write(f"📅 **From**: {start_date.strftime('%b %d, %Y')} to {end_date.strftime('%b %d, %Y')}")
    st.write(f"💸 **Daily Budget**: RM {daily_budget:.2f}")

    # Weather Forecast
    if weather_data:
        st.markdown("### 🌦️ Weather Forecast")
        for day in weather_data:
            emoji = "☀️" if day['weather'] == 'Clear' else \
                   "🌧️" if day['weather'] == 'Rain' else \
                   "⛅" if day['weather'] == 'Clouds' else "🌈"
            st.write(f"{day['date'].strftime('%a, %b %d')}: {emoji} {day['weather']}, {day['temp']:.1f}°C")
    
    # Packing List (now weather-aware)
    st.markdown("### � Packing List")
    packing_list = generate_packing_list(destination, weather_data)
    for item in packing_list:
        st.write(f"- {item}")

    # Travel Tips
    st.markdown("### 💡 Student Travel Tips")
    st.info("🎟️ Use your student ID for discounts on transport and museum entries.")
    st.info("🏨 Book accommodation early for better deals.")
    if weather_data and any(day['weather'] == 'Rain' for day in weather_data):
        st.warning("🌧️ Rain expected! Pack waterproof gear and plan indoor activities.")
    if weather_data and all(day['temp'] > 28 for day in weather_data):
        st.warning("🔥 Hot weather expected! Stay hydrated and use sunscreen.")




