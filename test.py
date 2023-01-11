from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_user():
    response = client.post("/users/", json={"email": "newuser5@admin.com", "name": "user5", "password": "test432"})
    assert response.status_code == 200


def test_create_loan():
    response = client.post("/users/3/loans/", json={"amount": 18000, "annualInterestRate": 6, "loanTerm": 10})
    assert response.status_code == 200


def get_summary_report():
    response = client.post("/loan_summary/", json={"user_id": 2, "loan_id": 1, "month": 5})
    assert response.status_code == 200


def get_loan_for_user():
    response = client.get("/loans/1}")
    assert response.status_code == 200


def loanshare():
    response = client.post("/loanshare/", json={"sender_id": 15, "receiver_id": 2, "loan_id": 2})
    assert response.status_code == 200


def get_loan_schedule():
    response = client.post("/loan_schedule/", json={"user_id": 12, "loan_id": 1})
    assert response.status_code == 200
