from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# =========================
# AUTH SCHEMAS
# =========================
class RegisterUser(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str = Field(..., min_length=10, max_length=15)


class LoginUser(BaseModel):
    email: str
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# =========================
# ACCOUNT SCHEMAS
# =========================
class AccountCreate(BaseModel):
    bank_name: str
    account_type: str
    balance: float = 0


# =========================
# TRANSACTION SCHEMAS
# =========================
class TransactionCreate(BaseModel):
    account_id: int
    amount: float
    txn_type: str
    description: Optional[str] = None


class TransactionResponse(BaseModel):
    id: int
    account_id: int
    amount: float
    txn_type: str
    description: Optional[str] = None
    category: Optional[str] = "others"
    created_at: datetime

    class Config:
        from_attributes = True   # Pydantic v2 fix


# =========================
# BUDGET SCHEMAS (MILESTONE-2)
# =========================
class BudgetCreate(BaseModel):
    month: int
    year: int
    category: str
    limit_amount: float


class BudgetResponse(BudgetCreate):
    id: int
    spent_amount: float
    warning: Optional[str] = None   # 🔥 Budget warning

    class Config:
        from_attributes = True


# =========================
# BILL SCHEMAS (MILESTONE-3)
# =========================
class BillCreate(BaseModel):
    bill_name: str
    amount: float
    due_date: datetime


class BillUpdate(BaseModel):
    bill_name: Optional[str] = None
    amount: Optional[float] = None
    due_date: Optional[datetime] = None
    is_paid: Optional[bool] = None


class BillResponse(BaseModel):
    id: int
    bill_name: str
    amount: float
    due_date: datetime
    is_paid: bool
    overdue: bool   # 🔥 due date logic output
    created_at: datetime

    class Config:
        from_attributes = True
