import uuid
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from typing import List, Dict, Any

from ..config import settings
from ..db import save_property, save_document, list_properties, get_property, delete_property, save_risk_assessment, save_investment_analysis
from ..services.document_parser import DocumentParserService
from ..services.llm_service import LLMService
from ..services.rag_service import RAGService
from ..agents.extraction_agent import ExtractionAgent
from ..agents.risk_agent import RiskAgent
from ..agents.investment_agent import InvestmentAgent

router = APIRouter(prefix="/properties", tags=["properties"])

llm_service = LLMService()
rag_service = RAGService(llm_service)
extraction_agent = ExtractionAgent(llm_service)
risk_agent = RiskAgent(llm_service)

def process_property_doc_background(prop_id: str, doc_id: str, file_path: str, filename: str):
    try:
        # 1. Parse document text
        parsed_data = DocumentParserService.parse_pdf(file_path)
        doc_type = parsed_data["doc_type"]
        
        # 2. Index in ChromaDB RAG
        meta = {
            "doc_type": doc_type,
            "address": filename.replace(".pdf", "")
        }
        rag_service.index_document(doc_id, prop_id, parsed_data["full_text"], meta)
        
        # 3. Save document entry in SQLite
        doc_record = {
            "id": doc_id,
            "property_id": prop_id,
            "doc_type": doc_type,
            "file_path": file_path,
            "raw_text": parsed_data["full_text"],
            "parsed_metadata": meta
        }
        save_document(doc_record)
        
        # 4. If it's a deed or inspection report, update property features
        prop = get_property(prop_id)
        if prop:
            ext_details = extraction_agent.extract_property_details(parsed_data["full_text"], filename)
            
            # Save updated property data
            updated_prop = {
                **prop,
                "building_sqft": ext_details.get("building_sqft", prop["building_sqft"]),
                "lot_size_sqft": ext_details.get("lot_size_sqft", prop["lot_size_sqft"]),
                "bedrooms": ext_details.get("bedrooms", prop["bedrooms"]),
                "bathrooms": ext_details.get("bathrooms", prop["bathrooms"]),
                "year_built": ext_details.get("year_built", prop["year_built"]),
                "file_path": file_path
            }
            save_property(updated_prop)
            
            # Run background risk evaluation
            assess = risk_agent.assess_risks(prop_id, parsed_data["full_text"])
            save_risk_assessment(prop_id, assess.overall_risk_score, [r.model_dump() for r in assess.risks])
            
            # Run background investment evaluation
            inv = InvestmentAgent.analyze_investment(
                property_id=prop_id,
                price=prop["purchase_price"],
                down_payment=prop["down_payment"],
                interest_rate=prop["interest_rate"],
                holding_years=prop["holding_period_years"],
                monthly_rent=prop["purchase_price"] * 0.007
            )
            save_investment_analysis(
                prop_id,
                inv.cap_rate,
                inv.cash_on_cash_return,
                inv.npv_10_years,
                inv.irr_10_years,
                inv.model_dump()
            )
            
        print(f"Property document processing complete for property {prop_id}, doc {doc_id}")
    except Exception as e:
        print(f"Error processing property document: {e}")

@router.post("/")
async def create_property(prop: Dict[str, Any]):
    prop_id = str(uuid.uuid4())
    prop["id"] = prop_id
    
    # Defaults
    prop["building_sqft"] = prop.get("building_sqft", 1500)
    prop["lot_size_sqft"] = prop.get("lot_size_sqft", 7000)
    prop["bedrooms"] = prop.get("bedrooms", 3)
    prop["bathrooms"] = prop.get("bathrooms", 2.0)
    prop["year_built"] = prop.get("year_built", 2000)
    prop["annual_tax"] = prop.get("annual_tax", prop["purchase_price"] * 0.012)
    prop["monthly_rent_estimate"] = prop.get("monthly_rent_estimate", prop["purchase_price"] * 0.007)
    
    save_property(prop)
    return {"message": "Property created successfully.", "property_id": prop_id}

@router.post("/{prop_id}/upload-doc")
async def upload_property_doc(prop_id: str, background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    prop = get_property(prop_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found.")
        
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF documents are supported.")
        
    doc_id = str(uuid.uuid4())
    safe_filename = f"{doc_id}.pdf"
    dest_path = settings.UPLOAD_DIR / safe_filename
    
    # Save file to uploads dir
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Trigger background parsing
    background_tasks.add_task(
        process_property_doc_background,
        prop_id,
        doc_id,
        str(dest_path),
        file.filename
    )
    
    return {
        "message": "Property document uploaded and is processing in the background.",
        "doc_id": doc_id
    }

@router.get("/")
async def get_all_properties():
    return list_properties()

@router.get("/{prop_id}")
async def get_single_property(prop_id: str):
    prop = get_property(prop_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found.")
    return prop

@router.delete("/{prop_id}")
async def remove_property(prop_id: str):
    prop = get_property(prop_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found.")
        
    # Delete SQLite records
    delete_property(prop_id)
    # Delete ChromaDB entries
    rag_service.delete_property_index(prop_id)
    
    return {"message": f"Property {prop_id} deleted successfully."}
