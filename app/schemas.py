from pydantic import BaseModel
from datetime import date
from typing import Optional

# Existing LoanCreate schema
class LoanCreate(BaseModel):
    customer_id: int
    amount: float
    interest_rate: float  
    loan_period: int   

# PaymentRequest schema
class PaymentRequest(BaseModel):
    loan_id: int
    amount: float
    payment_date: Optional[date] = None  # Optional; defaults to today if not given
    payment_type: str  # "EMI" or "LUMP_SUM"

class LoanRequest(BaseModel):
    loan_id: int
    customer_id: int
    amount: float
    request_type: str  # "EMI" or "TOPUP"
    request_date: Optional[date] = None

class CustomerCreate(BaseModel):
    name: str
    email: str
    balance: float
