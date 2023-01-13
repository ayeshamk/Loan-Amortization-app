from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_loan_schedule():
    response = client.post("/loan_schedule/", json={"user_id": 1, "loan_id": 1})
    assert response.status_code == 200
    assert response.json() == [{'month': 1, 'Remaining_Balance': '16240.13', 'Monthly_Payment': '1759.87'},
                               {'month': 2, 'Remaining_Balance': '14471.46', 'Monthly_Payment': '1768.67'},
                               {'month': 3, 'Remaining_Balance': '12693.95', 'Monthly_Payment': '1777.51'},
                               {'month': 4, 'Remaining_Balance': '10907.55', 'Monthly_Payment': '1786.40'},
                               {'month': 5, 'Remaining_Balance': '9112.21', 'Monthly_Payment': '1795.33'},
                               {'month': 6, 'Remaining_Balance': '7307.90', 'Monthly_Payment': '1804.31'},
                               {'month': 7, 'Remaining_Balance': '5494.57', 'Monthly_Payment': '1813.33'},
                               {'month': 8, 'Remaining_Balance': '3672.18', 'Monthly_Payment': '1822.40'},
                               {'month': 9, 'Remaining_Balance': '1840.67', 'Monthly_Payment': '1831.51'},
                               {'month': 10, 'Remaining_Balance': 0, 'Monthly_Payment': '1840.67'}]


def test_get_loan_schedule1():
    response = client.post("/loan_schedule/", json={"user_id": 1, "loan_id": 61})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Item not found'}

