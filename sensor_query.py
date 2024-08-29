import requests


def get_sensor_data(url, username, password):
    response = requests.get(url, auth=(username, password))
    response.raise_for_status()
    return response.json()
