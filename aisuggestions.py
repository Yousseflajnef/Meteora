from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))

def get_ai_suggestions(current, forecast):
    """Call Gemini API to get personalized weather suggestions."""

    #Format forecast data into readable summary string
    forecast_summary = "\n".join([
        f"- {data['date']}: {data['desc']}, avg {data['temp']}°C"
        for data in forecast
    ])
    # detailed prompt for gemini with weather data and format instructions
    prompt = f"""You are a helpful weather assistant. Based on the following weather data, give 3 short, practical, friendly suggestions for the day.
      Be specific to the conditions and location. Keep each suggestion under 15 words. Respond ONLY with a JSON array of 3 strings, no markdown, no preamble.

    Location: {current['city']}, {current['country']}
    Current: {current['condition']}, {current['temp']}°C, feels like {current['feels_like']}°C
    Humidity: {current['humidity']}%, Wind: {current['wind']} km/h

    Forecast:
    {forecast_summary}

    Example response format:
    ["Suggestion one here.", "Suggestion two here.", "Suggestion three here."]"""
    #call gemini api with prompt
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,

    )

    text = response.text.strip()
    # Strip markdown fences if present
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    suggestions = json.loads(text.strip())
    return suggestions

def get_fallback_suggestions(current):
    """Rule-based fallback if API call fails."""
    suggestions = []
    c = current["condition"].lower()
    temp = current["temp"]

    if "rain" in c:
        suggestions.append("Don't forget your umbrella today.")
    if "thunder" in c:
        suggestions.append("Avoid open spaces, thunderstorms are forecast.")
    if "snow" in c:
        suggestions.append("Bundle up, it's snowing outside.")
    if temp >= 30:
        suggestions.append("Hot weather, stay hydrated")
    elif temp >= 25:
        suggestions.append("Remember to use sunscreen before going out.")
    if temp <= 5:
        suggestions.append("Freezing temperatures, wear a coat.")
    elif temp <= 12:
        suggestions.append("Bring a jacket, it's chilly.")
    if current["wind"] > 40:
        suggestions.append("Strong wind secure your belongings outside.")

    if not suggestions:
        suggestions.append("Pleasant weather enjoy your day!")

    return suggestions[:3]
