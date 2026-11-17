from flask import Flask, render_template, request, jsonify
from classifier import process_ticket
from database import init_db, save_ticket, get_all_tickets

app = Flask(__name__)
init_db()

@app.route('/')
def home():
    tickets = get_all_tickets()
    return render_template('index.html', tickets=tickets)


@app.route('/ticket', methods=['POST'])
@app.route('/api/tickets', methods=['POST'])
def create_ticket():
    data = request.get_json(silent=True) or request.form.to_dict()
    description = data.get("description", "")
    
    if not description:
        return jsonify({"error": "Description is required"}), 400

    title = data.get("title", description[:30])
    employee_name = data.get("employee_name") or data.get("employee", "Arun")
    email = data.get("email", "arun@company.com")

    # Run the classifier
    category, severity, priority, confidence = process_ticket(f"{title} {description}")

    ticket_record = {
        "employee_name": employee_name,
        "email": email,
        "title": title,
        "description": description,
        "category": category,
        "severity": severity,
        "priority": priority,
        "confidence": confidence,
        "status": "Open"
    }

    ticket_id = save_ticket(ticket_record)
    ticket_record["ticket_id"] = ticket_id

    # Response format 
    return jsonify({
        "ticket": description,
        "ticket_id": ticket_id,
        "category": category,
        "severity": severity,
        "priority": priority,
        "confidence": f"{round(confidence * 100, 1)}%",
        "status": "Open"
    }), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)