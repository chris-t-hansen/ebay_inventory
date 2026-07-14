# GEMINI Instructions (`GEMINI.md`)

This document serves as the primary context, architectural blueprint, and development mandate for all AI agent interactions and human developers working on the `ebay_inventory` project. 

---

## 1. Project Overview

`ebay_inventory` is a Python-based utility integrated with a MariaDB database backend, designed to manage all aspects of eBay seller listings, physical inventory, sales, auction bids, fulfillment, and feedback loops. It functions as both a functional utility and a learning platform for working with the Gemini CLI tool.

### Core Objectives
*   **Inventory Synchronization:** Fetch and sync current listings and physical items from the eBay seller account.
*   **Listing Scheduling:** Store and schedule drafts of listings in advance to be published automatically at specified dates and times.
*   **Shipping & Package Configuration:** Set explicit carrier options, shipping services, and shipping weight (lbs) per listing.
*   **Media & Pictures Tracking:** Maintain and track local or eBay-hosted image assets associated with unique inventory SKUs.
*   **Auction Bids & Active Bid Tracking:** Monitor live bids, bidders, and current active amounts for auction-style listings.
*   **Fulfillment & Shipments:** Track orders needing to be shipped, register carrier names, associate tracking numbers, and manage shipment status.
*   **Feedback Automation:** Track whether feedback has been successfully left for the buyer or received from the buyer.
*   **Performance Metrics:** Calculate net margins and ROI on individual items and overall sales.
*   **Database Reliability:** Utilize MariaDB to store listings, orders, bids, and transactions with robust, portable schemas and relational consistency.

### Primary Stack
*   **Language:** Python 3.10+ (using strict type annotations and standard PEP 8 conventions).
*   **Database:** MariaDB (relational schema managed via SQLAlchemy with PyMySQL backend).
*   **API Integration:** eBay REST APIs (OAuth 2.0, Inventory API, Fulfillment API) and legacy Trading API.
*   **Testing:** `pytest` (using standard fixtures and mock integrations).

---

## 2. Directory & Architecture Blueprint

The project follows a clean, modular structure separating models, client integration services, and database management:

```text
ebay_inventory/
├── .gitignore              # Git ignore rules
├── LICENSE                 # Project license
├── README.md               # User-facing README
├── GEMINI.md               # This instructions file (Do not modify without explicit instruction)
├── init_db.py              # Automated script to bootstrap database schema from .env
├── requirements.txt        # Python package dependencies
├── .env.example            # Template for environment variables
├── src/                    # Application source code
│   ├── __init__.py
│   ├── main.py             # Entrypoint
│   ├── config.py           # Configuration and environment variables parsing
│   ├── database.py         # MariaDB connection and session pool management
│   ├── models/             # SQLAlchemy Database Models mapping tables
│   │   ├── __init__.py     # Models initializer
│   │   ├── base.py         # Declarative Base
│   │   ├── item.py         # InventoryItem & ItemPicture tables
│   │   ├── order.py        # Order table (shipping tracking, feedback)
│   │   └── bid.py          # AuctionBid table
│   ├── ebay/               # eBay API client/wrappers
│   └── services/           # Business logic (inventory sync, sales calculation)
├── db/                     # Database schemas and migrations
│   └── schema.sql          # Portable MariaDB Core DDL schema definition
└── tests/                  # Automated test suite
    ├── __init__.py
    ├── conftest.py         # pytest configurations and in-memory SQLite fixtures
    └── test_database.py    # Database model mapping and constraint tests
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
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

### 3.2. Environment Configuration
Create a `.env` file in the root directory using `.env.example` as a template:
```env
# Database Configuration
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=your_mariadb_user
DB_PASSWORD=your_secure_password
DB_NAME=your_target_database

# eBay Developer API Credentials
EBAY_APP_ID=your_client_id
EBAY_DEV_ID=your_dev_id
EBAY_CERT_ID=your_client_secret
EBAY_REDIRECT_URI=your_redirect_uri_name
EBAY_ENVIRONMENT=sandbox  # sandbox or production
```
*Note: Never commit `.env` or commit secrets to version control. Ensure `.gitignore` remains configured to ignore `.env` files.*

### 3.3. Database Setup (MariaDB)
Initialize your MariaDB schema using the automated setup script. The schema script `db/schema.sql` is portable, allowing you to build inside any existing database environment defined in your `.env`:
```bash
# Activate virtual environment and execute initialization
source .venv/bin/activate
python init_db.py
```

### 3.4. Running the Application
```bash
# Run the main entry point
python -m src.main
```

### 3.5. Running Tests
Tests use a simulated SQLite in-memory engine to prevent messing with your active MariaDB database and execute lightning-fast:
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
*   **Naming Conventions:** Tables and columns must use lowercase `snake_case`. Table names should be pluralized (e.g., `inventory_items`, `orders`).
*   **Data Integrity:** Use explicit foreign keys, non-null constraints where appropriate, and correct column types (e.g., `DECIMAL(10, 2)` for prices and monetary amounts, never floats).
*   **Primary Keys & Indexes:** Every table must have a primary key. Index heavily searched fields like eBay's unique Item ID (`ebay_listing_id`) or internal SKUs.

### 4.3. API Integration & Mocking
*   **API Client Decoupling:** Encapsulate all raw eBay API HTTP calls within an `EbayClient` class inside `src/ebay/`. Do not bleed API handling code into service or database layers.
*   **Testing Coverage:** Always mock HTTP responses when testing API clients. Never hit live eBay endpoints during automated unit tests. Use `pytest-mock` or `unittest.mock`.

### 4.4. Development Workflow & Git
*   **Surgical Edits:** When using Gemini CLI, utilize targeted edits using the `replace` tool to keep changes precise and minimize token usage.
*   **Incremental Progress:** Run linters and relevant test cases after every file edit. Do not accumulate large, unverified code changes.
*   **Git Auto-Commit:** Always stage, commit, and push newly created or modified files to git once they are fully implemented and verified via automated tests.

---

## 5. Agent Instructions for Tasks

When tasked with generating, modifying, or testing code in this workspace, you must:
1.  **Read and respect this file (`GEMINI.md`) first.**
2.  Maintain rigorous separation of concerns (DB, Business Logic, API, CLI/UI).
3.  Ensure database operations are safe, transactional, and follow strict type conventions.
4.  Write comprehensive tests (`pytest`) covering success paths, edge cases, and error handlings.
