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


class TransactionResponse(BaseModel):
    id: int
    account_id: int
    amount: float
    txn_type: str
    description: Optional[str] = None

    # ✅ ADDED FOR MILESTONE-2
    category: Optional[str] = "others"

    class Config:
        orm_mode = True


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

    class Config:
        orm_mode = True
