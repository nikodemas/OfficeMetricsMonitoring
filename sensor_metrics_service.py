import os
import time
import requests
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

SENSOR_URLS = {
    'temperature': os.getenv('SENSOR_TEMP_URL'),
    'pressure': os.getenv('SENSOR_PRESS_URL')
}
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
PUSHGATEWAY_URL = os.getenv('PUSHGATEWAY_URL')
POLL_INTERVAL = int(os.getenv('POLL_INTERVAL', 10))  # Polling interval in seconds, default is 10 seconds

def get_sensor_data(url):
    response = requests.get(url, auth=(USERNAME, PASSWORD))
    response.raise_for_status()
    return response.json()

def push_metrics_to_pushgateway(metric_name, metric_value, metric_type):
    registry = CollectorRegistry()
    gauge = Gauge('sensor_metrics', 'Metrics of the sensor', ['type'], registry=registry)
    gauge.labels(type=metric_type).set(metric_value)
    
    push_to_gateway(
        PUSHGATEWAY_URL, 
        job='sensor_metrics', 
        grouping_key={'sensor': 'esp32', 'type': metric_type}, 
        registry=registry
    )

def run_service():
    while True:
        for metric_type, url in SENSOR_URLS.items():
            try:
                data = get_sensor_data(url)
                print(f"Fetched {metric_type} data: {data}", flush=True)
                push_metrics_to_pushgateway('sensor_metrics', data['value'], metric_type)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching {metric_type} data: {e}", flush=True)
            except Exception as e:
                print(f"Error pushing {metric_type} metrics: {e}", flush=True)
        
        print(f"Metrics pushed to Pushgateway at {PUSHGATEWAY_URL}", flush=True)
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    run_service()

