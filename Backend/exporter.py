from prometheus_client import (
    CollectorRegistry,
    generate_latest,
    CONTENT_TYPE_LATEST,
    disable_created_metrics,
    Counter,
    Gauge,
    Histogram,
    Summary
)


# disabling creation of default metrics
disable_created_metrics()
# creating custom registry
registry = CollectorRegistry()


def metrics():
    return generate_latest(registry=registry), 200


http_requests_total = Counter(
    "http_requests_total",
    "Total received http requests",
    ["status", "path", "method"],
    registry=registry
)

active_requests = Gauge(
    "active_requests",
    "Number of users already using web application",
    ["path", "method"],
    registry=registry
)

request_duration = Summary(
    "request_duration",
    "summary of requests' duration",
    ["status", "path", "method"],
    registry=registry
)

requests_duration_distribution = Histogram(
    "requests_duration_distribution",
    "distribution of requests' living period",
    ["status", "path", "method"],
    registry=registry
)
