import sqlite3
from pathlib import Path

db = Path(__file__).resolve().parent / "data" / "database.sqlite"

print("Banco verificado:", db)
print("Arquivo existe:", db.exists())

conn = sqlite3.connect(db)

tabelas = conn.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
""").fetchall()

print("Tabelas encontradas:", tabelas)

conn.close()
