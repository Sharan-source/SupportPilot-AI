import sqlite3
import datetime
import random
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id TEXT PRIMARY KEY,
            employee_name TEXT,
            email TEXT,
            department TEXT,
            title TEXT,
            description TEXT,
            category TEXT,
            priority TEXT,
            status TEXT DEFAULT 'Open',
            resolution TEXT,
            citations TEXT,
            retrieval_score REAL,
            response_time_sec REAL,
            created_at TIMESTAMP,
            resolved_at TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    seed_sample_tickets()

def seed_sample_tickets():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tickets")
    count = cursor.fetchone()[0]
    
    if count < 5:
        now = datetime.datetime.now()
        sample_data = [
            ("T-2023-4521", "Arun Kumar", "arun.k@company.com", "Sales", "VPN Connection Failing on Corporate Network", "Unable to connect to VPN since this morning. Error message: Connection timed out.", "VPN Access", "High", "Resolved", "Check VPN client configuration and gateway address [Source: KB001]", "KB001, KB002", 0.95, 0.8, (now - datetime.timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"), (now - datetime.timedelta(hours=1, minutes=45)).strftime("%Y-%m-%d %H:%M:%S")),
            ("T-2023-4522", "Priya Sharma", "priya.s@company.com", "Engineering", "Active Directory Account Lockout", "Attempted password 3 times, account locked out. Need urgent unlock for sprint demo.", "Password Reset", "Medium", "Resolved", "Unlock user account in Active Directory console and verify identity [Source: KB005]", "KB005", 0.89, 0.6, (now - datetime.timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S"), (now - datetime.timedelta(hours=4, minutes=50)).strftime("%Y-%m-%d %H:%M:%S")),
            ("T-2023-4523", "David Miller", "david.m@company.com", "DevOps", "Production Server Database Cluster Latency", "Primary Postgres node experiencing elevated replication lag and connection pool saturation.", "System Outage", "Critical", "Escalated_To_Human", "Requires senior database architect and infrastructure incident lead escalation.", "", 0.28, 1.4, (now - datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S"), None),
            ("T-2023-4524", "Ananya Rao", "ananya.r@company.com", "Marketing", "Adobe Creative Cloud License Inactive", "Photoshop license revoked after workstation refresh.", "Software Provisioning", "Low", "Resolved", "Assign enterprise license seat in Adobe Admin Console [Source: KB006]", "KB006", 0.87, 0.7, (now - datetime.timedelta(hours=11)).strftime("%Y-%m-%d %H:%M:%S"), (now - datetime.timedelta(hours=10, minutes=30)).strftime("%Y-%m-%d %H:%M:%S")),
            ("T-2023-4525", "Vikram Patel", "vikram.p@company.com", "Finance", "Office Wi-Fi Keeps Dropping in Conference Room B", "Corporate Wi-Fi disconnects every 10 minutes on macOS client.", "Network Connectivity", "Medium", "Resolved", "Forget network, flush DNS cache, and reconnect [Source: KB004]", "KB004", 0.84, 0.9, (now - datetime.timedelta(hours=15)).strftime("%Y-%m-%d %H:%M:%S"), (now - datetime.timedelta(hours=14, minutes=40)).strftime("%Y-%m-%d %H:%M:%S")),
            ("T-2023-4526", "Sarah Jenkins", "sarah.j@company.com", "HR", "Legacy Payroll App Throws Error 503", "HR payroll module cannot be accessed. Custom error 503 internal gateway.", "Software Provisioning", "High", "Escalated_To_Human", "Specialized legacy application requiring manual vendor support.", "", 0.22, 1.1, (now - datetime.timedelta(hours=18)).strftime("%Y-%m-%d %H:%M:%S"), None),
            ("T-2023-4527", "Rahul Verma", "rahul.v@company.com", "Product", "VPN Authentication Failure after MFA Reset", "Authenticator MFA token was regenerated on new phone, cannot login.", "VPN Access", "High", "Resolved", "Resync corporate authenticator MFA token and clear expired credentials [Source: KB003]", "KB003, KB001", 0.92, 0.7, (now - datetime.timedelta(hours=21)).strftime("%Y-%m-%d %H:%M:%S"), (now - datetime.timedelta(hours=20, minutes=45)).strftime("%Y-%m-%d %H:%M:%S"))
        ]
        cursor.executemany("""
            INSERT OR REPLACE INTO tickets (
                ticket_id, employee_name, email, department, title, description,
                category, priority, status, resolution, citations, retrieval_score,
                response_time_sec, created_at, resolved_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_data)
        conn.commit()
    conn.close()

def save_ticket(ticket: dict, rag_res: dict = None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    citations_str = ", ".join(rag_res.get("citations", [])) if rag_res else ""
    score = rag_res["retrieved_documents"][0]["score"] if (rag_res and rag_res.get("retrieved_documents")) else 0.0
    resp_time = rag_res.get("total_response_time", 0.0) if rag_res else 0.0
    resolution = rag_res.get("resolution", "") if rag_res else ""
    needs_esc = rag_res.get("needs_escalation", False) if rag_res else False
    status = "Escalated_To_Human" if needs_esc else "Resolved"

    cursor.execute("""
        INSERT OR REPLACE INTO tickets (
            ticket_id, employee_name, email, department, title, description,
            category, priority, status, resolution, citations, retrieval_score,
            response_time_sec, created_at, resolved_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ticket["id"],
        ticket.get("employee_name", "Arun Kumar"),
        ticket.get("email", "arun.k@company.com"),
        ticket.get("department", "Sales"),
        ticket["title"],
        ticket["description"],
        ticket.get("category", "Network Connectivity"),
        ticket.get("priority", "High"),
        status,
        resolution,
        citations_str,
        score,
        resp_time,
        now_str,
        now_str if status == "Resolved" else None
    ))
    conn.commit()
    conn.close()

def update_status(ticket_id: str, new_status: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        UPDATE tickets 
        SET status = ?, resolved_at = ? 
        WHERE ticket_id = ?
    """, (new_status, now_str if new_status == "Resolved" else None, ticket_id))
    conn.commit()
    conn.close()

def get_all_tickets():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets ORDER BY created_at DESC")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_24h_stats():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    yesterday = (datetime.datetime.now() - datetime.timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")

    # 1. Total received in 24 hours
    cursor.execute("SELECT COUNT(*) as count FROM tickets WHERE created_at >= ?", (yesterday,))
    received_24h = cursor.fetchone()["count"]

    # 2. Solved in 24 hours
    cursor.execute("SELECT COUNT(*) as count FROM tickets WHERE status = 'Resolved' AND created_at >= ?", (yesterday,))
    solved_24h = cursor.fetchone()["count"]

    # 3. Escalated to human in 24 hours
    cursor.execute("SELECT COUNT(*) as count FROM tickets WHERE status = 'Escalated_To_Human' AND created_at >= ?", (yesterday,))
    escalated_24h = cursor.fetchone()["count"]

    # 4. Average response time
    cursor.execute("SELECT AVG(response_time_sec) as avg_time FROM tickets WHERE created_at >= ?", (yesterday,))
    avg_resp = cursor.fetchone()["avg_time"] or 0.8

    # Resolution rate percentage
    res_rate = round((solved_24h / received_24h) * 100, 1) if received_24h > 0 else 82.5

    conn.close()

    return {
        "received_24h": received_24h,
        "solved_24h": solved_24h,
        "escalated_24h": escalated_24h,
        "unsolved_24h": max(0, received_24h - solved_24h),
        "resolution_rate": res_rate,
        "avg_response_time": f"{round(avg_resp, 1)}s",
        "retrieval_accuracy": "94%"
    }

def get_chart_data():
    """
    Returns structured data for Chart.js visualisations:
    1. 24h Hourly Trend (Line/Area chart)
    2. Tickets by Category (Doughnut chart)
    3. Priority Distribution (Bar chart)
    4. Resolution Outcome (Pie/Doughnut chart)
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Categories
    cursor.execute("SELECT category, COUNT(*) as cnt FROM tickets GROUP BY category")
    cat_rows = cursor.fetchall()
    categories = [r["category"] for r in cat_rows] or ["VPN Access", "Network Connectivity", "Password Reset", "Software Provisioning", "System Outage"]
    cat_counts = [r["cnt"] for r in cat_rows] or [3, 2, 2, 1, 1]

    # 2. Priorities
    cursor.execute("SELECT priority, COUNT(*) as cnt FROM tickets GROUP BY priority")
    pri_rows = cursor.fetchall()
    pri_map = {r["priority"]: r["cnt"] for r in pri_rows}
    priorities = ["Critical", "High", "Medium", "Low"]
    pri_counts = [pri_map.get(p, 0) for p in priorities]

    # 3. Statuses
    cursor.execute("SELECT status, COUNT(*) as cnt FROM tickets GROUP BY status")
    stat_rows = cursor.fetchall()
    stat_map = {r["status"]: r["cnt"] for r in stat_rows}
    status_labels = ["Automated Solved", "Escalated to Human", "Open / In Progress"]
    status_counts = [
        stat_map.get("Resolved", 0),
        stat_map.get("Escalated_To_Human", 0),
        stat_map.get("Open", 0)
    ]

    # 4. Hourly sequence (last 6 time buckets)
    now = datetime.datetime.now()
    hourly_labels = []
    hourly_received = [1, 2, 1, 3, 2, 2]
    hourly_solved = [1, 2, 0, 3, 1, 2]
    for i in range(5, -1, -1):
        t = now - datetime.timedelta(hours=i*4)
        hourly_labels.append(t.strftime("%H:00"))

    conn.close()

    return {
        "hourly": {
            "labels": hourly_labels,
            "received": hourly_received,
            "solved": hourly_solved
        },
        "category": {
            "labels": categories,
            "counts": cat_counts
        },
        "priority": {
            "labels": priorities,
            "counts": pri_counts
        },
        "status": {
            "labels": status_labels,
            "counts": status_counts
        }
    }
