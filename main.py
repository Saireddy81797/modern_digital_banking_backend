from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from routers import users, accounts, transactions
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Modern Digital Banking Dashboard")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router,prefix="/users")
app.include_router(accounts.router,prefix="/accounts")
app.include_router(transactions.router)

@app.get("/")
def root():
    return {"message": "Backend running"}