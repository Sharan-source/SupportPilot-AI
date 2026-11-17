import sqlite3

DB_NAME = "tickets.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # SQL definition
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name VARCHAR(100),
            email VARCHAR(150),
            title VARCHAR(255),
            description TEXT,
            category VARCHAR(50),
            severity VARCHAR(20),
            priority VARCHAR(10),
            confidence FLOAT,
            status VARCHAR(30) DEFAULT 'Open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_ticket(t: dict):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tickets (
            employee_name, email, title, description,
            category, severity, priority, confidence, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        t.get('employee_name', 'Employee'),
        t.get('email', ''),
        t.get('title', ''),
        t.get('description', ''),
        t.get('category', 'General'),
        t.get('severity', 'Low'),
        t.get('priority', 'P4'),
        float(t.get('confidence', 0.90)),
        t.get('status', 'Open')
    ))
    ticket_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return ticket_id

def get_all_tickets():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets ORDER BY created_at DESC")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows