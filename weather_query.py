import openmeteo_requests


def get_weather_data(lat, long):
    params = {
        "latitude": lat,
        "longitude": long,
        "current": ["temperature_2m", "surface_pressure"],
    }
    url = "https://api.open-meteo.com/v1/forecast"

    om = openmeteo_requests.Client()
    responses = om.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    temperature = response.Current().Variables(0).Value()
    pressure = response.Current().Variables(1).Value()

    return temperature, pressure
