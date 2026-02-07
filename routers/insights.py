from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime

from database import get_db
from models import Transaction
from routers.auth_utils import get_current_user

router = APIRouter(
    prefix="/insights",
    tags=["Insights"]
)

# =========================
# 1. CASH FLOW
# =========================
@router.get("/cash-flow")
def cash_flow(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.txn_type == "credit"
    ).scalar() or 0

    expense = db.query(func.sum(Transaction.amount)).filter(
        Transaction.txn_type == "debit"
    ).scalar() or 0

    return {
        "total_income": income,
        "total_expense": expense,
        "net_cash_flow": income - expense
    }


# =========================
# 2. BURN RATE (AVG MONTHLY SPEND)
# =========================
@router.get("/burn-rate")
def burn_rate(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    monthly = db.query(
        extract("month", Transaction.created_at).label("month"),
        func.sum(Transaction.amount).label("total")
    ).filter(
        Transaction.txn_type == "debit"
    ).group_by("month").all()

    if not monthly:
        return {"average_monthly_burn": 0}

    avg = sum(m.total for m in monthly) / len(monthly)
    return {"average_monthly_burn": avg}


# =========================
# 3. TOP SPENDING CATEGORIES
# =========================
@router.get("/top-spending")
def top_spending(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    results = db.query(
        Transaction.category,
        func.sum(Transaction.amount).label("total")
    ).filter(
        Transaction.txn_type == "debit"
    ).group_by(Transaction.category).order_by(
        func.sum(Transaction.amount).desc()
    ).limit(5).all()

    return [
        {"category": r.category, "amount": r.total}
        for r in results
    ]


# =========================
# 4. MONTHLY SPENDING
# =========================
@router.get("/monthly-spending")
def monthly_spending(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    results = db.query(
        extract("year", Transaction.created_at).label("year"),
        extract("month", Transaction.created_at).label("month"),
        func.sum(Transaction.amount).label("total")
    ).filter(
        Transaction.txn_type == "debit"
    ).group_by("year", "month").all()

    return [
        {
            "year": int(r.year),
            "month": int(r.month),
            "amount": r.total
        }
        for r in results
    ]
