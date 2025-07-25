from fastapi import APIRouter, HTTPException, Request
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import get_db
from fastapi import Depends

router = APIRouter()

@router.post("/lend")
def create_loan(data: schemas.LoanCreate, request: Request = None, db: Session = Depends(get_db)):
    try:
        # Check if customer exists
        customer = db.query(models.Customer).filter(models.Customer.id == data.customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        # Calculate total amount and EMI
        total_amount = data.loan_amount * (1 + (data.loan_period * data.interest_rate / 100))
        monthly_emi = total_amount / (data.loan_period * 12)

        # Create loan entry
        loan = models.Loan(
            customer_id=data.customer_id,
            loan_amount=data.loan_amount,
            loan_period=data.loan_period,
            interest_rate=data.interest_rate,
            total_amount=total_amount,
            monthly_emi=monthly_emi
        )
        db.add(loan)
        db.commit()
        db.refresh(loan)

        return {
            "loan_id": loan.id,
            "total_amount": loan.total_amount,
            "monthly_emi": loan.monthly_emi
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
