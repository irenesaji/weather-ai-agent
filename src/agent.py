import logging

import requests


logging.basicConfig(
    filename="logs/agent.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def get_weather():
    """Fetch current weather data."""
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=8.5241&longitude=76.9366"
        "&current=temperature_2m,relative_humidity_2m,weather_code"
    )

    logging.info("Requesting weather data from Open-Meteo API.")

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    logging.info("Weather data received successfully.")

    return response.json()


def main():
    """Run the weather agent."""
    logging.info("Weather AI Agent started.")

    weather = get_weather()
    current = weather["current"]

    temperature = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    weather_code = current["weather_code"]

    print("Weather AI Agent")
    print("----------------")
    print(f"Temperature: {temperature} °C")
    print(f"Humidity: {humidity}%")
    print(f"Weather code: {weather_code}")

    if temperature > 35:
        decision = "It is very hot. Stay hydrated."
    elif temperature < 20:
        decision = "It is cool. Consider carrying a light jacket."
    else:
        decision = "Weather conditions are comfortable."

    print(f"Decision: {decision}")

    logging.info("Temperature: %s °C", temperature)
    logging.info("Humidity: %s%%", humidity)
    logging.info("Weather code: %s", weather_code)
    logging.info("Agent decision: %s", decision)
    logging.info("Weather AI Agent finished successfully.")


if __name__ == "__main__":
    main()