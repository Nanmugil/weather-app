import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta, timezone

import requests
from dotenv import load_dotenv


# Load API key from the .env file
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"


# -------------------- WINDOW --------------------

root = tk.Tk()
root.title("Weather App")
root.geometry("850x720")
root.minsize(700, 600)
root.configure(bg="#edf4fb")

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TButton",
    font=("Arial", 10, "bold"),
    padding=8,
)

style.configure(
    "TEntry",
    padding=8,
)

style.configure(
    "TLabel",
    background="#ffffff",
    foreground="#24364b",
    font=("Arial", 10),
)

style.configure(
    "Search.TButton",
    background="#1769aa",
    foreground="white",
)

style.map(
    "Search.TButton",
    background=[("active", "#12568d")],
)


# -------------------- HEADER --------------------

header = tk.Frame(root, bg="#1769aa", height=100)
header.pack(fill="x")
header.pack_propagate(False)

title_label = tk.Label(
    header,
    text="WEATHER APP",
    font=("Arial", 24, "bold"),
    fg="white",
    bg="#1769aa",
)
title_label.pack(pady=(20, 2))

subtitle_label = tk.Label(
    header,
    text="Check current weather and a five-day forecast",
    font=("Arial", 10),
    fg="#e5f1ff",
    bg="#1769aa",
)
subtitle_label.pack()


# -------------------- SEARCH SECTION --------------------

search_frame = tk.Frame(root, bg="#edf4fb")
search_frame.pack(fill="x", padx=25, pady=20)

city_entry = ttk.Entry(search_frame, font=("Arial", 12))
city_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

search_button = ttk.Button(
    search_frame,
    text="Search",
    style="Search.TButton",
)

search_button.pack(side="left", padx=(0, 8))

refresh_button = ttk.Button(
    search_frame,
    text="Refresh",
)

refresh_button.pack(side="left")


# -------------------- STATUS --------------------

status_label = tk.Label(
    root,
    text="Enter a city name to get started.",
    font=("Arial", 10),
    fg="#536579",
    bg="#edf4fb",
)
status_label.pack(pady=(0, 10))


# -------------------- CURRENT WEATHER CARD --------------------

current_card = tk.Frame(
    root,
    bg="white",
    highlightbackground="#d6e2ef",
    highlightthickness=1,
)
current_card.pack(fill="x", padx=25, pady=(0, 20))

city_label = tk.Label(
    current_card,
    text="City, Country",
    font=("Arial", 19, "bold"),
    fg="#173c67",
    bg="white",
)
city_label.pack(pady=(18, 5))

weather_icon_label = tk.Label(
    current_card,
    text="🌤️",
    font=("Segoe UI Emoji", 48),
    bg="white",
)
weather_icon_label.pack()

temperature_label = tk.Label(
    current_card,
    text="-- °C",
    font=("Arial", 28, "bold"),
    fg="#1769aa",
    bg="white",
)
temperature_label.pack()

condition_label = tk.Label(
    current_card,
    text="Weather condition",
    font=("Arial", 13),
    fg="#536579",
    bg="white",
)
condition_label.pack(pady=(4, 18))


# -------------------- WEATHER DETAILS --------------------

details_frame = tk.Frame(current_card, bg="white")
details_frame.pack(fill="x", padx=15, pady=(0, 18))

humidity_label = tk.Label(
    details_frame,
    text="Humidity: --%",
    font=("Arial", 11, "bold"),
    bg="white",
)
humidity_label.pack(side="left", expand=True)

feels_label = tk.Label(
    details_frame,
    text="Feels like: -- °C",
    font=("Arial", 11, "bold"),
    bg="white",
)
feels_label.pack(side="left", expand=True)

wind_label = tk.Label(
    details_frame,
    text="Wind: -- m/s",
    font=("Arial", 11, "bold"),
    bg="white",
)
wind_label.pack(side="left", expand=True)


# -------------------- FORECAST SECTION --------------------

forecast_heading = tk.Label(
    root,
    text="FIVE-DAY FORECAST",
    font=("Arial", 15, "bold"),
    fg="#173c67",
    bg="#edf4fb",
)
forecast_heading.pack(pady=(0, 12))

