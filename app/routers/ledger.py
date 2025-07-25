from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, database

router = APIRouter()

@router.get("/ledger/{loan_id}")
def ledger(loan_id: int, db: Session = Depends(database.SessionLocal)):
    return crud.get_ledger(db, loan_id)
