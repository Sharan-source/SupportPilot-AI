def build_context(retrieved_docs: list) -> str:
    """
    Step 3: Context Augmentation.
    Formats retrieved KB articles into structured context.
    """
    if not retrieved_docs:
        return "No relevant enterprise knowledge base articles found."
    
    context_blocks = []
    for doc in retrieved_docs:
        block = (
            f"SOURCE: {doc['id']} - {doc['title']} (Relevance: {doc['score'] * 100:.1f}%)\n"
            f"CATEGORY: {doc.get('category', 'General')}\n"
            f"{doc['content'].strip()}\n"
            f"----------------------------------------"
        )
        context_blocks.append(block)
    return "\n".join(context_blocks)

def generate_resolution(ticket: dict, retrieved_docs: list) -> dict:
    """
    Step 4: Resolution Generation with Citations (Slide 14).
    Produces step-by-step guidance referencing the KB documents.
    """
    if not retrieved_docs:
        return {
            "status": "UNRESOLVED",
            "resolution": (
                "No sufficiently matching knowledge base article was found. "
                "The ticket requires human agent intervention for specialized investigation."
            ),
            "citations": [],
            "needs_escalation": True
        }

    steps = []
    citations = []

    for doc in retrieved_docs:
        citations.append(f"{doc['id']} ({doc['title']})")
        lines = doc["content"].split("\n")
        for line in lines:
            line = line.strip()
            # Extract numbered steps from the SOP
            if line and any(line.startswith(f"{i}.") for i in range(1, 10)):
                cleaned = line.split(".", 1)[1].strip()
                steps.append(f"• {cleaned} [Source: {doc['id']}]")

    if not steps:
        steps.append(f"• Refer to troubleshooting guidance in {retrieved_docs[0]['title']}.")

    steps.append("• If the issue persists, contact the internal escalation desk with diagnostics.")

    formatted_resolution = (
        "Generated Resolution (RAG-Assisted):\n" + "\n".join(steps[:5])
    )

    return {
        "status": "RESOLVED",
        "resolution": formatted_resolution,
        "citations": list(set(citations)),
        "needs_escalation": False
    }