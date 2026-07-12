from typing import Dict, Any
from ..services.llm_service import LLMService
from ..services.rag_service import RAGService

class QAAgent:
    def __init__(self, llm_service: LLMService, rag_service: RAGService):
        self.llm = llm_service
        self.rag = rag_service

    def answer_question(self, property_id: str, question: str) -> Dict[str, Any]:
        """
        Answers a user's question about property documents using ChromaDB chunks.
        """
        chunks = self.rag.query_property(property_id=property_id, query_text=question, n_results=4)
        
        if not chunks:
            return {
                "answer": "Not available in documents (No indexed content found).",
                "sources": []
            }
            
        context_parts = []
        sources = []
        for i, c in enumerate(chunks):
            doc_type = c["metadata"].get("doc_type", "unknown")
            text_chunk = c["text"]
            context_parts.append(f"--- Document Chunk {i+1} ({doc_type.upper()}) ---\n{text_chunk}")
            sources.append({
                "doc_type": doc_type,
                "score": float(c["score"]),
                "snippet": text_chunk[:150] + "..."
            })
            
        context = "\n\n".join(context_parts)
        
        variables = {
            "context": context,
            "question": question
        }
        
        answer = self.llm.generate_text("qa", variables)
        
        return {
            "answer": answer,
            "sources": sources
        }
