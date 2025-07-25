from app.models import Loan, Payment
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter()

@router.post("/create_customer")
def create_customer(data: schemas.CustomerCreate, db: Session = Depends(database.get_db)):
    new_customer = models.Customer(**data.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return {"message": "Customer created successfully", "customer_id": new_customer.id}


@router.get("/customers/{customer_id}/account-overview")
def account_overview(customer_id: int, db: Session = Depends(database.get_db)):
    loans = db.query(Loan).filter(Loan.customer_id == customer_id).all()
    if not loans:
        raise HTTPException(status_code=404, detail="No loans found for this customer.")

    response = []

    for loan in loans:
        payments = db.query(Payment).filter(Payment.loan_id == loan.id).all()
        total_paid = sum([p.amount_paid for p in payments])

        # EMI-based payments only
        emi_payments = [p for p in payments if p.payment_type and p.payment_type.upper() == "EMI"]
        emi_paid_count = len(emi_payments)
        emi_left = loan.emi_left

        response.append({
            "loan_id": loan.id,
            "principal_amount": round(loan.amount, 2),
            "total_interest": round(loan.total_interest, 2),
            "total_amount": round(loan.total_amount, 2),
            "emi_amount": round(loan.emi, 2),
            "total_paid_till_date": round(total_paid, 2),
            "emi_left": emi_left
        })

    return {
        "customer_id": customer_id,
        "loans": response
    }