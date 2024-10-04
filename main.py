import json
import logging
import os
import time

import requests

from pushgateway_client import push_metrics_to_pushgateway
from sensor_query import get_sensor_data
from weather_query import get_weather_data

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)


def load_config():
    # Configuration for the sensor metrics
    sensor_config = json.loads(os.getenv("SENSOR_CONFIG"))
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    # Latitude and longitude of the location for weather data
    weather_config = {
        "latitude": os.getenv("LATITUDE"),
        "longitude": os.getenv("LONGITUDE"),
    }

    pushgateway_url = os.getenv("PUSHGATEWAY_URL")

    # Polling interval in seconds, default is 60 seconds
    poll_interval = int(os.getenv("POLL_INTERVAL", 60))

    return (
        sensor_config,
        username,
        password,
        weather_config,
        pushgateway_url,
        poll_interval,
    )


def fetch_and_push_sensor_data(sensor_config, username, password, pushgateway_url):
    for sensor_name, sensor_data in sensor_config.items():
        office = sensor_data["office"]
        for metric_type, url in sensor_data["sensor_urls"].items():
            try:
                data = get_sensor_data(url, username, password)
                logging.info(
                    f"Fetched inside {metric_type} from "
                    f"sensor {sensor_name} in {office}: {data['value']}"
                )
                push_metrics_to_pushgateway(
                    pushgateway_url,
                    "sensor_metrics",
                    data["value"],
                    metric_type,
                    sensor_name,
                    office,
                )
            except requests.exceptions.RequestException as e:
                logging.error(
                    f"Error fetching {metric_type} data from "
                    f"sensor {sensor_name} in {office}: {e}"
                )
            except Exception as e:
                logging.error(
                    f"Error pushing {metric_type} metrics from "
                    f"sensor {sensor_name} in {office}: {e}"
                )


def fetch_and_push_weather_data(weather_config, pushgateway_url):
    try:
        temperature, pressure = get_weather_data(
            weather_config["latitude"], weather_config["longitude"]
        )
        if temperature is not None:
            logging.info(f"Fetched outside temperature: {temperature}")
            push_metrics_to_pushgateway(
                pushgateway_url, "weather_metrics", temperature, "temperature"
            )
        if pressure is not None:
            logging.info(f"Fetched outside pressure: {pressure}")
            push_metrics_to_pushgateway(
                pushgateway_url, "weather_metrics", pressure, "pressure"
            )
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather data: {e}")
    except Exception as e:
        logging.error(f"Error pushing weather metrics: {e}")


def run_service():
    (
        sensor_config,
        weather_config,
        pushgateway_url,
        username,
        password,
        poll_interval,
    ) = load_config()
    while True:
        fetch_and_push_sensor_data(sensor_config, username, password, pushgateway_url)
        fetch_and_push_weather_data(weather_config, pushgateway_url)

        logging.info(f"Metrics pushed to Pushgateway at {pushgateway_url}")
        time.sleep(poll_interval)


if __name__ == "__main__":
    run_service()
