import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# Tajuk aplikasi
st.title('Currency Exchange Rate Viewer')

# Mesej selamat datang
st.write('Pilih mata wang asas dan sasaran untuk lihat kadar tukaran serta perubahannya dalam bentuk graf!')

# Senarai mata wang
currency_options = ['MYR', 'USD', 'EUR', 'GBP', 'JPY', 'SGD', 'AUD', 'CNY']

# Dropdown untuk mata wang asas dan sasaran
base_currency = st.selectbox('Pilih mata wang asas:', currency_options)
target_currency = st.selectbox('Pilih mata wang sasaran:', currency_options, index=1)

# Elakkan pengguna pilih mata wang yang sama
if base_currency == target_currency:
    st.warning("Sila pilih dua mata wang yang berbeza untuk perbandingan.")
else:
    # Tarikh mula dan tamat (30 hari terakhir)
    end_date = datetime.today()
    start_date = end_date - timedelta(days=30)

    # Format tarikh
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')

    # Panggilan API untuk data sejarah
    url = f'https://api.vatcomply.com/history?base={base_currency}&symbols={target_currency}&start_date={start_str}&end_date={end_str}'
    response = requests.get(url)

    if response.status_code == 200:
        history_data = response.json().get("rates", {})

        # Tukar data ke dalam DataFrame
        df = pd.DataFrame.from_dict(history_data, orient='index')
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        df.columns = [f'{base_currency} to {target_currency}']

        # Papar carta
        st.write(f'Graf kadar tukaran {base_currency} kepada {target_currency} untuk 30 hari terakhir:')
        st.line_chart(df)

    else:
        st.error(f"API gagal dimuatkan. Kod status: {response.status_code}")

