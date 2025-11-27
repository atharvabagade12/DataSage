import sqlite3

conn = sqlite3.connect('auth.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables in auth.db:", [t[0] for t in tables])

if tables:
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table[0]})")
        columns = cursor.fetchall()
        print(f"\nTable: {table[0]}")
        print("Columns:", [c[1] for c in columns])
        
        cursor.execute(f"SELECT * FROM {table[0]} LIMIT 1")
        sample = cursor.fetchone()
        if sample:
            print("Sample row:", sample)

conn.close()
