from rag.pipeline import RAGPipeline

ticket = {
    "id": "T-2023-4521",
    "title": "VPN Connection Failing on Corporate Network",
    "description": "Unable to connect to VPN since this morning. Error message: Connection timed out. Please check your network settings and try again.",
    "category": "Network Connectivity",
    "priority": "High"
}

pipeline = RAGPipeline()
result = pipeline.run(ticket)

print("\n" + "=" * 60)
print(f"RAG PIPELINE RESULT FOR {ticket['id']}")
print("=" * 60)
print("Query Keywords:", result["analysis"]["keywords"])
print("\nRetrieved Articles:")
for doc in result["retrieved_documents"]:
    print(f" • {doc['title']} (Score: {doc['score']})")

print("\nGenerated Resolution:")
print(result["resolution"])

print("\nTime Sequence:")
for step in result["timeline"]:
    print(f" [{step['stage_num']}] {step['name']} -> {step['elapsed_ms']} ms ({step['timestamp']})")
print(f"Total Time: {result['total_response_time']}s")
print("=" * 60)