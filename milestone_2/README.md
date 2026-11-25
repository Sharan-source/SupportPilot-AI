# 🧠 SupportPilot — Milestone 2: Knowledge Retrieval & Resolution Generation (RAG)

> **Enterprise AI Helpdesk Platform — Module 2: RAG-Powered Resolution Engine & Live Analytics**  
> *Developed as part of the Infosys Springboard AI/ML Internship.*

---

## 📌 Milestone 2 Overview

Milestone 2 advances the **SupportPilot** platform from classification to automated intelligent troubleshooting. It implements an enterprise **Retrieval-Augmented Generation (RAG)** pipeline that:
1. Takes classified IT tickets from Milestone 1.
2. Extracts key technical query terms.
3. Retrieves relevant Standard Operating Procedures (SOPs) from an enterprise Knowledge Base using **TF-IDF Vectorization** and **Cosine Similarity Ranking**.
4. Augments context with threshold validation ($\ge 0.30$ relevance).
5. Generates step-by-step troubleshooting actions explicitly cited to internal knowledge articles (e.g., `[Source: KB001]`).
6. Tracks elapsed execution time across 4 stages in milliseconds.
7. Logs 24-hour operational KPIs (Received, Solved, Escalated, Resolution Rate).
8. Supports **Human-in-the-Loop escalation** for unresolved tickets.
9. Displays interactive analytics graphs using **Chart.js**.

---

## 🏗️ Detailed RAG Workflow & Architecture

```mermaid
flowchart TD
    subgraph S1 ["Stage 1: Ticket Analysis & Query Generation"]
        T["Ticket Input\n(Title, Description, Category, Priority)"] --> AN["analyzer.py\n• Cleans special characters\n• Extracts keywords (vpn, network, firewall, dns, auth)\n• Formulates normalized search query"]
    end

    subgraph S2 ["Stage 2: Enterprise Knowledge Retrieval"]
        KB[("📚 knowledge_base.json\nEnterprise SOPs\n(KB001 - KB007)")] --> VEC["retriever.py\n• TfidfVectorizer(ngram=(1,2))\n• Pre-indexed KB Document Vectors"]
        AN --> Q["Vectorize Query"]
        Q --> CS["Cosine Similarity Calculation\nscore = cos(q_vec, doc_vec)"]
        VEC --> CS
        CS --> FILTER{"score >= 0.30\n(Threshold Check)"}
        FILTER -- Yes --> TOPK["Rank Top-K (k=3) Articles"]
        FILTER -- No / None --> NORET["Flag needs_escalation = True"]
    end

    subgraph S3 ["Stage 3: Context Augmentation"]
        TOPK --> CTX["generator.build_context()\nFormats structured KB blocks with relevance scores"]
    end

    subgraph S4 ["Stage 4: Resolution Generation with Citations"]
        CTX --> GEN["generator.generate_resolution()\n• Synthesizes actionable troubleshooting steps\n• Attaches source citations [Source: KB001]"]
        NORET --> ESC_MSG["Fallback: No matching SOP found.\nSuggests immediate Human Escalation."]
    end

    subgraph S5 ["Human-in-the-Loop & 24h Analytics"]
        GEN --> UI["Interactive Web Platform\n(Slide 2 Mockup UI)"]
        ESC_MSG --> UI
        UI --> ACT{"User Validation"}
        ACT -- "Yes, Mark as Solved" --> DB_SOLVED["Update status: 'Resolved'\nLogged in 24h Solved Metrics"]
        ACT -- "No, Approach Human Agent" --> DB_ESC["Update status: 'Escalated_To_Human'\nAssigned to Senior Engineer"]
        DB_SOLVED --> CHARTS["📊 Chart.js Dashboard Visualizations\n(Velocity, Category, Priority, Outcome)"]
        DB_ESC --> CHARTS
    end
```

---

## ⏱️ Real-Time 4-Stage Timeline Sequence

Every ticket processed by the RAG engine logs each stage with millisecond precision:

```mermaid
sequenceDiagram
    autonumber
    actor Employee as 👤 Employee
    participant App as 🌐 app.py
    participant Pipeline as ⚙️ rag/pipeline.py
    participant Retriever as 📚 rag/retriever.py
    participant Generator as 🤖 rag/generator.py
    participant DB as 💾 database.py

    Employee->>App: Submits IT Issue (Ticket Form / Preset)
    App->>Pipeline: pipeline.run(ticket)
    
    rect rgb(240, 248, 255)
        Pipeline->>Pipeline: [Stage 1] Ticket Analysis & Keywords (~0.1 ms)
        Pipeline->>Retriever: [Stage 2] TF-IDF Cosine Search (~2.8 ms)
        Retriever-->>Pipeline: Top-K Matching Documents (Score >= 0.30)
        Pipeline->>Generator: [Stage 3] Context Augmentation (~0.05 ms)
        Pipeline->>Generator: [Stage 4] Response Generation (~0.05 ms)
        Generator-->>Pipeline: Resolution with Citations [Source: KB001]
    end

    Pipeline-->>App: Full RAG Result + Timeline Metrics
    App->>DB: save_ticket(ticket, rag_result)
    App-->>Employee: Displays Resolution, 4-Stage Stepper & Action Buttons
```

---

## 📂 Milestone 2 File Directory

