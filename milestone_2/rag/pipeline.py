import time
from datetime import datetime
from rag.analyzer import analyze_ticket
from rag.retriever import KnowledgeRetriever
from rag.generator import build_context, generate_resolution

class RAGPipeline:
    def __init__(self, retriever: KnowledgeRetriever = None):
        self.retriever = retriever or KnowledgeRetriever()

    def run(self, ticket: dict) -> dict:
        """
        Executes the 4 RAG stages while recording precise execution timestamps.
        """
        start_total = time.time()
        workflow_timeline = []

        # Stage 1: Ticket Analysis
        t0 = time.time()
        analysis = analyze_ticket(ticket)
        t1 = time.time()
        workflow_timeline.append({
            "stage_num": 1,
            "name": "Ticket Analysis & Query Generation",
            "status": "completed",
            "elapsed_ms": round((t1 - t0) * 1000, 1),
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3]
        })

        # Stage 2: Knowledge Base Retrieval
        t0 = time.time()
        docs = self.retriever.search(analysis["query"])
        t1 = time.time()
        workflow_timeline.append({
            "stage_num": 2,
            "name": "Knowledge Base Retrieval",
            "status": "completed",
            "elapsed_ms": round((t1 - t0) * 1000, 1),
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3]
        })

        # Stage 3: Context Augmentation
        t0 = time.time()
        context = build_context(docs)
        t1 = time.time()
        workflow_timeline.append({
            "stage_num": 3,
            "name": "Context Augmentation",
            "status": "completed",
            "elapsed_ms": round((t1 - t0) * 1000, 1),
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3]
        })

        # Stage 4: Resolution Generation
        t0 = time.time()
        gen_result = generate_resolution(ticket, docs)
        t1 = time.time()
        workflow_timeline.append({
            "stage_num": 4,
            "name": "Response Generation",
            "status": "completed",
            "elapsed_ms": round((t1 - t0) * 1000, 1),
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3]
        })

        total_response_time = round(time.time() - start_total, 2)

        return {
            "ticket": ticket,
            "analysis": analysis,
            "retrieved_documents": docs,
            "context": context,
            "resolution": gen_result["resolution"],
            "citations": gen_result["citations"],
            "needs_escalation": gen_result["needs_escalation"],
            "timeline": workflow_timeline,
            "total_response_time": total_response_time
        }