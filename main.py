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
async def get_loan_summary(request: Request, db: Session = Depends(get_db)):
    json_data = await request.json()
    summary = loan_function.get_loan_summary(db, json_data)
    return summary


@app.post("/loan_schedule/")
async def get_loan_schedule(request: Request, db: Session = Depends(get_db)):
    json_data = await request.json()
    schedule = loan_function.loan_schedule(db, json_data)
    return schedule


@app.get("/loans/{user_id}")
def read_loan(user_id: int, db: Session = Depends(get_db)):
    loan = loan_function.get_loans(db, user_id)
    return loan


@app.post("/loanshare/")
async def user_loan_share(request: Request, db: Session = Depends(get_db)):
    json_data = await request.json()
    try:
        loan_id = \
            db.query(models.Loan).filter(models.Loan.owner).filter(models.User.id == json_data.get('sender_id')).all()[
                (json_data.get('loan_id') - 1)].id
    except HTTPException:
        raise HTTPException(status_code=404, detail="Item not found")

    return loan_function.share_loan(db=db, loan=loan_id, user_id=json_data['receiver_id'])


if __name__ == '__main__':
    uvicorn.run(app, port=8000)
