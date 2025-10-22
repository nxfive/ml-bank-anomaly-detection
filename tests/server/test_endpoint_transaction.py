from fastapi.testclient import TestClient
from services.server.run import app  


client = TestClient(app)


def test_get_all_transactions():
    response = client.get("/transactions/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "AccountID" in data[0]  


def test_get_transactions_by_account_id():
    response_all = client.get("/transactions/")
    account_id = response_all.json()[0]["AccountID"]
    response = client.get(f"/transactions/{account_id}")
    assert response.status_code == 200
    data = response.json()
    assert all(d["AccountID"] == account_id for d in data)


def test_get_transactions_invalid_account():
    response = client.get("/transactions/INVALID_ACCOUNT")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Account ID not found"
