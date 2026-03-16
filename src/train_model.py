import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("data/orders_2024.csv")

# Clean column names
df.columns = df.columns.str.strip().str.lower()

print("Columns found in dataset:", df.columns)

# Detect columns
day_col = [c for c in df.columns if "day" in c][0]
weather_col = [c for c in df.columns if "weather" in c][0]
event_col = [c for c in df.columns if "event" in c][0]
orders_col = [c for c in df.columns if "order" in c][0]

# Remove rows where orders is NaN
df = df.dropna(subset=[orders_col])

# Convert orders to numeric (force safe)
df[orders_col] = pd.to_numeric(df[orders_col], errors="coerce")

# Drop again if any conversion created NaN
df = df.dropna(subset=[orders_col])

# Encode categorical columns
le_day = LabelEncoder()
le_weather = LabelEncoder()
le_event = LabelEncoder()

df[day_col] = le_day.fit_transform(df[day_col])
df[weather_col] = le_weather.fit_transform(df[weather_col])
df[event_col] = le_event.fit_transform(df[event_col])

X = df[[day_col, weather_col, event_col]]
y = df[orders_col]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
joblib.dump((model, le_day, le_weather, le_event), "models/demand_model.pkl")

print("✅ Model trained and saved successfully!")