"""
Database Initialization Script.
Parses the local '.env' file and runs 'db/schema.sql' to bootstrap the MariaDB database and tables.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import pymysql

# Locate .env file in the root directory
ROOT_DIR = Path(__file__).resolve().parent
ENV_PATH = ROOT_DIR / ".env"

if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)
else:
    print("Error: .env file not found. Please copy .env.example to .env and fill in your MariaDB credentials.")
    sys.exit(1)

# Retrieve configuration parameters
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "ebay_inventory")

if not DB_USER or DB_PASSWORD is None:
    print("Error: DB_USER and DB_PASSWORD must be configured in your .env file.")
    sys.exit(1)

print(f"Connecting to MariaDB server at {DB_HOST}:{DB_PORT} and database '{DB_NAME}' as user '{DB_USER}'...")

try:
    # Establish connection with the configured database name
    connection = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4"
    )
except Exception as e:
    print(f"Failed to connect to MariaDB: {e}")
    sys.exit(1)

try:
    with connection.cursor() as cursor:
        # Read the schema SQL file
        schema_file_path = ROOT_DIR / "db" / "schema.sql"
        if not schema_file_path.exists():
            print(f"Error: Schema file not found at {schema_file_path}")
            sys.exit(1)
            
        with open(schema_file_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()

        # Split SQL file into individual statements
        # Note: This is a simple parser that splits by semicolon.
        # It works perfectly for standard table DDLs.
        statements = schema_sql.split(";")
        
        print("Executing schema DDLs...")
        for stmt in statements:
            cleaned_stmt = stmt.strip()
            if not cleaned_stmt:
                continue
                
            try:
                cursor.execute(cleaned_stmt)
            except Exception as ddl_err:
                print(f"Error executing statement:\n{cleaned_stmt}\nError: {ddl_err}")
                connection.rollback()
                sys.exit(1)
                
        connection.commit()
        print(f"Successfully initialized database '{DB_NAME}' and all tables!")
        
finally:
    connection.close()
