from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import csv, io

from database import get_db
from models import User, Account, Transaction
from schemas import TransactionCreate, TransactionResponse

# ✅ FIXED IMPORT (auth utils file)
from routers.auth_utils import get_current_user

# ✅ AUTO CATEGORIZATION SERVICE
from services.categorization import auto_categorize

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.get("/{account_id}", response_model=List[TransactionResponse])
def get_transactions(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    account = db.query(Account).filter(
        Account.id == account_id,
        Account.user_id == current_user.id
    ).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    return db.query(Transaction).filter(
        Transaction.account_id == account_id
    ).all()


@router.post("/", response_model=TransactionResponse)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    account = db.query(Account).filter(
        Account.id == transaction.account_id,
        Account.user_id == current_user.id
    ).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # ✅ AUTO CATEGORY
    category = auto_categorize(transaction.description)

    new_txn = Transaction(
        account_id=transaction.account_id,
        amount=transaction.amount,
        txn_type=transaction.txn_type,
        description=transaction.description,
        category=category
    )

    db.add(new_txn)
    db.commit()
    db.refresh(new_txn)

    return new_txn


@router.post("/upload-csv")
def upload_transactions_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")

    content = file.file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))

    created = 0

    for row in reader:
        if "account_id" not in row:
            continue

        account_id = int(row["account_id"])

        account = db.query(Account).filter(
            Account.id == account_id,
            Account.user_id == current_user.id
        ).first()

        if not account:
            continue

        description = row.get("description", "")

        # ✅ AUTO CATEGORY
        category = auto_categorize(description)

        txn = Transaction(
            account_id=account_id,
            amount=float(row["amount"]),
            txn_type=row["txn_type"],
            description=description,
            category=category
        )

        db.add(txn)
        created += 1

    db.commit()
    return {"message": f"{created} transactions uploaded successfully"}


# =====================================================
# ✅ MANUAL RE-CATEGORIZATION (MILESTONE-2 FEATURE)
# =====================================================
@router.put("/{transaction_id}/category")
def update_transaction_category(
    transaction_id: int,
    new_category: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    txn = db.query(Transaction).join(Account).filter(
        Transaction.id == transaction_id,
        Account.user_id == current_user.id
    ).first()

    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")

    txn.category = new_category
    db.commit()

    return {"message": "Transaction category updated successfully"}
