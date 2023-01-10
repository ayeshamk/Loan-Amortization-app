
import uvicorn
from typing import List
import json
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql_loan import schemas, user_functions, models,loan_function
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


@app.get("/users/", response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db)):
    users = user_functions.get_user(db)
    return users



@app.post("/users/{user_id}/loans/", response_model=schemas.Loan)
def create_loan_for_user(
        user_id: int, loan: schemas.LoanCreate, db: Session = Depends(get_db)):
    return loan_function.create_loan(db=db, loan=loan, user_id=user_id)


@app.get("/loans/{user_id}", response_model=List[schemas.Loan])
def read_loan(user_id:int,db: Session = Depends(get_db)):
    loan = loan_function.get_loans(db, user_id)
    return loan

if __name__ == '__main__':
    uvicorn.run(app, port=8000)
