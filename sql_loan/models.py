from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .database import Base

loan_user_table = Table(
    "user_loan",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("loan_id", Integer, ForeignKey("loans.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    name = Column(String)
    is_active = Column(Boolean, default=True)

    loans = relationship("Loan", back_populates="owner", secondary=loan_user_table)


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, index=True)
    annualInterestRate = Column(Integer, index=True)
    loanTerm = Column(Integer, index=True)
    # owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="loans", secondary=loan_user_table)
