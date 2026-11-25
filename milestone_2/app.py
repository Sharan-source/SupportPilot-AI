from flask import Flask, render_template, request, jsonify
from database import init_db, save_ticket, get_all_tickets, get_24h_stats, update_status, get_chart_data
from rag.pipeline import RAGPipeline
import json
import os
import random
from config import KB_FILE_PATH

app = Flask(__name__)
init_db()
rag_pipeline = RAGPipeline()

@app.route('/')
def home():
    tickets = get_all_tickets()
    stats = get_24h_stats()
    latest = tickets[0] if tickets else None
    return render_template('index.html', tickets=tickets, stats=stats, latest=latest)

@app.route('/api/tickets/rag', methods=['POST'])
def process_rag_ticket():
    data = request.get_json(silent=True) or request.form.to_dict()
    ticket_id = data.get("id") or f"T-2023-{random.randint(4600, 9999)}"
    
    ticket = {
        "id": ticket_id,
        "title": data.get("title", "VPN Connection Issue"),
        "description": data.get("description", ""),
        "category": data.get("category", "VPN Access"),
        "priority": data.get("priority", "High"),
        "employee_name": data.get("employee_name", "Arun Kumar"),
        "email": data.get("email", "arun.k@company.com"),
        "department": data.get("department", "Engineering")
    }

    # Run RAG Pipeline (4-step workflow)
    result = rag_pipeline.run(ticket)

    # Save to SQLite database
    save_ticket(ticket, result)

    return jsonify({
        "status": "success",
        "ticket": ticket,
        "rag_result": result,
        "stats": get_24h_stats(),
        "chart_data": get_chart_data()
    }), 201

# Action 1: Mark as Solved by User
@app.route('/api/tickets/<ticket_id>/resolve', methods=['POST'])
def resolve_ticket(ticket_id):
    update_status(ticket_id, "Resolved")
    return jsonify({
        "message": f"Ticket {ticket_id} marked as Solved!",
        "stats": get_24h_stats(),
        "chart_data": get_chart_data()
    })

# Action 2: Approaching Human Agent (Escalation)
@app.route('/api/tickets/<ticket_id>/escalate', methods=['POST'])
def escalate_ticket(ticket_id):
    update_status(ticket_id, "Escalated_To_Human")
    return jsonify({
        "message": f"Ticket {ticket_id} escalated to Human Support Team.",
        "next_step": "A senior support engineer has been assigned and will reach out to the employee shortly.",
        "stats": get_24h_stats(),
        "chart_data": get_chart_data()
    })

# Route for Chart.js Visualisations
@app.route('/api/dashboard/charts', methods=['GET'])
def dashboard_charts():
    return jsonify(get_chart_data())

# Route for Knowledge Base Explorer
@app.route('/api/knowledge-base', methods=['GET'])
def get_knowledge_base():
    if os.path.exists(KB_FILE_PATH):
        with open(KB_FILE_PATH, "r", encoding="utf-8") as f:
            kb = json.load(f)
            return jsonify(kb)
    return jsonify([])

if __name__ == '__main__':
    print("=" * 65)
    print("SupportPilot AI - Milestone 2 Server Running on http://127.0.0.1:5001")
    print("=" * 65)
    app.run(debug=True, port=5001)
