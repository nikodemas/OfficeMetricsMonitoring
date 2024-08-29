import os
import time

import requests

from pushgateway_client import push_metrics_to_pushgateway
from sensor_query import get_sensor_data
from weather_query import get_weather_data

# Configuration for the sensor metrics
SENSOR_URLS = {
    'temperature': os.getenv('SENSOR_TEMP_URL'),
    'pressure': os.getenv('SENSOR_PRESS_URL')
}
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

# Latitude and longitude of the location for weather data
LATITUDE = os.getenv('LATITUDE')
LONGITUDE = os.getenv('LONGITUDE')

PUSHGATEWAY_URL = os.getenv('PUSHGATEWAY_URL')
POLL_INTERVAL = int(os.getenv('POLL_INTERVAL', 60))  # Polling interval in seconds, default is 60 seconds


def fetch_and_push_sensor_data():
    for metric_type, url in SENSOR_URLS.items():
        try:
            data = get_sensor_data(url, USERNAME, PASSWORD)
            print(f"Fetched {metric_type} data: {data}", flush=True)
            push_metrics_to_pushgateway(PUSHGATEWAY_URL, 'sensor_metrics', data['value'], metric_type)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {metric_type} data: {e}", flush=True)
        except Exception as e:
            print(f"Error pushing {metric_type} metrics: {e}", flush=True)


def fetch_and_push_weather_data():
    try:
        temperature, pressure = get_weather_data(LATITUDE, LONGITUDE)
        if temperature is not None:
            print(f"Fetched weather temperature: {temperature} °C", flush=True)
            push_metrics_to_pushgateway(PUSHGATEWAY_URL, 'weather_metrics', temperature, 'temperature')
        if pressure is not None:
            print(f"Fetched weather pressure: {pressure} hPa", flush=True)
            push_metrics_to_pushgateway(PUSHGATEWAY_URL, 'weather_metrics', pressure, 'pressure')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}", flush=True)
    except Exception as e:
        print(f"Error pushing weather metrics: {e}", flush=True)


def run_service():
    while True:
        fetch_and_push_sensor_data()
        fetch_and_push_weather_data()

        print(f"Metrics pushed to Pushgateway at {PUSHGATEWAY_URL}", flush=True)
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    run_service()
