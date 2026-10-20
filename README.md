Weather App

A Python-based Weather Application that retrieves real-time weather information and a five-day forecast using the OpenWeather API.

Features

- Search for weather by city name.
- Display current temperature and feels-like temperature.
- Show weather conditions, humidity, and wind speed.
- Display a five-day weather forecast.
- Show weather emojis based on conditions.
- Refresh weather information.
- Handle invalid cities, API errors, timeouts, and connection problems.
- Provide both command-line and Tkinter GUI versions.

Technologies Used

- Python
- Tkinter
- Requests
- Python-dotenv
- OpenWeather API

Project Structure

weatherApp/
├── main.py
├── weather_gui.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md

Installation

1. Install Python.
2. Clone or download this repository.
3. Open the project folder in a terminal.
4. Install dependencies:

python -m pip install -r requirements.txt

5. Create a ".env" file and add your OpenWeather API key:

OPENWEATHER_API_KEY=your_actual_api_key_here

Run the Application

Command-line version:

python main.py

Graphical version:

python weather_gui.py

Security

Keep your API key private. Do not upload your ".env" file to GitHub.

Future Enhancements

- Add weather icons and improved UI themes.
- Add Celsius and Fahrenheit selection.
- Display sunrise and sunset times.
- Add hourly forecast details.
- Improve mobile-friendly and responsive access through a web version.

Author

Nanmugil K.

Python Full Stack Development | Python | Django | HTML | CSS | JavaScript