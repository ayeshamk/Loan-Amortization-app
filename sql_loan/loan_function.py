from sqlalchemy.orm import Session

from . import models,schemas
from fastapi import HTTPException


def get_loans(db: Session, user_id: int):
    return db.query(models.Loan).filter(models.Loan.owner_id == user_id).all()


def create_loan(db: Session, loan: schemas.LoanCreate, user_id: int):
    if db.query(models.User).filter(models.User.id == user_id).first() is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_loan = models.Loan(**loan.dict(), owner_id=user_id)
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan
