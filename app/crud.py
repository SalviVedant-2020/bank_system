from sqlalchemy.orm import Session
from . import models, schemas

def create_loan(db: Session, request: schemas.LoanRequest):
    P = request.principal
    N = request.loan_period
    R = request.interest_rate

    I = (P * N * R) / 100
    A = P + I
    months = N * 12
    emi = round(A / months, 2)

    loan = models.Loan(
        customer_id=request.customer_id,
        principal=P,
        interest_rate=R,
        loan_period=N,
        total_interest=I,
        total_amount=A,
        emi=emi,
        emi_left=months
    )
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return {"loan_id": loan.id, "total_amount": A, "monthly_emi": emi}

def make_payment(db: Session, payment: schemas.PaymentRequest):
    loan = db.query(models.Loan).filter(models.Loan.id == payment.loan_id).first()
    if not loan:
        return {"error": "Loan not found"}

    loan.total_amount -= payment.amount
    if payment.type == "EMI":
        loan.emi_left = max(loan.emi_left - 1, 0)
    else:
        emi_reduction = int(payment.amount // loan.emi)
        loan.emi_left = max(loan.emi_left - emi_reduction, 0)

    txn = models.Transaction(loan_id=loan.id, amount=payment.amount, type=payment.type)
    db.add(txn)
    db.commit()
    return {"status": "Payment Recorded"}

def get_ledger(db: Session, loan_id: int):
    loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    txns = loan.transactions
    return {
        "transactions": [{"date": t.date, "amount": t.amount, "type": t.type} for t in txns],
        "balance": loan.total_amount,
        "emi": loan.emi,
        "emi_left": loan.emi_left
    }

def get_account_overview(db: Session, customer_id: int):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        return {"error": "Customer not found"}

    loans_info = []
    for loan in customer.loans:
        paid = sum([t.amount for t in loan.transactions])
        loans_info.append({
            "loan_id": loan.id,
            "principal": loan.principal,
            "total_amount": loan.total_amount,
            "interest": loan.total_interest,
            "emi": loan.emi,
            "paid": paid,
            "emi_left": loan.emi_left
        })

    return {"customer_id": customer.id, "loans": loans_info}
