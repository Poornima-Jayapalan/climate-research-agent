import requests

BASE_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(lat: float, lon: float):
    """
    Fetch current weather + short-term forecast from Open-Meteo.
    """

    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    return response.json()


def format_weather(data: dict) -> str:
    """Convert API response into readable text."""

    current = data.get("current_weather", {})
    daily = data.get("daily", {})

    if not current:
        return "Weather data unavailable."

    output = []

    # Current weather
    output.append("🌤️ Current Weather:")
    output.append(f"- Temperature: {current.get('temperature')} °C")
    output.append(f"- Wind Speed: {current.get('windspeed')} km/h")
    output.append(f"- Time: {current.get('time')}")

    # Forecast
    dates = daily.get("time", [])
    max_temps = daily.get("temperature_2m_max", [])
    min_temps = daily.get("temperature_2m_min", [])
    precipitation = daily.get("precipitation_sum", [])

    if dates:
        output.append("\n📅 Forecast:")
        for i in range(min(5, len(dates))):  # next 5 days
            output.append(
                f"- {dates[i]} | 🌡️ {min_temps[i]}–{max_temps[i]} °C | 🌧️ {precipitation[i]} mm"
            )

    return "\n".join(output)