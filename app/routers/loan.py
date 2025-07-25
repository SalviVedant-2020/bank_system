from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import LoanCreate
from app.database import get_db
from app.models import Loan, Customer, Payment

router = APIRouter()

@router.post("/create_loan")
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    print("loan: ", loan)
    customer = db.query(Customer).filter(Customer.id == loan.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    principal = loan.amount
    rate = loan.interest_rate
    time = loan.loan_period / 12

    total_interest = (principal * rate * time) / 100
    total_amount = principal + total_interest
    emi = total_amount / loan.loan_period
    print(principal,total_amount, emi)

    new_loan = Loan(
        customer_id=loan.customer_id,
        amount=principal,
        interest_rate=rate,
        loan_period=loan.loan_period,
        total_interest=total_interest,
        total_amount=total_amount,
        emi=emi,
        emi_left=loan.loan_period
    )

    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)

    return {
        "message": "Loan created successfully",
        "loan_id": new_loan.id,
        "customer_id": loan.customer_id,
        "principal": principal,
        "total_interest": total_interest,
        "total_amount": total_amount,
        "emi": emi
    }



@router.get("/loans/{loan_id}/ledger")
def get_loan_ledger(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found.")

    # Fetch all transactions (EMI + Lump Sum)
    payments = db.query(Payment).filter(Payment.loan_id == loan_id).order_by(Payment.payment_date).all()

    total_paid = sum([p.amount_paid for p in payments])
    balance = loan.total_amount

    # Count EMI payments (only payments where payment_type == 'EMI')
    emi_payments = [p for p in payments if p.payment_type.upper() == 'EMI']
    emi_left = loan.emi_left

    return {
        "loan_id": loan.id,
        "customer_id": loan.customer_id,
        "original_amount": loan.amount,
        "interest_rate": loan.interest_rate,
        "loan_period": loan.loan_period,
        "monthly_emi": round(loan.emi, 2),
        "total_amount_to_be_paid": round(loan.total_amount, 2),
        "total_paid": round(total_paid, 2),
        "balance": round(balance, 2),
        "emi_left": emi_left,
        "transactions": [
            {
                "payment_id": p.id,
                "amount_paid": p.amount_paid,
                "payment_date": p.payment_date,
                "payment_type": p.payment_type
            }
            for p in payments
        ]
    }
