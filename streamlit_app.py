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
    international_items = ["🛂 Passport", "✈️ Boarding Pass", "💵 Foreign Currency"]

    if destination.lower() in ["langkawi", "pulau pinang", "penang"]:
        return general + beach_items
    elif destination.lower() in ["cameron highlands"]:
        return general + cold_items
    elif destination.lower() == "singapore":
        return general + international_items  # Add passport for Singapore trips
    else:
        return general

    if destination.lower() in ["langkawi", "pulau pinang", "penang"]:
        return general + beach_items
    elif destination.lower() in ["cameron highlands"]:
        return general + cold_items
    else:
        return general

# === Get Nearby Attractions (using OpenStreetMap Nominatim API) ===
def get_nearby_attractions(lat, lon, radius=5000, limit=5):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat}&lon={lon}"
        response = requests.get(url, headers={"User-Agent": "StudentTravelPlanner"})
        if response.status_code == 200:
            data = response.json()
            return data.get("display_name", "Location details not available")
        return "No nearby attractions found"
    except:
        return "Could not fetch attractions"

# === Predefined Interesting Places ===
DESTINATION_ATTRACTIONS = {
    "Kuala Lumpur": [
        {"name": "Petronas Twin Towers", "coords": (3.1580, 101.7118), "type": "icon", "color": "blue", "icon": "camera"},
        {"name": "KL Tower", "coords": (3.1390, 101.6869), "type": "icon", "color": "red", "icon": "camera"},
        {"name": "Batu Caves", "coords": (3.2373, 101.6839), "type": "icon", "color": "green", "icon": "temple"},
        {"name": "Merdeka Square", "coords": (3.1478, 101.6953), "type": "icon", "color": "orange", "icon": "flag"}
    ],
    "Port Dickson":[
        {"name": "Army Museum", "coords": (2.49643, 101.84729), "type": "icon", "color": "blue", "icon": "camera"},
        {"name": "Pantai Teluk kemang", "coords": (2.454562, 101.8599476), "type": "icon", "color": "lightblue", "icon": "umbrella"},
        {"name": "Port Dickson Ornamental Fish Center", "coords": (2.463292413830889, 101.85039595269518), "type": "icon", "color": "blue", "icon": "camera"},
    ],
    "Melaka":[
        {"name": "Jonker Street Night Market", "coords": (2.1950778007253806, 102.24845147301384), "type": "icon", "color": "red", "icon": "shopping-cart"},
        {"name": "A Famosa", "coords": (2.1920185802100858, 102.25046435952073), "type": "icon", "color": "blue", "icon": "camera"},
        {"name": "Taming Sari Tower", "coords": (2.1911108173642373, 102.24703204602767), "type": "icon", "color": "blue", "icon": "camera"}, 
        {"name": "Muzium Samudera", "coords": (2.192013291333821, 102.24724510130268), "type": "icon", "color": "blue", "icon": "camera"},
    ],
    "Kuantan":[
        {"name": "Teluk Cempedak", "coords": (3.8134673607867153, 103.37036876780307), "type": "icon", "color": "lightblue", "icon": "umbrella"},
        {"name": "Menara Kuantan 188", "coords": (3.80421487213873, 103.32754978650692), "type": "icon", "color": "red", "icon": "camera"},
        {"name": "Penyu Gergasi Pantai Pelindung", "coords": (3.834100334424492, 103.37638360000003), "type": "icon", "color": "blue", "icon": "camera"},
        {"name": "Taman Gelora Kuantan", "coords": (3.809206965543498, 103.34928780184948), "type": "icon", "color": "green", "icon": "tree"}
    ],
    "Johor": [
        {"name": "LEGOLAND Malaysia", "coords": (1.4273704688381563, 103.62948920000002), "type": "icon", "color": "blue", "icon": "camera"},
        {"name": "Kota Tinggi Firefly Park", "coords": (1.7271644891503173, 103.91135728465744), "type": "icon", "color": "blue", "icon": "camera"},
        {"name": "Desaru Beach", "coords": (1.5478119955238197, 104.26247003862977), "type": "icon", "color": "lightblue", "icon": "umbrella"},
        {"name": "Johor Premium Outlet", "coords": (1.6030799550645818, 103.62164121534255), "type": "icon", "color": "red", "icon": "shopping-cart"}
    ],
    "Terengganu": [
        {"name": "Masjid Kristal", "coords": (5.322503892862815, 103.12052834232873), "type": "icon", "color": "orange", "icon": "temple"},
        {"name": "Pasar Payang", "coords": (5.337485775923021, 103.1361146), "type": "icon", "color": "red", "icon": "shopping-cart"},
        {"name": "Drawnbridge Kuala Terengganu", "coords": (5.340451724170789, 103.14474695582182), "type": "icon", "color": "blue", "icon": "camera"},
        {"name": "Redang Island", "coords": (5.801370419304246, 102.99448439461156), "type": "icon", "color": "blue", "icon": "camera"},
    ],
    "Penang": [
        {"name": "Penang Hill", "coords": (5.4149, 100.3298), "type": "icon", "color": "green", "icon": "tree"},
        {"name": "Kek Lok Si Temple", "coords": (5.4205, 100.3382), "type": "icon", "color": "orange", "icon": "temple"},
        {"name": "George Town Street Art", "coords": (5.4141, 100.3288), "type": "icon", "color": "purple", "icon": "paint-brush"},
        {"name": "Penang National Park", "coords": (5.4717, 100.2044), "type": "icon", "color": "darkgreen", "icon": "tree"},
        {"name": "Escape Penang", "coords": (5.449948766600535, 100.21410237301384), "type": "icon", "color": "lightblue", "icon": "umbrella"},
    ],
    "Langkawi": [
        {"name": "Sky Bridge", "coords": (6.3647, 99.6769), "type": "icon", "color": "blue", "icon": "bridge"},
        {"name": "Cenang Beach", "coords": (6.2936, 99.7281), "type": "icon", "color": "lightblue", "icon": "umbrella"},
        {"name": "Kilim Geoforest Park", "coords": (6.4075, 99.8478), "type": "icon", "color": "green", "icon": "tree"},
        {"name": "Eagle Square", "coords": (6.3195, 99.8466), "type": "icon", "color": "red", "icon": "flag"}
    ],
    "Cameron Highlands": [
        {"name": "Boh Tea Plantation", "coords": (4.5204, 101.4127), "type": "icon", "color": "green", "icon": "leaf"},
        {"name": "Mossy Forest", "coords": (4.4933, 101.3833), "type": "icon", "color": "darkgreen", "icon": "tree"},
        {"name": "Lavender Garden", "coords": (4.4693, 101.3773), "type": "icon", "color": "purple", "icon": "flower"},
        {"name": "Time Tunnel Museum", "coords": (4.4629, 101.3758), "type": "icon", "color": "blue", "icon": "book"}
    ],
    "Singapore": [
        {"name": "Marina Bay Sands", "coords": (1.2837, 103.8607), "type": "icon", "color": "blue", "icon": "hotel"},
        {"name": "Gardens by the Bay", "coords": (1.2816, 103.8636), "type": "icon", "color": "green", "icon": "tree"},
        {"name": "Sentosa Island", "coords": (1.2494, 103.8303), "type": "icon", "color": "lightblue", "icon": "umbrella"},
        {"name": "Chinatown", "coords": (1.2838, 103.8439), "type": "icon", "color": "red", "icon": "shopping-cart"}
    ]
}

