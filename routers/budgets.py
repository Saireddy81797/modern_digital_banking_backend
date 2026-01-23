from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from database import get_db
from models import Budget, Transaction
from schemas import BudgetCreate, BudgetResponse

# ✅ FIXED IMPORT
from routers.auth_utils import get_current_user


router = APIRouter(
    prefix="/budgets",
    tags=["Budgets"]
)

# =================================================
# A) CREATE BUDGET
# =================================================
@router.post("/", response_model=BudgetResponse)
def create_budget(
    budget: BudgetCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    new_budget = Budget(
        user_id=current_user.id,
        month=budget.month,
        year=budget.year,
        category=budget.category,
        limit_amount=budget.limit_amount
    )

    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)

    return new_budget


# =================================================
# B) LIST BUDGETS
# =================================================
@router.get("/", response_model=list[BudgetResponse])
def list_budgets(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(Budget).filter(
        Budget.user_id == current_user.id
    ).all()


# =================================================
# C) BUDGET PROGRESS + WARNING LOGIC 🔥🔥
# =================================================
@router.get("/progress", response_model=list[BudgetResponse])
def budget_progress(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    budgets = db.query(Budget).filter(
        Budget.user_id == current_user.id
    ).all()

    results = []

    for b in budgets:
    spent = db.query(func.sum(Transaction.amount)).filter(
        Transaction.category == b.category,
        Transaction.txn_type == "debit",
        extract("month", Transaction.created_at) == b.month,
        extract("year", Transaction.created_at) == b.year
    ).scalar() or 0

    b.spent_amount = spent

    # 🔥 WARNING LOGIC
    if spent > b.limit_amount:
        b.warning = "⚠ Budget limit exceeded!"
    else:
        b.warning = "✅ Within budget"


        # 🔹 WARNING LOGIC
        warning = None

        if spent >= b.limit_amount:
            warning = "❌ Budget limit exceeded!"
        elif spent >= 0.8 * b.limit_amount:
            warning = "⚠ You are close to your budget limit"

        # 🔹 Attach warning dynamically
        response = BudgetResponse(
            id=b.id,
            month=b.month,
            year=b.year,
            category=b.category,
            limit_amount=b.limit_amount,
            spent_amount=spent,
            warning=warning
        )

        results.append(response)

    return results
