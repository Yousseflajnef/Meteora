import requests
from datetime import datetime, UTC
from dotenv import load_dotenv
import os

# load api key from .env file
load_dotenv()
api_key = os.getenv("OPENWEATHER_API_KEY")

# check weather condition and return corresponding Lucide icon


def weather_icon(condition):
    cond = condition.lower()
    if "rain" in cond or "light rain" in cond:
        return "cloud-rain"
    if "thunder" in cond:
        return "cloud-lightning"
    if "snow" in cond:
        return "snowflake"
    if ("fog" in cond or "mist" in cond):
        return "wind"
    if "cloud" in cond:
        return "cloud"
    if "night" in cond:
        return "moon"
    if ("clear" in cond or "sunny" in cond):
        return "sun"
    return "cloud-sun"  # default
# check weather condition and return corresponding background


def get_bg_class(condition, hour):
    cond = condition.lower()
    is_day = 6 <= hour < 19
    # check daytime
    if is_day:
        if "rain" in cond:
            return "bg-rainy-day"
        if "cloud" in cond:
            return "bg-cloudy-day"
        if "snow" in cond:
            return "bg-snowy-day"
        if ("thunderstorm" in cond or "storm" in cond):
            return "bg-storm"
        if ("fog" in cond or "mist" in cond):
            return "bg-foggy-day"
        return "bg-clear-day"  # default for day
    else:
        if "rain" in cond:
            return "bg-night-rain"
        if "cloud" in cond:
            return "bg-night-rain"
        if "thunder" in cond:
            return "bg-night-rain"
        if "snow" in cond:
            return "bg-night-rain"
        if ("fog" in cond or "mist" in cond):
            return "bg-night-rain"
        return "bg-night"


def get_weather(city):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=en&units=metric"
    data = requests.get(url, timeout=6).json()
    if data.get("cod") != 200:
        return None, None
    # get weather condition description form OpenWeather API
    condition = data["weather"][0]["description"]
    tz = data.get("timezone", 0)
    local_timestamp = datetime.now(UTC).timestamp() + tz
    hour = int((local_timestamp) % 86400 // 3600)  # calculate time in hours
    minute = int((local_timestamp % 3600) // 60)
    local_time = f"{hour:02d}:{minute:02d}"

    # create dictionnary with current weather data
    current = {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temp": round(data["main"]["feels_like"], 1),
        "feels_like": round(data["main"]["feels_like"], 1),  # round to 1 decimal
        "humidity": data["main"]["humidity"],
        "wind": round(data["wind"]["speed"], 1),
        "condition": condition,
        "icon": weather_icon(condition),
        "bg_class": get_bg_class(condition, hour),
        "hour": hour,
        "local_time": local_time
    }
    # Fetch forecast from API (i wrote this section with the help of claude ai to establish forcast)
    url_f = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&lang=en&units=metric"
    forecast_data = requests.get(url_f, timeout=6).json()
    # group forcast data by date
    days = {}
    for e in forecast_data.get("list", []):
        date = datetime.fromtimestamp(e["dt"]).strftime("%A %d/%m")
        # store tempature and description
        temp_i = e["main"]["temp"]
        desc = e["weather"][0]["description"].capitalize()
        days.setdefault(date, []).append((temp_i, desc))
    # forcast list
    forecast = []
    # take first 4 days
    for i, (date, vals) in enumerate(days.items()):
        if i >= 4:
            break
        temp_avg = round(sum(v[0] for v in vals) / len(vals), 1)  # calculate average temperature
        desc = vals[0][1]
        forecast.append({
            "date": date.capitalize(),
            "temp": temp_avg,
            "desc": desc,
            "icon": weather_icon(desc),
        })

    return current, forecast
