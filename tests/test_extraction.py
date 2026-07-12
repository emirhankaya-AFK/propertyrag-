import pytest
from pathlib import Path
from .generate_test_property_doc import create_sample_property_pdf
from backend.services.document_parser import DocumentParserService
from backend.services.llm_service import LLMService
from backend.agents.extraction_agent import ExtractionAgent
from backend.agents.risk_agent import RiskAgent

@pytest.fixture(scope="module")
def sample_pdf():
    pdf_path = Path(__file__).parent / "temp_test_prop.pdf"
    create_sample_property_pdf(str(pdf_path))
    yield str(pdf_path)
    if pdf_path.exists():
        pdf_path.unlink()

def test_document_parsing(sample_pdf):
    parsed = DocumentParserService.parse_pdf(sample_pdf)
    assert parsed["doc_type"] == "inspection"
    assert "742 Evergreen Terrace" in parsed["full_text"]

def test_details_extraction(sample_pdf):
    parsed = DocumentParserService.parse_pdf(sample_pdf)
    llm = LLMService()
    agent = ExtractionAgent(llm)
    res = agent.extract_property_details(parsed["full_text"], "temp_test_prop.pdf")
    
    assert res["bedrooms"] == 3
    assert res["building_sqft"] == 1800
    assert res["condition"] == "good"

def test_risk_assessment(sample_pdf):
    parsed = DocumentParserService.parse_pdf(sample_pdf)
    llm = LLMService()
    agent = RiskAgent(llm)
    assess = agent.assess_risks("prop_1", parsed["full_text"])
    
    assert assess.overall_risk_score > 0
    assert len(assess.risks) > 0
    # Foundation cracking is structural
    categories = [r.category for r in assess.risks]
    assert "structural" in categories