# === Destination Coordinates ===
DESTINATION_COORDS = {
    "Kuala Lumpur": (3.1390, 101.6869),
    "Port Dickson": (2.522540, 101.796295),
    "Melaka": (2.3263, 102.3464),
    "Kuantan": (3.8201, 103.3322),
    "Johor": (1.9344, 103.3587),
    "Terengganu": (5.0936, 102.9896),
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
    "Port Dickson",
    "Melaka", 
    "Kuantan",
    "Johor",
    "Terengganu",
    "Penang",
    "Langkawi",
    "Cameron Highlands",
    "Singapore",
])
days = st.slider("📅 Number of Days", 1, 14, 3)
start_date = st.date_input("📆 Start Date", datetime.date.today())

# Base budget amounts by destination type
base_budgets = {
    "city": 400,      # KL, Penang, Johor, etc.
    "beach": 350,     # Port Dickson, Langkawi
    "hill": 450,      # Cameron Highlands
    "international": 600  # Singapore
}

# Categorize destinations
destination_types = {
    "Kuala Lumpur": "city",
    "Port Dickson": "beach",
    "Melaka": "city",
    "Kuantan": "beach",
    "Johor": "city",
    "Terengganu": "beach",
    "Penang": "city",
    "Langkawi": "beach",
    "Cameron Highlands": "hill",
    "Singapore": "international"
}

