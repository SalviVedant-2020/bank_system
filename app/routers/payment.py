from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Payment, Loan
from app.schemas import PaymentRequest
from datetime import datetime
from typing import List
from math import ceil

router = APIRouter()

@router.get("/get_payments/{loan_id}")
def get_payments(loan_id: int, db: Session = Depends(get_db)):
    payments = db.query(Payment).filter(Payment.loan_id == loan_id).all()
    if not payments:
        raise HTTPException(status_code=404, detail="No payments found for this loan.")
    return payments



@router.post("/make_payment")
def make_payment(payment: PaymentRequest, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == payment.loan_id).first()

    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    if loan.emi_left <= 0 or loan.total_amount <= 0:
        raise HTTPException(status_code=400, detail="Loan is already paid off")

    # Add payment record
    new_payment = Payment(
        loan_id=payment.loan_id,
        amount_paid=payment.amount,
        payment_date=datetime.utcnow(),
        payment_type='LUMP_SUM' if payment.payment_type=='lump_sum' else 'EMI'
    )
    db.add(new_payment)

    # Handle EMI or LUMP SUM
    if payment.payment_type == "emi":
        if abs(payment.amount - loan.emi) > 1:
            raise HTTPException(status_code=400, detail=f"EMI must be {loan.emi}")
        loan.emi_left -= 1
        loan.total_amount -= loan.emi
    elif payment.payment_type == "lump_sum":
        if payment.amount > loan.total_amount:
            raise HTTPException(status_code=400, detail="Payment exceeds total amount")
        loan.total_amount -= payment.amount
        loan.emi_left = ceil(loan.total_amount / loan.emi) if loan.total_amount > 0 else 0
    else:
        raise HTTPException(status_code=400, detail="Invalid payment type. Must be 'emi' or 'lump_sum'")

    db.commit()
    db.refresh(loan)

    return {
        "message": "Payment successful",
        "remaining_amount": loan.total_amount,
        "emi_left": loan.emi_left
    }