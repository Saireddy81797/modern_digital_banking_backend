## Modern Digital Banking Backend

A FastAPI-based backend system for a modern digital banking dashboard.
This backend handles authentication, accounts, transactions, categorization, and budgeting, built using a milestone-driven architecture.

## Project Overview

This project serves as the backend for a digital banking application that allows users to manage multiple accounts, track transactions, categorize spending, and monitor monthly budgets with real-time progress calculations.

The backend is designed to be modular, scalable, and frontend-agnostic, enabling integration with React or Streamlit dashboards.

## Key Features
## Authentication & User Management

JWT-based authentication

Secure user registration and login

User-specific data access control

## Account Management

Create and manage multiple bank accounts

Accounts linked securely to users


## Transaction Management

Create credit and debit transactions

Upload transactions in bulk using CSV files

Fetch transactions per account

## Transaction Categorization (Milestone-2)

Automatic categorization using keyword-based rules

Categories include:

Food

Travel

Shopping

Utilities

Others

Manual re-categorization API for corrections

## Budgeting & Spend Tracking (Milestone-2)

Create monthly budgets per category

View all budgets for a user

Calculate real-time budget progress

Spent amount derived dynamically from transactions
