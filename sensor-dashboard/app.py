import streamlit as st
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=5000, limit=None, key="refresh")

API_URL = st.secrets["API_URL"]

st.set_page_config(page_title="Dashboard Cảm Biến", layout="wide")
st.title("📊 Sensor Dashboard (Lambda + DynamoDB)")

device_id = st.text_input("Thiết bị:", "testing")
minutes = st.slider("Khoảng thời gian (phút):", 5, 10000, 30)

params = {"device_id": device_id, "minutes": minutes}
try:
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    items = response.json()
except Exception as e:
    st.error(f"Lỗi API: {e}")
    items = []

if items:
    df = pd.DataFrame(items)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    st.line_chart(df[['temperature', 'humidity', 'light', 'gas']])
    st.json(items[-1])
else:
    st.warning("Không có dữ liệu.")
