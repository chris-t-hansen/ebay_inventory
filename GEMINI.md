# GEMINI Instructions (`GEMINI.md`)

This document serves as the primary context, architectural blueprint, and development mandate for all AI agent interactions and human developers working on the `ebay_inventory` project. 

---

## 1. Project Overview

`ebay_inventory` is a Python-based utility integrated with a MariaDB database, designed to track eBay listings, inventory, sales, and transaction details. It functions as both a functional utility and a learning platform for working with the Gemini CLI tool.

### Core Objectives
*   **Inventory Synchronization:** Fetch and sync current listings from the eBay seller account.
*   **Sales & Order Tracking:** Record sales, transaction fees, shipping costs, and buyer information.
*   **Performance Metrics:** Calculate net margins and ROI on individual items and overall sales.
*   **Database Reliability:** Utilize MariaDB to store listings and transactions with robust schemas and relations.

### Primary Stack
*   **Language:** Python 3.10+ (using strict type annotations and standard PEP 8 conventions).
*   **Database:** MariaDB (relational schema, optimized for transactional consistency).
*   **API Integration:** eBay REST APIs (OAuth 2.0, Inventory API, Fulfillment API).
*   **Testing:** `pytest` (using standard fixtures and mock integrations).

---

## 2. Directory & Architecture Blueprint

Since the project is in its early bootstrapping phase, the following structure is established as the architectural standard:

```text
ebay_inventory/
├── .gitignore              # Git ignore rules
├── LICENSE                 # Project license
├── README.md               # User-facing README
├── GEMINI.md               # This instructions file (Do not modify without explicit instruction)
├── requirements.txt        # Python package dependencies
├── .env.example            # Template for environment variables
├── src/                    # Application source code
│   ├── __init__.py
│   ├── main.py             # Entrypoint
│   ├── config.py           # Configuration and environment variables parsing
│   ├── database.py         # MariaDB connection and session management
│   ├── models/             # Database tables (SQLAlchemy or SQL schema models)
│   ├── ebay/               # eBay API client/wrappers
│   └── services/           # Business logic (inventory sync, sales calculation)
├── db/                     # Database schemas and migrations
│   ├── schema.sql          # Core DDL schema definition
│   └── migrations/         # Optional database migration scripts
└── tests/                  # Automated test suite
    ├── __init__.py
    ├── conftest.py         # pytest configurations and fixtures
    ├── test_database.py    # Database connection/operation tests
    └── test_ebay_client.py # Mocks and unit tests for eBay API integration
```

---

## 3. Building and Running

### 3.1. Environment Setup (Local Development)
To initialize the project environment, execute the following commands:

1.  **Create and Activate a Virtual Environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
2.  **Install Dependencies:**
    *(TODO: Define packages in `requirements.txt` once dependencies are selected.)*
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

### 3.2. Environment Configuration
Create a `.env` file in the root directory using `.env.example` as a template:
```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=ebay_user
DB_PASSWORD=your_secure_password
DB_NAME=ebay_inventory

# eBay API Credentials
EBAY_CLIENT_ID=your_ebay_client_id
EBAY_CLIENT_SECRET=your_ebay_client_secret
EBAY_REDIRECT_URI=your_redirect_uri
EBAY_ENVIRONMENT=sandbox  # sandbox or production
```
*Note: Never commit `.env` or commit secrets to version control. Ensure `.gitignore` remains configured to ignore `.env` files.*

### 3.3. Database Setup (MariaDB)
Initialize the database and schema:
```bash
# TODO: Document exact database creation and initialization commands.
# Example: mysql -u root -p < db/schema.sql
```

### 3.4. Running the Application
```bash
# Run the main entry point
python -m src.main
```

### 3.5. Running Tests
```bash
# Execute unit and integration tests
pytest
```

---

## 4. Development Conventions & Guidelines

All agents and developers must strictly follow these conventions when contributing:

### 4.1. Code Quality & Formatting
*   **PEP 8 Compliance:** All Python code must conform to PEP 8 standards. Use `black` and `ruff`/`flake8` for formatting and linting.
*   **Type Hinting:** Mandatory type annotations for all function/method signatures and complex variables.
*   **Documentation:** All modules, classes, and public methods must include Google-style docstrings describing parameters, return values, and exceptions.

### 4.2. Database Design Best Practices
*   **Naming Conventions:** Tables and columns must use lowercase `snake_case`. Table names should be pluralized (e.g., `listings`, `orders`).
*   **Data Integrity:** Use explicit foreign keys, non-null constraints where appropriate, and correct column types (e.g., `DECIMAL(10, 2)` for prices and monetary amounts, never floats).
*   **Primary Keys & Indexes:** Every table must have a primary key. Index heavily searched fields like eBay's unique Item ID (`ebay_item_id`) or internal SKUs.

### 4.3. API Integration & Mocking
*   **API Client Decoupling:** Encapsulate all raw eBay API HTTP calls within an `EbayClient` class inside `src/ebay/`. Do not bleed API handling code into service or database layers.
*   **Testing Coverage:** Always mock HTTP responses when testing API clients. Never hit live eBay endpoints during automated unit tests. Use `pytest-mock` or `unittest.mock`.

### 4.4. Development Workflow & Git
*   **Surgical Edits:** When using Gemini CLI, utilize targeted edits using the `replace` tool to keep changes precise and minimize token usage.
*   **Incremental Progress:** Run linters and relevant test cases after every file edit. Do not accumulate large, unverified code changes.
*   **No Staging/Commits:** Do not stage or commit files unless explicitly requested by the user.

---

## 5. Agent Instructions for Tasks

When tasked with generating, modifying, or testing code in this workspace, you must:
1.  **Read and respect this file (`GEMINI.md`) first.**
2.  Maintain rigorous separation of concerns (DB, Business Logic, API, CLI/UI).
3.  Ensure database operations are safe, transactional, and follow strict type conventions.
4.  Write comprehensive tests (`pytest`) covering success paths, edge cases, and error handlings.
