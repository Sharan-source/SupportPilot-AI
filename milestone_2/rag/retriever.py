import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import MIN_RELEVANCE_THRESHOLD, TOP_K_DOCUMENTS, KB_FILE_PATH

class KnowledgeRetriever:
    def __init__(self, kb_path: str = KB_FILE_PATH):
        self.kb_path = kb_path
        self.documents = self._load_documents()
        self.texts = [f"{d['title']} {d['content']}" for d in self.documents]
        
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
        self.doc_vectors = self.vectorizer.fit_transform(self.texts)

    def _load_documents(self):
        if not os.path.exists(self.kb_path):
            raise FileNotFoundError(f"Knowledge Base file not found at {self.kb_path}")
        with open(self.kb_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def search(self, query: str, top_k: int = TOP_K_DOCUMENTS, min_score: float = MIN_RELEVANCE_THRESHOLD):
        """
        Step 2: Knowledge Base Retrieval.
        Computes cosine similarity between query and KB documents.
        Filters by min_score threshold.
        """
        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.doc_vectors)[0]
        ranked_indices = scores.argsort()[::-1]
        
        results = []
        for idx in ranked_indices[:top_k]:
            score = float(scores[idx])
            if score >= min_score:
                doc = dict(self.documents[idx])
                doc["score"] = round(score, 3)
                results.append(doc)
                
        return results