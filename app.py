from flask import Flask, flash, redirect, render_template, request, session,jsonify
from weather import get_weather
from aisuggestions import get_ai_suggestions, get_fallback_suggestions


app = Flask(__name__)



@app.route("/",methods=["GET", "POST"])
def index():
    """show weather and forcast after searching city"""
    current = None
    forecast = []
    suggestions = []
    error = None
    city = ""
    if request.method == "POST":


            city = request.form.get("city")
            #verify user input
            if not city:
                error = "Must Enter a city."
            try:
                if not city.replace(" ", "").isalpha():
                    raise ValueError
            except ValueError:
                error = "Must enter a valid city name."
            #get data
            current, forecast = get_weather(city)
            if current is None:
                error = "City not found."
            else:
                # Try AI suggestions, fall back to rule based
                try:
                    suggestions = get_ai_suggestions(current, forecast)
                except Exception as e:
                    print(f"AI ERROR:{e}")
                    suggestions = get_fallback_suggestions(current)



    return render_template("index.html",
            current=current,
            forecast=forecast,
            suggestions=suggestions,
            error=error,
            city=city,
            )
if __name__ == "__main__":
    app.run(debug=True)



