import pandas as pd
import numpy as np

dates = pd.date_range(start="2024-01-01", end="2024-12-31")

data = []

for date in dates:

    day = date.day_name()

    weather = np.random.choice(["Sunny","Rainy","Cloudy"])

    event = np.random.choice(["None","Festival","Sports"])

    base = 100

    if day in ["Saturday","Sunday"]:
        base += 50

    if weather == "Rainy":
        base -= 20

    if event != "None":
        base += 40

    orders = base + np.random.randint(-10,10)

    data.append([date,day,weather,event,orders])

df = pd.DataFrame(data,columns=[
"date","day_of_week","weather","event","orders"
])

df.to_csv("data/orders_2024.csv",index=False)

print("Dataset Generated")