# Meteora
### Video Demo:  <URL [HERE](https://youtu.be/K9MzZfU8zW8?si=uAgs6Ebh5e7qOwMR)>
### Link : <URL [Link](https://meteora-seven-xi.vercel.app)>
#### Description:
Meteora is a weather web application built with python and flask.It allows users to search for any city in the world and instantly see the current weather conditions, a 4-day forcast and ai suggestions tailored to the weather and location

## How it works:
The user types a city name into the search bar and submits the form. Flask handles the POST request, calls OpenWeatherMap api to fetch real-time weather data, then calls the google gemini api to generate three short, practical suggestions based on the conditions. All of this data is passed to jinja2 template which renders the full page.The page design shifts dynamically based on the weather condition and time of day at searched location.*

## Technologies Used

- Python
- Flask
- Jinja2
- HTML/CSS
- OpenWeatherMap API
- Google Gemini API

## File breakdown:
**`app.py`**
The main flask application. Defines a single route ('/') thet handles both POST and GET requests. On GET, it renders the empty search page.On POST it validates user input , calls 'get_weather()' and 'get_ai_suggestions()', handles errors and passes all data to the template . Input validation checks that the city field is not empty and contains only alphabetic characters (with spaces allowed for cities like "New York"). If the ai suggestions fail for any reason, it falls back to a rule-based system (get_fallback_suggestions())so the app never breaks.

**`weather.py`**
Handels all communications with the OpenWeatherMap api. The `get_weather()` function makes two api calls : one for current weather and one for the 4-day forcast, and returns two clean python dictionnaries that the rest of the app uses. It also computes local time at the searched city using the UTC timezone offset returned by the api and determines which design to apply based on the current weather and local hour via `get_bg_class()`. the `weather_icon()` function maps conditiion strings to icon names. All api keys are loaded from a `.env` file via `python-dotenv`.

**`aisuggestions.py`**
Handles the Google gemini api integration. The `get_ai_suggestions()` function builds a detailed prompt containing the city, country, current conditions and forcast summary, then asks gemini to respond with a JSON array of three short suggestions. The response is parsed and returned as a python list. Because gemini sometimes wraps JSON in markdown code fences, the function strips those before parsing. The `get_fallback_suggestions()` functon provides rule-based suggestions in case of the api call fails.

**`/templates/index.html`**
The single HTML template rendered by flask. Uses Jinja2 templating throughout the page. The page title updates with the city name, the body class changes to match the weather theme, and all weather data is injected directly into the HTML at render time. Conditional blocks (`{% if current %}`, `{%if suggestions%}`) ensure sections only appear when data is available. icons use Lucide loaded via unpkg CDN (`https://unpkg.com/lucide@latest/dist/umd/lucide.min.js`). After the page loads, `lucide.createIcons()` is called in `<script>` to replace every `<i data-lucide="...">` tag with the corresponding inline SVG. The search is a plain HTML form with `method="POST"`.

**`static/style.css`**
The entire visual design of the app. The theming system is built on CSS custom properties: seven theme classes (clear day, cloudy, rain, storm, snow, night, night rain) each override a set of variables (`--bg`, `--accent`, `--glass`, `--btn-bg`, etc.) that cascade through every element on the page. The visual style is glassmorphism: semi-transparent backgrounds with `backdrop-filter: blur()` which works well over colorful gradients. The snow theme intentionally uses dark text instead of white, since the background is light.

## Design decisions:
The biggest decision was choosing server-side rendering with Jinja over a JavaScript-heavy approach.

Another deliberate choice was the use of Google gemini for ai suggestions instead of just relying on simple rule-based system that still exists because gemini produces genuinely useful , location-aware suggestions that feel personal, it knows that 32°C in Tunis hits differently than 32°C in London. The prompt explicitly asks for suggestions under 15 words, which keeps the UI clean.

## Setup
 
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
 
2. Create a `.env` file in the project root:
   ```
   OPENWEATHER_API_KEY=your_key_here
   GEMINI_API_KEY=your_key_here
   ```
 
3. Run the app:
   ```
   python app.py
   ```
 
4. Open your browser at http://127.0.0.1:5000

## Project structure:
```
meteora/
├── app.py               # Flask app and routing
├── weather.py           # OpenWeatherMap API logic
├── aisuggestions.py     # Google Gemini AI suggestions
├── requirements.txt     # Python dependencies
├── .env                 # API keys (not committed)
├── .gitignore
├── templates/
│   └── index.html       # Jinja2 template
└── static/
    ├── style.css        # Theming and layout
```