# Calculate dynamic budget
base_budget = base_budgets[destination_types[destination]]
budget = base_budget + (days * 50)  # RM50 extra per day
budget = st.number_input("💸 Your estimated budget (MYR)", 
                        min_value=100,
                        max_value=5000,
                        value=int(budget))


# Enter your OpenWeatherMap API key here
api_key = "8447cc1e7a0d0d0d8ceef48fbf8ddee2"

# === Trip Planner ===
if st.button("✨ Generate Trip Plan"):
    end_date = start_date + datetime.timedelta(days=days - 1)
    
    # Trip Summary
    st.success("✅ Trip Summary")
    st.write(f"📍 **Destination**: {destination}")
    st.write(f"📅 **From**: {start_date.strftime('%b %d, %Y')} to {end_date.strftime('%b %d, %Y')}")
    st.write(f"💰 **Total Budget**: RM {budget:,.2f}")
    
    if days > 0:
        daily_budget = budget / days
        st.write(f"📊 **Daily Budget**: RM {daily_budget:,.2f} (for {days} days)")
        
        # Budget allocation breakdown
        st.markdown("### 💰 Budget Allocation Guide")
        st.write(f"- 🏨 Accommodation: RM {budget*0.4/days:,.2f}/day")
        st.write(f"- 🍽️ Food: RM {budget*0.3/days:,.2f}/day") 
        st.write(f"- 🚍 Transport: RM {budget*0.2/days:,.2f}/day")
        st.write(f"- 🎟 Activities: RM {budget*0.1/days:,.2f}/day")
    else:
        st.warning("Number of days must be at least 1")
        st.stop()

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
        
        # Display Map with Attractions
        st.markdown("### 🗺️ Destination Map with Attractions")
        if destination in DESTINATION_COORDS:
            lat, lon = DESTINATION_COORDS[destination]
        else:
            lat, lon = weather['lat'], weather['lon']
        
        m = folium.Map(location=[lat, lon], zoom_start=12)
        
        # Add main destination marker
        folium.Marker(
            [lat, lon],
            popup=destination,
            tooltip="Your destination",
            icon=folium.Icon(color="black", icon="star")
        ).add_to(m)
        
        # Add predefined attractions
        if destination in DESTINATION_ATTRACTIONS:
            for attraction in DESTINATION_ATTRACTIONS[destination]:
                folium.Marker(
                    location=attraction["coords"],
                    popup=attraction["name"],
                    tooltip=attraction["name"],
                    icon=folium.Icon(color=attraction["color"], icon=attraction["icon"])
                ).add_to(m)
        
        # Try to get nearby attractions from OSM
        try:
            nearby_info = get_nearby_attractions(lat, lon)
            if isinstance(nearby_info, str):
                st.write(f"📍 **Location Details**: {nearby_info}")
        except:
            pass
        
        folium_static(m, width=700, height=400)
        
        # Display attractions list
        st.markdown("### 🏞️ Top Attractions")
        if destination in DESTINATION_ATTRACTIONS:
            cols = st.columns(2)
            for i, attraction in enumerate(DESTINATION_ATTRACTIONS[destination]):
                with cols[i % 2]:
                    st.markdown(f"📍 **{attraction['name']}**")
                    st.write(f"🗺️ [View on Map](https://www.google.com/maps?q={attraction['coords'][0]},{attraction['coords'][1]})")
    else:
        st.warning("Could not fetch weather data. Please check your API key or destination name.")

    # Travel Tips
    st.markdown("### 💡 Student Travel Tips")
    st.info("🎟️ Use your student ID for discounts on transport and museum entries.")
    st.info("🏨 Book accommodation early for better deals.")
    st.info("🗺️ Check the map above for key attractions in your destination.")
    st.info("🍽️ Try local street food for budget-friendly meals.")
