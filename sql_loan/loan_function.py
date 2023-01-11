from sqlalchemy.orm import Session
import numpy as np
from . import models, schemas
from fastapi import HTTPException


def get_loans(db: Session, user_id: int):
    return db.query(models.Loan).filter(models.Loan.owner_id == user_id).all()


def get_loan_summary(db: Session, json_data):
    loan_record = db.query(models.Loan).filter(models.Loan.owner_id == json_data.get("user_id")).all()[
        (json_data.get('loan_id') - 1)]
    total_amont = loan_record.amount
    interest_rate = loan_record.annualInterestRate / 100
    interest_rate_per_month = interest_rate / 12
    loanTerm_per_year = (loan_record.loanTerm / 12) * 12
    new_item = dict()
    new_item['Principal_Balance'] = abs(
        np.ppmt(interest_rate_per_month, json_data.get('month'), loanTerm_per_year, total_amont))
    new_item['interest_already_paid'] = abs(np.cumsum(
        np.ipmt(interest_rate_per_month, range(1, json_data.get('month') + 1), loanTerm_per_year, total_amont))[-1])
    new_item['principal_amount_already_paid'] = abs(np.cumsum(
        np.ppmt(interest_rate_per_month, range(1, json_data.get('month') + 1), loanTerm_per_year, total_amont))[-1])
    return new_item


def create_loan(db: Session, loan: schemas.LoanCreate, user_id: int):
    if db.query(models.User).filter(models.User.id == user_id).first() is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_loan = models.Loan(**loan.dict(), owner_id=user_id)
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan
