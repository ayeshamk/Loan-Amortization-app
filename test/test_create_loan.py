from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_loan1():
    response = client.post("/users/12/loans/", json={"amount": 18000, "annualInterestRate": 6, "loanTerm": 10})
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_create_loan2():
    response = client.post("/users/2/loans/", json={"amount": 18000, "annualInterestRate": 6, "loanTerm": 10})
    assert response.status_code == 200
    # it will fail cause every time id will increase
    assert response.json() == {'amount': 18000, 'loanTerm': 10, 'annualInterestRate': 6, 'id': 2}