| File / Folder | Role & Implementation Details |
| :--- | :--- |
| **`app.py`** | Flask application hosting RAG endpoints, 24-hour KPI calculations, Chart.js analytics API, and HTML rendering on port `5001`. |
| **`config.py`** | Defines `MIN_RELEVANCE_THRESHOLD = 0.30`, `TOP_K_DOCUMENTS = 3`, and database/KB file paths. |
| **`database.py`** | SQLite persistence (`supportpilot_m2.db`), calculates 24-hour KPIs, provides structured chart analytics, and seeds initial data. |
| **`demo_rag.py`** | Terminal CLI test demonstrating the entire 4-stage RAG pipeline with millisecond timing diagnostics. |
| **`data/knowledge_base.json`** | Enterprise knowledge base containing SOPs for VPN, Network Firewall, Authentication/MFA, Wi-Fi/DNS, Password Unlock, Software Provisioning, and Server Downtime. |
| **`models/schemas.py`** | Dataclasses for `TicketInput`, `KBArticle`, and `WorkflowStep`. |
| **`rag/analyzer.py`** | Extracts domain keywords (`vpn`, `network`, `firewall`, `dns`, `authentication`) and builds normalized query. |
| **`rag/retriever.py`** | Uses `TfidfVectorizer(ngram_range=(1,2))` and `cosine_similarity` to retrieve and rank KB articles matching criteria. |
| **`rag/generator.py`** | Builds augmented context blocks and generates step-by-step troubleshooting actions with `[Source: KB001]` citations. |
| **`rag/pipeline.py`** | Orchestrates the 4 stages, measuring elapsed time in milliseconds for each phase. |
| **`templates/index.html`** | UI featuring Milestone banner, 24h KPI cards, RAG stepper, human escalation actions, and 4 Chart.js graphs. |

---

## 📊 Dashboard Visualizations & Graphs (Chart.js)

The Milestone 2 platform provides 4 real-time interactive charts:

1. **24-Hour Ticket Velocity & Resolution Trends (Line/Area Chart)**:
   - Compares hourly ticket ingestion rates against completed resolutions over the last 24 hours.
2. **Resolution Status Breakdown (Doughnut Chart)**:
   - Visualizes the proportion of **Automated Solved** tickets vs. **Escalated to Human Agent** vs. **Open**.
3. **Tickets by IT Category (Polar Area Chart)**:
   - Displays distribution across enterprise categories: *VPN Access*, *Network Connectivity*, *Password Reset*, *Software Provisioning*, and *System Outage*.
4. **ITIL Priority Matrix Breakdown (Bar Chart)**:
   - Highlights ticket volume across *P1 - Critical*, *P2 - High*, *P3 - Medium*, and *P4 - Low*.

---

## 🚨 Human-in-the-Loop Escalation Protocol

```mermaid
stateDiagram-v2
    [*] --> Ingested
    Ingested --> RAG_Processing: Query Analysis & Retrieval
    RAG_Processing --> Auto_Resolved: Score >= 0.30 (Troubleshooting Generated)
    RAG_Processing --> Escalated_To_Human: Score < 0.30 (No matching SOP)
    
    Auto_Resolved --> Solved: Employee Clicks "Yes, Mark as Solved"
    Auto_Resolved --> Escalated_To_Human: Employee Clicks "No, Approach Human Agent"
    
    Escalated_To_Human --> [*]: Assigned to Senior Support Engineer
    Solved --> [*]: Ticket Closed (24h Metric Updated)
```

* **"Yes, Mark as Solved"**: Validates the resolution, closes the ticket, and increments the 24-hour solved count.
* **"No, Approach Human Agent"**: Updates status to `Escalated_To_Human`, records the escalation in the 24-hour dashboard, and displays immediate guidance on support team assignment.

---

## 🔌 API Endpoints

### 1. Ingest Ticket & Run RAG Pipeline
* **Endpoint**: `POST /api/tickets/rag`
* **Payload**:
```json
{
  "title": "VPN connection failing on corporate network",
  "description": "Connection timed out on IPsec gateway port 500.",
  "category": "VPN Access",
  "priority": "High",
  "employee_name": "Arun Kumar",
  "email": "arun.k@company.com",
  "department": "Engineering"
}
```
* **Response**: Returns ticket ID, RAG resolution with citations, retrieved KB documents with scores, 4-stage timeline metrics, and updated 24h statistics.

### 2. Mark Ticket as Solved
* **Endpoint**: `POST /api/tickets/<ticket_id>/resolve`
* **Response**: Sets status to `Resolved` and returns updated 24h KPIs.

### 3. Escalate Ticket to Human Agent
* **Endpoint**: `POST /api/tickets/<ticket_id>/escalate`
* **Response**: Sets status to `Escalated_To_Human` and returns escalation confirmation.

### 4. Fetch Chart Analytics Data
* **Endpoint**: `GET /api/dashboard/charts`
* **Response**: JSON dataset for hourly trends, category breakdown, priority distribution, and resolution outcomes.

### 5. Knowledge Base Catalog
* **Endpoint**: `GET /api/knowledge-base`
* **Response**: Complete collection of indexed enterprise SOPs.

---

## 🚀 Execution & Testing Guide

### Step 1: Install Requirements
```bash
pip install -r requirements.txt
```

### Step 2: Run Terminal Pipeline Verification
```bash
python demo_rag.py
```

### Step 3: Launch Web Application
```bash
python app.py
```
Open your browser at:
👉 **`http://127.0.0.1:5001`**
