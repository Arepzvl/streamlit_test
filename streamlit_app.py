import streamlit as st
import requests

# Set the app title 
st.title('This Is My First Streamlit!!')

# Add a welcome message 
st.write('Welcome to my Streamlit app!')

# Create a text input 
widgetuser_input = st.text_input('Enter a custom message:', 'Hello, Streamlit!')

# Display the customized message 
st.write('Customized Message:', widgetuser_input)

# Senarai mata wang yang disokong (boleh tambah lagi jika perlu)
currency_options = ['MYR', 'USD', 'EUR', 'GBP', 'JPY', 'SGD', 'AUD', 'CNY']

# Dropdown untuk memilih mata wang asas
base_currency = st.selectbox('Pilih mata wang asas:', currency_options)

# API call bergantung pada pilihan pengguna
response = requests.get(f'https://api.vatcomply.com/rates?base={base_currency}')

# Papar output jika berjaya
if response.status_code == 200:
    data = response.json()
    st.write(f'Kadar tukaran untuk: {base_currency}')
    st.json(data)  # nicely formatted JSON output
else:
    st.error(f"API call failed with status code: {response.status_code}")
