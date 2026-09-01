"""Production-ready weather agent with exceptions, retries, and logging."""

import logging
import time

import requests


logging.basicConfig(
    filename="logs/agent.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def get_weather():
    """Fetch current weather data with bounded retries."""
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=8.5241&longitude=76.9366"
        "&current=temperature_2m,relative_humidity_2m,weather_code"
    )

    max_retries = 3

    for attempt in range(1, max_retries + 1):
        logging.info(
            "Weather API attempt %s of %s.",
            attempt,
            max_retries,
        )

        try:
            logging.info("Requesting weather data from Open-Meteo API.")

            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            logging.info("Weather data received successfully.")

            return data

        except requests.exceptions.Timeout:
            logging.warning(
                "Weather API request timed out on attempt %s.",
                attempt,
            )

        except requests.exceptions.RequestException as error:
            logging.error(
                "Weather API request failed on attempt %s: %s",
                attempt,
                error,
            )

        if attempt < max_retries:
            delay = 2 ** (attempt - 1)

            logging.info(
                "Retrying in %s seconds.",
                delay,
            )

            time.sleep(delay)

    logging.error(
        "Weather API failed after %s attempts.",
        max_retries,
    )

    print("Error: Unable to fetch weather data after 3 attempts.")

    return None


def main():
    """Run the weather agent."""
    logging.info("Weather AI Agent started.")

    weather = get_weather()

    if weather is None:
        logging.error(
            "Agent stopped because weather data was unavailable."
        )
        return

    try:
        current = weather["current"]

        temperature = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        weather_code = current["weather_code"]

    except KeyError as error:
        logging.error("Missing weather data field: %s", error)
        print("Error: Weather response is missing required data.")
        return

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
