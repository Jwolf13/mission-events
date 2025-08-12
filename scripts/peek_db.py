# scripts/peek_db.py
import sqlite3
from pathlib import Path

db_path = Path("mission.db")
if not db_path.exists():
    print("mission.db not found in current folder. cd to your project root and try again.")
    raise SystemExit(1)

con = sqlite3.connect(str(db_path))
cur = con.cursor()

# Show tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
tables = [r[0] for r in cur.fetchall()]
print("Tables:", tables)

# If events table exists, show some rows
if "events" in tables:
    print("\nLast 5 events (id, title, details):")
    for row in cur.execute("SELECT id, title, details FROM events ORDER BY id DESC LIMIT 5;"):
        print(row)
else:
    print("\nNo 'events' table yet. Create an event via Swagger (POST /events).")

con.close()
