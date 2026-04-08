import requests
import pandas as pd

POWER_URL = "https://power.larc.nasa.gov/api/temporal/monthly/point"


def get_climate_data(
    lat: float,
    lon: float,
    start_year: int = 2000,
    end_year: int = 2020,
):
    """
    Fetch climate data from NASA POWER API.

    Returns monthly temperature & precipitation.
    """

    params = {
        "parameters": "T2M,PRECTOT",
        "community": "RE",
        "longitude": lon,
        "latitude": lat,
        "start": start_year,
        "end": end_year,
        "format": "JSON",
    }

    response = requests.get(POWER_URL, params=params)
    response.raise_for_status()

    data = response.json()

    try:
        param_data = data["properties"]["parameter"]

        temp = param_data["T2M"]
        precip = param_data["PRECTOT"]

        df = pd.DataFrame({
            "date": list(temp.keys()),
            "temperature": list(temp.values()),
            "precipitation": list(precip.values()),
        })

        return df

    except KeyError:
        raise ValueError("Unexpected API response format")


def summarize_climate(df: pd.DataFrame) -> str:
    """Generate a simple climate summary."""

    avg_temp = df["temperature"].mean()
    total_precip = df["precipitation"].sum()

    return (
        f"Average Temperature: {avg_temp:.2f} °C\n"
        f"Total Precipitation: {total_precip:.2f} mm"
    )