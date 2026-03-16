import streamlit as st
import pandas as pd
import joblib
import sys
import os

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.inventory import check_inventory

st.set_page_config(page_title="AI Food Demand Forecasting", layout="wide")

st.title("🍽 AI Food & Beverage Demand Forecasting System")

# ---------------- LOAD DATA ----------------

df = pd.read_csv("data/orders_2024.csv")
df.columns = df.columns.str.strip().str.lower()

orders_col = [c for c in df.columns if "order" in c][0]

st.subheader("📊 Historical Demand Trend")
st.line_chart(df[orders_col])

st.write("Total Orders in 2024:", int(df[orders_col].sum()))

# ---------------- LOAD MODEL ----------------

model, le_day, le_weather, le_event = joblib.load("models/demand_model.pkl")

# ---------------- PREDICTION ----------------

st.subheader("🔮 Predict Future Demand")

day = st.selectbox("Select Day", le_day.classes_)
weather = st.selectbox("Select Weather", le_weather.classes_)
event = st.selectbox("Select Event", le_event.classes_)

day_encoded = le_day.transform([day])[0]
weather_encoded = le_weather.transform([weather])[0]
event_encoded = le_event.transform([event])[0]

prediction = model.predict([[day_encoded, weather_encoded, event_encoded]])[0]
prediction = int(prediction)

st.success(f"📦 Predicted Orders: {prediction}")

# ---------------- INVENTORY ----------------

st.subheader("📦 Inventory & Procurement")

current_stock = st.number_input("Enter Current Stock", value=300)

order_quantity, alert = check_inventory(prediction, current_stock)

if order_quantity > 0:
    st.error(alert)
    st.write(f"🛒 Suggested Procurement Quantity: {int(order_quantity)}")
else:
    st.success(alert)