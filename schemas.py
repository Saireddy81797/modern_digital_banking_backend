from pydantic import BaseModel, EmailStr, Field
from typing import Optional

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


from datetime import datetime

class TransactionResponse(BaseModel):
    id: int
    account_id: int
    amount: float
    txn_type: str
    description: Optional[str] = None
    category: Optional[str] = "others"
    created_at: datetime

    class Config:
        from_attributes = True   # 🔹 Pydantic v2 fix



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

    # 🔹 NEW FIELD (for warning when limit exceeded)
    warning: Optional[str] = None

    class Config:
        from_attributes = True   # 🔹 Pydantic v2 fix