forecast_frame = tk.Frame(root, bg="#edf4fb")
forecast_frame.pack(fill="both", expand=True, padx=25)

forecast_labels = []

for index in range(5):
    card = tk.Frame(
        forecast_frame,
        bg="white",
        highlightbackground="#d6e2ef",
        highlightthickness=1,
    )

    card.grid(
        row=0,
        column=index,
        sticky="nsew",
        padx=4,
        pady=4,
    )

    date_label = tk.Label(
        card,
        text="--",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#173c67",
        justify="center",
    )
    date_label.pack(pady=(12, 8))

    icon_label = tk.Label(
        card,
        text="🌤️",
        font=("Segoe UI Emoji", 25),
        bg="white",
    )
    icon_label.pack(pady=5)

    temp_label = tk.Label(
        card,
        text="-- °C",
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#1769aa",
    )
    temp_label.pack(pady=5)

    weather_label = tk.Label(
        card,
        text="--",
        font=("Arial", 9),
        bg="white",
        wraplength=115,
        justify="center",
    )
    weather_label.pack(pady=5)

    humidity_forecast_label = tk.Label(
        card,
        text="Humidity: --%",
        font=("Arial", 9),
        bg="white",
        fg="#536579",
    )
    humidity_forecast_label.pack(pady=(5, 12))

    forecast_labels.append(
        (
            date_label,
            icon_label,
            temp_label,
            weather_label,
            humidity_forecast_label,
        )
    )

    forecast_frame.columnconfigure(index, weight=1)


# -------------------- WEATHER ICON --------------------

def get_weather_icon(condition):
    """Return an emoji based on the weather condition."""

    condition = condition.lower()

    if "thunderstorm" in condition:
        return "⛈️"
    elif "drizzle" in condition:
        return "🌦️"
    elif "rain" in condition:
        return "🌧️"
    elif "snow" in condition:
        return "❄️"
    elif "clear" in condition:
        return "☀️"
    elif "cloud" in condition:
        return "☁️"
    elif any(word in condition for word in ("mist", "fog", "haze")):
        return "🌫️"
    else:
        return "🌤️"


# -------------------- API REQUESTS --------------------

def get_current_weather(city):
    """Return current weather data for the selected city."""

    url = f"{BASE_URL}/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    return response.json()


def get_forecast(city):
    """Return forecast data for the selected city."""

    url = f"{BASE_URL}/forecast"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    return response.json()


# -------------------- UPDATE WEATHER DISPLAY --------------------

def update_weather(current_data, forecast_data):
    """Update the current weather and forecast cards."""

    city_name = current_data["name"]
    country = current_data["sys"]["country"]
    current = current_data["main"]
    weather = current_data["weather"][0]
    wind = current_data.get("wind", {})

    city_label.config(text=f"{city_name}, {country}")

    temperature_label.config(
        text=f"{current['temp']:.1f} °C"
    )

    weather_icon_label.config(
        text=get_weather_icon(weather["main"])
    )

    condition_label.config(
        text=weather["description"].title()
    )

    humidity_label.config(
        text=f"Humidity: {current['humidity']}%"
    )

    feels_label.config(
        text=f"Feels like: {current['feels_like']:.1f} °C"
    )

    wind_label.config(
        text=f"Wind: {wind.get('speed', 0):.1f} m/s"
    )

    # Convert forecast timestamps into the city's local time.
    timezone_offset = forecast_data["city"].get("timezone", 0)

    city_timezone = timezone(
        timedelta(seconds=timezone_offset)
    )

    daily_data = {}

    for item in forecast_data["list"]:
        forecast_time = datetime.fromtimestamp(
            item["dt"],
            tz=timezone.utc,
        ).astimezone(city_timezone)

        forecast_date = forecast_time.date()

        # Keep one forecast per day, preferring noon.
        if forecast_date not in daily_data:
            daily_data[forecast_date] = (item, forecast_time)

        if forecast_time.hour == 12:
            daily_data[forecast_date] = (item, forecast_time)

    days = list(daily_data.values())[:5]

    # Update all five forecast cards.
    for index, labels in enumerate(forecast_labels):
        (
            date_label,
            icon_label,
            temp_label,
            weather_label,
            humidity_forecast_label,
        ) = labels

        if index < len(days):
            item, forecast_time = days[index]
            condition = item["weather"][0]

            date_label.config(
                text=forecast_time.strftime("%a\n%d %b")
            )

            icon_label.config(
                text=get_weather_icon(condition["main"])
            )

            temp_label.config(
                text=f"{item['main']['temp']:.1f} °C"
            )

            weather_label.config(
                text=condition["description"].title()
            )

            humidity_forecast_label.config(
                text=f"Humidity: {item['main']['humidity']}%"
            )

        else:
            date_label.config(text="--")
            icon_label.config(text="🌤️")
            temp_label.config(text="-- °C")
            weather_label.config(text="--")
            humidity_forecast_label.config(text="Humidity: --%")

    status_label.config(text="Weather updated successfully.")


