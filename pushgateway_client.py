from prometheus_client import CollectorRegistry, Gauge, push_to_gateway


def push_metrics_to_pushgateway(
    pushgateway_url,
    metric_name,
    metric_value,
    metric_type,
    sensor_name=None,
    office=None,
):
    registry = CollectorRegistry()
    labels = {"type": metric_type}
    if sensor_name:
        labels["sensor"] = sensor_name
    if office:
        labels["office"] = office

    gauge = Gauge(
        metric_name, "Metrics of the sensor", list(labels.keys()), registry=registry
    )
    gauge.labels(**labels).set(metric_value)

    push_to_gateway(
        pushgateway_url,
        job=metric_name,
        grouping_key=labels,
        registry=registry,
    )
