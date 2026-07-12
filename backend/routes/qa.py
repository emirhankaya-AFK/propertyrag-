from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.llm_service import LLMService
from ..services.rag_service import RAGService
from ..agents.qa_agent import QAAgent

router = APIRouter(prefix="/qa", tags=["qa"])

llm_service = LLMService()
rag_service = RAGService(llm_service)
qa_agent = QAAgent(llm_service, rag_service)

class QuestionRequest(BaseModel):
    question: str

@router.post("/{prop_id}/ask")
async def ask_property_question(prop_id: str, req: QuestionRequest):
    try:
        ans = qa_agent.answer_question(prop_id, req.question)
        return ans
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
