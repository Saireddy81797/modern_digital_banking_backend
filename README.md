🏦 Modern Digital Banking Backend

A scalable FastAPI-based backend for a modern digital banking dashboard that supports user authentication, account management, transaction processing, budgeting, and financial insights.

This project follows a modular backend architecture and is built as part of an 8-week milestone-driven implementation.

🚀 Features Implemented
🔐 Authentication & User Management

JWT-based authentication

Secure user registration and login

User-scoped data access

🏦 Accounts

Create and manage multiple bank accounts

Account-to-user relationship enforcement

💳 Transactions

Create transactions (credit/debit)

Bulk transaction upload via CSV

Transaction listing per account

🏷️ Transaction Categorization (Milestone-2)

Automatic categorization based on transaction description keywords

Categories such as food, travel, shopping, utilities, others

Manual re-categorization API for correcting categories

📊 Budgets & Spend Tracking (Milestone-2)

Create monthly budgets by category

List user-specific budgets

Real-time budget progress calculation

Computes spent amount from transactions

Supports month & year based tracking

🧱 Tech Stack

Backend Framework: FastAPI

Database: PostgreSQL / SQLite (via SQLAlchemy ORM)

Authentication: JWT

ORM: SQLAlchemy

API Docs: Swagger (FastAPI /docs)

Language: Python 3.10+
