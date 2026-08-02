import sqlite3

conn = sqlite3.connect("storage/tenorio3g.db")

cursor = conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
)

print("\n===== TABLAS =====")

for table in cursor.fetchall():
    print(table[0])

conn.close()