from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, database

router = APIRouter()

@router.get("/account/{customer_id}")
def account(customer_id: int, db: Session = Depends(database.SessionLocal)):
    return crud.get_account_overview(db, customer_id)
