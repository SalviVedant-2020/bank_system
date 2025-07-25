from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey("loans.id"))
    amount_paid = Column(Float)
    payment_date = Column(DateTime, default=datetime.utcnow)
    payment_type = Column(String, nullable=False)  # "EMI" or "LUMP SUM"
    loan = relationship("Loan", back_populates="payments")

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    balance = Column(Float)
    loans = relationship("Loan", back_populates="customer")

class Loan(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    amount = Column(Float)
    interest_rate = Column(Float)
    loan_period = Column(Integer)
    total_interest = Column(Float)
    total_amount = Column(Float)
    emi = Column(Float)
    emi_left = Column(Integer)
    payments = relationship("Payment", back_populates="loan")
    customer = relationship("Customer", back_populates="loans")
    transactions = relationship("Transaction", back_populates="loan")

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    loan_id = Column(Integer, ForeignKey('loans.id'))
    date = Column(DateTime, default=datetime.utcnow)
    amount = Column(Float)
    type = Column(String) 
    loan = relationship("Loan", back_populates="transactions")
