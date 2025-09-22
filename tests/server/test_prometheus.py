import pytest
from fastapi.testclient import TestClient
from prometheus_client.parser import text_string_to_metric_families
from server.run import app  

client = TestClient(app)


def test_error_400_metrics():
    response = client.get("/error400")
    assert response.status_code == 400

    metrics_text = client.get("/metrics").text
    parsed_metrics = {m.name: m for m in text_string_to_metric_families(metrics_text)}
    http_responses = parsed_metrics["ml_app_http_responses"]

    found = any(
        sample.labels.get("status") == "400" and sample.labels.get("endpoint") == "error400"
        for sample in http_responses.samples
    )
    assert found, "Metrics not found for status code 400"


def test_error_500_metrics():
    with pytest.raises(RuntimeError):
        client.get("/error500")

    metrics_text = client.get("/metrics").text
    parsed_metrics = {m.name: m for m in text_string_to_metric_families(metrics_text)}
    http_responses = parsed_metrics["ml_app_http_responses"]

    found = any(
        sample.labels.get("status") == "500" and sample.labels.get("endpoint") == "error500"
        for sample in http_responses.samples
    )
    assert found, "Metrics not found for status code 500"
