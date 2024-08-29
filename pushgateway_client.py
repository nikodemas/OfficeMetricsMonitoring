from prometheus_client import CollectorRegistry, Gauge, push_to_gateway


def push_metrics_to_pushgateway(pushgateway_url, metric_name, metric_value, metric_type):
    registry = CollectorRegistry()
    gauge = Gauge(metric_name, 'Metrics of the sensor', ['type'], registry=registry)
    gauge.labels(type=metric_type).set(metric_value)

    push_to_gateway(
        pushgateway_url,
        job=metric_name,
        grouping_key={'sensor': 'esp32', 'type': metric_type},
        registry=registry
    )
