# Modern Digital Banking Backend

## Backend Service for Digital Banking Dashboard

A FastAPI-based backend that provides secure authentication, account management, transaction processing, transaction categorization, and monthly budgeting features for a modern digital banking application.

---

## Project Overview

This backend is designed to support a digital banking dashboard where users can manage multiple bank accounts, track transactions, categorize spending, and monitor monthly budgets.  
The application follows a modular and scalable architecture suitable for real-world backend systems.

---

## Features

### Authentication & User Management
JWT-based authentication for secure login and registration.  
Ensures user-specific access to accounts, transactions, and budgets.

### Account Management
Allows users to create and manage multiple bank accounts.  
Each account is linked securely to a single user.

### Transaction Management
Supports credit and debit transactions.  
Provides CSV upload functionality for bulk transaction ingestion.

### Transaction Categorization
Automatically categorizes transactions using keyword-based rules.  
Supports manual category updates when auto-categorization is incorrect.

### Budgeting & Spend Tracking
Allows users to create monthly budgets by category.  
Calculates real-time spending and compares it against budget limits.

---

## Technology Stack

FastAPI is used as the backend framework.  
SQLAlchemy ORM is used for database interactions.  
JWT is used for authentication and authorization.  
PostgreSQL or SQLite can be used as the database.

---
## Project Structure
modern_digital_banking_backend/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── requirements.txt
├── services/
│ └── categorization.py
└── routers/
├── auth.py
├── accounts.py
├── transactions.py
└── budgets.py

## Project Structure

