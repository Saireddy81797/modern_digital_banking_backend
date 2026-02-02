from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models import Bill
from schemas import BillCreate, BillUpdate, BillResponse
from routers.auth_utils import get_current_user

router = APIRouter(
    prefix="/bills",
    tags=["Bills"]
)

# =========================
# CREATE BILL
# =========================
@router.post("/", response_model=BillResponse)
def create_bill(
    bill: BillCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    new_bill = Bill(
        user_id=current_user.id,
        bill_name=bill.bill_name,
        amount=bill.amount,
        due_date=bill.due_date
    )

    db.add(new_bill)
    db.commit()
    db.refresh(new_bill)

    overdue = datetime.utcnow() > new_bill.due_date and not new_bill.is_paid

    return {
        **new_bill.__dict__,
        "overdue": overdue
    }


# =========================
# LIST ALL BILLS
# =========================
@router.get("/", response_model=list[BillResponse])
def list_bills(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    bills = db.query(Bill).filter(
        Bill.user_id == current_user.id
    ).all()

    response = []
    for bill in bills:
        overdue = datetime.utcnow() > bill.due_date and not bill.is_paid
        response.append({**bill.__dict__, "overdue": overdue})

    return response


# =========================
# UPDATE BILL (MARK PAID / EDIT)
# =========================
@router.put("/{bill_id}", response_model=BillResponse)
def update_bill(
    bill_id: int,
    bill_data: BillUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    bill = db.query(Bill).filter(
        Bill.id == bill_id,
        Bill.user_id == current_user.id
    ).first()

    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    if bill_data.bill_name is not None:
        bill.bill_name = bill_data.bill_name
    if bill_data.amount is not None:
        bill.amount = bill_data.amount
    if bill_data.due_date is not None:
        bill.due_date = bill_data.due_date
    if bill_data.is_paid is not None:
        bill.is_paid = bill_data.is_paid

    db.commit()
    db.refresh(bill)

    overdue = datetime.utcnow() > bill.due_date and not bill.is_paid

    return {
        **bill.__dict__,
        "overdue": overdue
    }


# =========================
# DELETE BILL
# =========================
@router.delete("/{bill_id}")
def delete_bill(
    bill_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    bill = db.query(Bill).filter(
        Bill.id == bill_id,
        Bill.user_id == current_user.id
    ).first()

    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    db.delete(bill)
    db.commit()
    return {"message": "Bill deleted successfully"}
