import sqlite3
import os

db_path = "data/work_log.db"
os.makedirs("data", exist_ok=True)

def init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS employees (rfid TEXT PRIMARY KEY, name TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS logs (rfid TEXT, direction TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
    conn.commit()
    conn.close()

def add_employee(rfid, name):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO employees (rfid, name) VALUES (?, ?)", (rfid, name))
    conn.commit()
    conn.close()

def log_event(rfid, direction):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO logs (rfid, direction) VALUES (?, ?)", (rfid, direction))
    conn.commit()
    conn.close()

def get_last_direction(rfid):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT direction FROM logs WHERE rfid = ? ORDER BY timestamp DESC LIMIT 1", (rfid,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else "OUT"

def get_employee_name(rfid):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT name FROM employees WHERE rfid = ?", (rfid,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else "Неизвестен"

def get_logs():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        SELECT logs.timestamp, employees.name, logs.direction
        FROM logs LEFT JOIN employees ON logs.rfid = employees.rfid
        ORDER BY logs.timestamp DESC
    """)
    results = c.fetchall()
    conn.close()
    return results

init_db()
