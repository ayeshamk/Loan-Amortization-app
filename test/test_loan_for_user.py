from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_loan_for_user():
    response = client.get("/loans/2")
    assert response.status_code == 200
    assert response.json() == [{'amount': 18000, 'loanTerm': 10, 'annualInterestRate': 6, 'id': 1},
                               {'amount': 18000, 'loanTerm': 10, 'annualInterestRate': 6, 'id': 2},
                               {'amount': 18000, 'loanTerm': 10, 'annualInterestRate': 6, 'id': 3}]


def test_get_loan_for_user1():
    response = client.get("/loans/1")
    assert response.status_code == 200
    assert response.json() == []
