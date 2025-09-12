import pytest
from fastapi.testclient import TestClient
from server.run import app


client = TestClient(app)


sample_data = [
    {
        "TransactionID": "TX000001",
        "AccountID": "AC001",
        "TransactionAmount": 100.0,
        "TransactionDate": "2023-04-11T16:29:14", 
        "TransactionType": "Credit",  
        "Location": "Houston",
        "DeviceID": "D00001",
        "IPAddress": "200.13.225.150",
        "MerchantID": "M001",
        "Channel": "Online", 
        "CustomerAge": 30,
        "CustomerOccupation": "Student",  
        "TransactionDuration": 10,
        "LoginAttempts": 1,
        "AccountBalance": 1000.0,
        "PreviousTransactionDate": "2023-04-01T16:29:14"
    }
]


def test_get_models():
    response = client.get("/models/")
    assert response.status_code == 200
    data = response.json()
    assert "available_models" in data
    assert isinstance(data["available_models"], list)
    assert "Isolation Forest" in data["available_models"]
    assert "Local Outlier Factor" in data["available_models"]


@pytest.mark.parametrize("model_name", ["isolation_forest", "local_outlier_factor"])
def test_predict_single_model(model_name):
    response = client.post(f"/models/{model_name}/predict", json=list(sample_data))
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "isFraud" in data[0]


def test_predict_both_models():
    response = client.post("/models/predict", json=list(sample_data))
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "isFraud" in data[0]
    assert "if_pred" in data[0]
    assert "lof_pred" in data[0]


def test_invalid_model_name():
    response = client.post("/models/invalid_model/predict", json=list(sample_data))
    assert response.status_code == 422
