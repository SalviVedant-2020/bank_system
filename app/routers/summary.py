from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Loan, Payment

router = APIRouter()

@router.get("/customers/{customer_id}/summary")
def loan_summary(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found.")

    total_paid = db.query(Payment).filter(Payment.loan_id == loan_id).with_entities(Payment.amount_paid).all()
    total_paid_sum = sum([p.amount_paid for p in total_paid])

    balance = (loan.amount * (1 + (loan.interest_rate / 100))) - total_paid_sum

    return {
        "loan_id": loan.id,
        "customer_id": loan.customer_id,
        "amount": loan.amount,
        "interest_rate": loan.interest_rate,
        "loan_period": loan.loan_period,
        "total_paid": total_paid_sum,
        "balance": round(balance, 2)
    }
