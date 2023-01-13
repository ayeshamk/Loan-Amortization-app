import uvicorn
from typing import List
from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session

from sql_loan import schemas, user_functions, models, loan_function
from sql_loan.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_functions.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_functions.create_user(db=db, user=user)


@app.post("/users/{user_id}/loans/")
def create_loan_for_user(
        user_id: int, loan: schemas.LoanCreate, db: Session = Depends(get_db)):
    return loan_function.create_loan(db=db, loan=loan, user_id=user_id)


@app.post("/loan_summary/")
def get_loan_summary(request: Request,loan:schemas.LoanSummary, db: Session = Depends(get_db)):
    summary = loan_function.get_loan_summary(db, loan)
    return summary


@app.post("/loan_schedule/")
def get_loan_schedule(loan: schemas.LoanSchedule, db: Session = Depends(get_db)):
    schedule = loan_function.loan_schedule(db, loan)
    return schedule


@app.get("/loans/{user_id}")
def read_loan(user_id: int, db: Session = Depends(get_db)):
    loan = loan_function.get_loans(db, user_id)
    return loan


@app.post("/loanshare/")
def user_loan_share(json_data: schemas.ShareLoan, db: Session = Depends(get_db)):
    try:
        loan_id = db.query(models.Loan).filter(models.Loan.owner).filter(models.User.id == json_data.sender_id).all()[
                (json_data.loan_id - 1)].id
    except Exception as e:
        raise HTTPException(status_code=404, detail="Item not found")

    return loan_function.share_loan(db=db, loan=loan_id, user_id=json_data.receiver_id)


if __name__ == '__main__':
    uvicorn.run(app, port=8000)
