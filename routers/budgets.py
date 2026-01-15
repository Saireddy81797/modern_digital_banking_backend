from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Budget, Transaction
from schemas import BudgetCreate
from deps import get_current_user
from sqlalchemy import func, extract

router = APIRouter(prefix="/budgets", tags=["Budgets"])
