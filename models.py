from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship
from database import Base

# =========================
# USER MODEL
# =========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String(15), unique=True, nullable=False)

    accounts = relationship("Account", back_populates="user")
    budgets = relationship("Budget", back_populates="user", cascade="all,delete")
    bills = relationship("Bill", back_populates="user", cascade="all,delete")


# =========================
# ACCOUNT MODEL
# =========================
class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    bank_name = Column(String, nullable=False)
    account_type = Column(String, nullable=False)
    balance = Column(Float, default=0)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="accounts")
    transactions = relationship(
        "Transaction",
        back_populates="account",
        cascade="all,delete"
    )


# =========================
# TRANSACTION MODEL
# =========================
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    txn_type = Column(String, nullable=False)  # credit / debit
    account_id = Column(
        Integer,
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False
    )
    description = Column(String, nullable=True)
    category = Column(String, default="others")

    # REQUIRED FOR BUDGET CALCULATION
    created_at = Column(DateTime, default=datetime.utcnow)

    account = relationship("Account", back_populates="transactions")


# =========================
# BUDGET MODEL (MILESTONE-2)
# =========================
class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)

    category = Column(String, nullable=False)
    limit_amount = Column(Float, nullable=False)
    spent_amount = Column(Float, default=0)

    user = relationship("User", back_populates="budgets")


# =========================
# BILL MODEL (MILESTONE-3)
# =========================
class Bill(Base):
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    bill_name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    due_date = Column(DateTime, nullable=False)

    is_paid = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bills")
