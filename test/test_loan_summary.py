from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_summary_report():
    response = client.post("/loan_summary/", json={"user_id": 2, "loan_id": 1, "month": 5})
    assert response.status_code == 200
    assert response.json() == {'Principal_Balance': 1795.3325772217222, 'interest_already_paid': 361.5654159312165,
                               'principal_amount_already_paid': 8887.786131324821}


def test_get_summary_report1():
    response = client.post("/loan_summary/", json={"user_id": 1, "loan_id": 15, "month": 2})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Item not found'}


def test_get_summary_report3():
    response = client.post("/loan_summary/", json={"user_id": 1, "loan_id": 1, "month": 55})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Enter Month is not valid'}

