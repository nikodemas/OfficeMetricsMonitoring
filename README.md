# Sensor Metrics Service

This project fetches temperature and pressure metrics from ESP322 sensor and open-meteo API and pushes them to a Prometheus Pushgateway. It runs as a service on Kubernetes.

## Structure

- `main.py`: Driver script.
- `sensor_query.py`: Module to fetch sensor data.
- `weather_query.py`: Module to fetch weather data.
- `pushgateway_client.py`: Module to push metrics to Prometheus Pushgateway.
- `Dockerfile`: Dockerfile to build the image.
- `requirements.txt`: Python dependencies.
- `kubernetes/`: Directory containing Kubernetes manifests.
  - `config.yaml.example`: Secret and ConfigMap example file for environment variables.
  - `sensor-metrics.yaml`: Deployment configuration for Kubernetes.

## Setup

### Running on Kubernetes

- Deploy `config.yaml` from [GitLab](https://gitlab.cern.ch/tunikode/OfficeMetricsMonitoring/). 
- Deploy `sensor-metrics.yaml` to create a pod and start the application.

### Running locally

```shell
# install dependencies
pip install -r requirements.txt

# set up environment variables
export SENSOR_TEMP_URL=http://url
...

# run the service
python main.py
```
