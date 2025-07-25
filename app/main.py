from fastapi import FastAPI
from app.routers import customer, loan, payment, summary  

app = FastAPI()

app.include_router(customer.router)
app.include_router(loan.router)
app.include_router(payment.router)
app.include_router(summary.router)  