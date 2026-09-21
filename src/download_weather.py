import requests
import pandas as pd

url = "https://power.larc.nasa.gov/api/temporal/daily/point"

params = {
    "parameters": "PRECTOTCORR,T2M,RH2M",   # rainfall, temperature, humidity
    "community": "AG",
    "longitude": 79.8612,                    # Colombo
    "latitude": 6.9271,
    "start": "20190101",
    "end": "20241231",
    "format": "JSON",
}

response = requests.get(url, params=params, timeout=120)
print("Status:", response.status_code)
response.raise_for_status()

data = response.json()["properties"]["parameter"]
weather = pd.DataFrame(data)
weather.index.name = "date"

weather.to_csv("data/raw/nasa_power_colombo_daily.csv")
print("Shape:", weather.shape)
print(weather.head())