# -------------------- ERROR HANDLING --------------------

def finish_error(message):
    """Show an error and re-enable the buttons."""

    search_button.config(state="normal")
    refresh_button.config(state="normal")

    status_label.config(text="Unable to update weather.")

    messagebox.showerror("Weather App", message)


def finish_success(current_data, forecast_data):
    """Update the interface after successful requests."""

    try:
        update_weather(current_data, forecast_data)

    except (KeyError, IndexError, TypeError, ValueError):
        finish_error("Could not display the received weather data.")

    finally:
        search_button.config(state="normal")
        refresh_button.config(state="normal")


# -------------------- BACKGROUND REQUEST --------------------

def fetch_weather(city):
    """Fetch data in a background thread to keep the GUI responsive."""

    try:
        current_data = get_current_weather(city)
        forecast_data = get_forecast(city)

        root.after(
            0,
            lambda: finish_success(
                current_data,
                forecast_data,
            ),
        )

    except requests.exceptions.HTTPError as error:
        response = error.response

        if response is not None and response.status_code == 401:
            message = "Invalid API key or the key is not activated."
        elif response is not None and response.status_code == 404:
            message = "City not found. Check the spelling and try again."
        elif response is not None and response.status_code == 429:
            message = "API request limit reached. Please try again later."
        elif response is not None:
            message = f"Weather service error: HTTP {response.status_code}"
        else:
            message = "The weather service returned an HTTP error."

        root.after(0, lambda msg=message: finish_error(msg))

    except requests.exceptions.Timeout:
        root.after(
            0,
            lambda: finish_error(
                "The request timed out. Please try again."
            ),
        )

    except requests.exceptions.ConnectionError:
        root.after(
            0,
            lambda: finish_error(
                "No internet connection. Check your network."
            ),
        )

    except requests.exceptions.RequestException:
        root.after(
            0,
            lambda: finish_error(
                "Unable to connect to the weather service."
            ),
        )

    except (KeyError, TypeError, ValueError):
        root.after(
            0,
            lambda: finish_error(
                "Unexpected data received from the weather service."
            ),
        )


# -------------------- SEARCH FUNCTION --------------------

def search_weather():
    """Validate the city and start fetching weather."""

    city = city_entry.get().strip()

    if not city:
        messagebox.showwarning(
            "Missing city",
            "Please enter a city name.",
        )
        return

    if not API_KEY:
        messagebox.showerror(
            "API key missing",
            "Add OPENWEATHER_API_KEY to your .env file.",
        )
        return

    search_button.config(state="disabled")
    refresh_button.config(state="disabled")

    status_label.config(text=f"Fetching weather for {city}...")

    threading.Thread(
        target=fetch_weather,
        args=(city,),
        daemon=True,
    ).start()


# -------------------- BUTTON EVENTS --------------------

search_button.config(command=search_weather)
refresh_button.config(command=search_weather)

city_entry.bind(
    "<Return>",
    lambda event: search_weather(),
)


# -------------------- START APPLICATION --------------------

root.mainloop()