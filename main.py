import os
from datetime import datetime

import requests
from dotenv import load_dotenv

# Load the API key from the .env file
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5"


def get_current_weather(city):
    """Fetch current weather information for a city."""
    url = f"{BASE_URL}/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def get_forecast(city):
    """Fetch the five-day forecast in three-hour intervals."""
    url = f"{BASE_URL}/forecast"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def display_current_weather(data):
    """Display the current weather details."""
    city = data["name"]
    country = data["sys"]["country"]
    temperature = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    condition = data["weather"][0]["description"]
    wind_speed = data["wind"]["speed"]

    print("\n" + "=" * 40)
    print("          CURRENT WEATHER")
    print("=" * 40)
    print(f"City          : {city}, {country}")
    print(f"Temperature   : {temperature} °C")
    print(f"Feels like    : {feels_like} °C")
    print(f"Condition     : {condition.title()}")
    print(f"Humidity      : {humidity}%")
    print(f"Wind speed    : {wind_speed} m/s")
    print("=" * 40)


def display_forecast(data):
    """Display one forecast entry per date, around noon."""
    daily_forecasts = {}

    for item in data["list"]:
        forecast_time = datetime.fromtimestamp(item["dt"])
        date = forecast_time.strftime("%Y-%m-%d")

        # Prefer the forecast closest to 12:00 for each date.
        if date not in daily_forecasts:
            daily_forecasts[date] = item
        else:
            saved_time = datetime.fromtimestamp(
                daily_forecasts[date]["dt"]
            )
            if abs(forecast_time.hour - 12) < abs(saved_time.hour - 12):
                daily_forecasts[date] = item

    print("\n" + "=" * 40)
    print("         FIVE-DAY FORECAST")
    print("=" * 40)

    for date, item in list(daily_forecasts.items())[:5]:
        temp = item["main"]["temp"]
        condition = item["weather"][0]["description"].title()
        humidity = item["main"]["humidity"]

        print(f"\nDate        : {date}")
        print(f"Temperature : {temp} °C")
        print(f"Condition   : {condition}")
        print(f"Humidity    : {humidity}%")

    print("\n" + "=" * 40)


def main():
    if not API_KEY:
        print("API key not found.")
        print("Please add OPENWEATHER_API_KEY to your .env file.")
        return

    print("\nWELCOME TO THE WEATHER APP")

    while True:
        city = input(
            "\nEnter city name (or type 'exit' to quit): "
        ).strip()

        if city.lower() == "exit":
            print("Thank you for using the Weather App!")
            break

        if not city:
            print("Please enter a city name.")
            continue

        try:
            current_data = get_current_weather(city)
            forecast_data = get_forecast(city)

            display_current_weather(current_data)
            display_forecast(forecast_data)

        except requests.exceptions.HTTPError as error:
            status = error.response.status_code

            if status == 404:
                print("City not found. Check the spelling and try again.")
            elif status == 401:
                print("API key is invalid or not activated yet.")
            elif status == 429:
                print("API request limit reached. Please try later.")
            else:
                print(f"Weather API error: {status}")

        except requests.exceptions.Timeout:
            print("The request timed out. Please try again.")

        except requests.exceptions.ConnectionError:
            print("Could not connect. Check your internet connection.")

        except requests.exceptions.RequestException as error:
            print(f"Request failed: {error}")

        except (KeyError, IndexError, TypeError):
            print("Unexpected weather data received from the API.")


if __name__ == "__main__":
    main()