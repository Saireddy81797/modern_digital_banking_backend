from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
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

    # ✅ ADDED FOR MILESTONE-2
    category = Column(String, default="others")

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
