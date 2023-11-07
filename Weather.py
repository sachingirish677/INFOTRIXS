import requests
import argparse
import json
import time

API_KEY = "c2d0e899b97c4d80b0b133939230311"

def get_weather(city):
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {"key": API_KEY, "q": city}
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Couldn't fetch weather data for {city}")
        return None

def add_favorite(city):
    try:
        with open("favorites.json", "r") as file:
            favorites = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        favorites = []

    if city not in favorites:
        favorites.append(city)
        with open("favorites.json", "w") as file:
            json.dump(favorites, file)
        print(f"{city} added to favorites.")

def remove_favorite(city):
    with open("favorites.json", "r") as file:
        favorites = json.load(file)

    if city in favorites:
        favorites.remove(city)
        with open("favorites.json", "w") as file:
            json.dump(favorites, file)
        print(f"{city} removed from favorites.")
    else:
        print(f"{city} is not in favorites.")

def display_favorites():
    try:
        with open("favorites.json", "r") as file:
            favorites = json.load(file)

        if favorites:
            print("Favorite Cities:")
            for city in favorites:
                print(f"- {city}")
        else:
            print("No favorite cities.")
    except (FileNotFoundError, json.JSONDecodeError):
        print("No favorite cities.")

def main():
    parser = argparse.ArgumentParser(description="Weather API")
    parser.add_argument("--city", help="Check weather for a specific city")
    parser.add_argument("--add", help="Add a city to favorites")
    parser.add_argument("--remove", help="Remove a city from favorites")
    parser.add_argument("--favorites", action="store_true", help="Display favorite cities")
    args = parser.parse_args()

    if args.city:
        weather_data = get_weather(args.city)
        if weather_data:
            print(f"Weather in {args.city}: {weather_data['current']['condition']['text']}, "
                  f"Temperature: {weather_data['current']['temp_c']}°C")
    elif args.add:
        add_favorite(args.add)
    elif args.remove:
        remove_favorite(args.remove)
    elif args.favorites:
        display_favorites()
    else:
        print("Please provide a valid command. Use --help for assistance.")

if __name__ == "__main__":
    while True:
        main()
        time.sleep(15)
