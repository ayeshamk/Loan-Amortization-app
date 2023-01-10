from typing import List, Union

from pydantic import BaseModel


class LoanBase(BaseModel):
    amount: int
    annualInterestRate: int
    loanTerm: int


class LoanCreate(LoanBase):
    pass


class Loan(LoanBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    loans: List[Loan] = []

    class Config:
        orm_mode = True
