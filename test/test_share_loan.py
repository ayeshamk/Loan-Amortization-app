from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_loanshare():
    response = client.post("/loanshare/", json={"sender_id": 15, "receiver_id": 2, "loan_id": 2})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Item not found'}


def test_loanshare1():
    response = client.post("/loanshare/", json={"sender_id": 1, "receiver_id": 2, "loan_id": 1})
    assert response.status_code == 200
    assert response.json() is True


