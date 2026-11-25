import re

def analyze_ticket(ticket: dict) -> dict:
    """
    Step 1: Ticket Analysis & Query Generation.
    Extracts core terms and builds a refined search query.
    """
    raw_text = f"{ticket.get('title', '')} {ticket.get('description', '')}".lower()
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', ' ', raw_text)
    
    possible_keywords = [
        "vpn", "network", "firewall", "authentication", "timeout", 
        "connection", "dns", "password", "server", "database", 
        "hardware", "software", "license", "reboot", "mfa"
    ]
    
    extracted_keywords = [kw for kw in possible_keywords if kw in clean_text]
    
    return {
        "ticket_id": ticket.get("id", "T-AUTO"),
        "category": ticket.get("category", "General IT"),
        "priority": ticket.get("priority", "Medium"),
        "keywords": extracted_keywords,
        "query": clean_text.strip()
    }