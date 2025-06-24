# test_db.py
from app.db.db import list_tables

if __name__ == "__main__":
    print("Tablas disponibles", list_tables())
