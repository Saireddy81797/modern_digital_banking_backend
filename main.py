from fastapi import FastAPI

# Import routers
from routers import accounts
from routers import transactions
from routers import budgets
from routers import auth
from routers import bills

# if you have auth router

app = FastAPI(title="Modern Digital Banking Backend")

# =========================
# REGISTER ROUTERS
# =========================
app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(transactions.router)
app.include_router(budgets.router)
app.include_router(bills.router)


# =========================
# ROOT ENDPOINT
# =========================
@app.get("/")
def root():
    return {"message": "Modern Digital Banking Backend is running"}
