from sqlalchemy.orm import Session
import numpy as np
from . import models, schemas
from fastapi import HTTPException
import json


def get_loans(db: Session, user_id: int):
    return db.query(models.Loan).filter(models.Loan.owner).filter(models.User.id == user_id).all()


def get_loan_summary(db: Session, json_data):
    try:
        loan_record = \
            db.query(models.Loan).filter(models.Loan.owner).filter(models.User.id == json_data.user_id).all()[
                (json_data.loan_id - 1)]
    except:
        raise HTTPException(status_code=404, detail="Item not found")

    if json_data.month <=loan_record.loanTerm:
        pass
    else:
        raise HTTPException(status_code=404, detail="Enter Month is not valid")
    total_amount = loan_record.amount
    interest_rate = loan_record.annualInterestRate / 100
    interest_rate_per_month = interest_rate / 12
    loanTerm_per_year = (loan_record.loanTerm / 12) * 12
    new_item = dict()
    new_item['Principal_Balance'] = abs(
        np.ppmt(interest_rate_per_month, json_data.month, loanTerm_per_year, total_amount))
    new_item['interest_already_paid'] = abs(np.cumsum(
        np.ipmt(interest_rate_per_month, range(1, json_data.month + 1), loanTerm_per_year, total_amount))[-1])
    new_item['principal_amount_already_paid'] = abs(np.cumsum(
        np.ppmt(interest_rate_per_month, range(1, json_data.month + 1), loanTerm_per_year, total_amount))[-1])
    return new_item


def loan_schedule(db: Session, json_data):
    try:
        loan_record = \
            db.query(models.Loan).filter(models.Loan.owner).filter(models.User.id == json_data.user_id).all()[
                (json_data.loan_id - 1)]
    except:
        raise HTTPException(status_code=404, detail="Item not found")

    total_amount = loan_record.amount
    interest_rate = loan_record.annualInterestRate / 100
    interest_rate_per_month = interest_rate / 12
    loanTerm_per_year = (loan_record.loanTerm / 12) * 12
    principle_amount_pay = abs(np.ppmt(interest_rate_per_month, 1, loanTerm_per_year, total_amount))
    interest_amount_pay = abs(np.ipmt(interest_rate_per_month, 1, loanTerm_per_year, total_amount))
    principle_amount = principle_amount_pay + interest_amount_pay
    main_list = list()
    for amount in range(loan_record.loanTerm):
        new_item = dict()
        new_item['month'] = amount + 1
        if total_amount - (principle_amount - interest_amount_pay) > 0:
            remainig_amount = total_amount - (principle_amount - interest_amount_pay)
            new_item['Remaining_Balance'] = "%.2f" % round(remainig_amount, 2)
        else:
            new_item['Remaining_Balance'] = 0
            remainig_amount = 0
        new_item['Monthly_Payment'] = principle_amount - interest_amount_pay
        new_item['Monthly_Payment'] = "%.2f" % round(new_item['Monthly_Payment'], 2)
        interest_amount_pay = abs(np.ipmt(interest_rate_per_month, 1, loanTerm_per_year, remainig_amount))
        total_amount = remainig_amount
        main_list.append(new_item)
    return main_list


def create_loan(db: Session, loan: schemas.LoanCreate, user_id: int):
    if db.query(models.User).filter(models.User.id == user_id).first() is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_loan = models.Loan(**loan.dict())
    db.add(db_loan)
    db_loan.owner = [db.query(models.User).filter(models.User.id == user_id).first()]
    db.commit()
    db.refresh(db_loan)
    return db_loan


def share_loan(db: Session, loan, user_id: int):
    if db.query(models.User).filter(models.User.id == user_id).first() is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not [v for v in db.query(models.loan_user_table).all() if (user_id, loan) == v]:
        obj = models.loan_user_table.insert().values(user_id=user_id, loan_id=loan)
        db.execute(obj)
        db.commit()
        return True
    return False
