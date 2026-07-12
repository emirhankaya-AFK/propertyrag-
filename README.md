# PropertyRAG - Real Estate Property Advisor Agent

PropertyRAG is a professional property analysis, risk evaluation, and investment modeling application. It reads uploaded property deeds, appraisal reports, and home inspections, extracts property characteristics, calculates risk indexes, computes mortgage and NPV/IRR cash-flows, compares neighborhood comps, and renders Buy/Pass reports.

---

## Tech Stack
- **Backend API**: FastAPI + Uvicorn
- **RAG & Vector Storage**: ChromaDB + Gemini Embeddings (`models/embedding-001`)
- **LLM**: Gemini API (`gemini-2.0-flash`)
- **Document Parser**: PyMuPDF (`fitz`)
- **Comparable Sales**: Zillow/Redfin mock API integrations (with automatic variances)
- **Financial Projections**: Cash flow sheets, mortgage amortization, NPV, and Internal Rate of Return (IRR) models
- **Frontend Dashboard**: Streamlit

---

## Directory Structure
```
propertyrag/
├── backend/
│   ├── main.py              # FastAPI server entrypoint
│   ├── db.py                # SQLite database helper
│   ├── routes/              # FastAPI router endpoints
│   ├── agents/              # Custom LLM agents
│   ├── services/            # PDF parsing, financial calculations, RAG, and Zillow/Redfin APIs
│   ├── models/              # Pydantic schemas
│   └── config/              # Prompts, risk rules, market settings
├── frontend/
│   ├── app.py               # Streamlit application
│   ├── pages/               # Sidebar subpages
│   └── components/          # Investment calculator grids, comps bars, PDF views
├── tests/
│   ├── generate_test_property_doc.py # Mock inspection PDF program
│   ├── test_extraction.py   # Inspection & risk tests
│   ├── test_investment_calc.py # Amortization, NPV, IRR tests
│   └── test_market_data.py  # Comps database tests
├── requirements.txt
└── README.md
```

---

## Installation & Setup

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Gemini Credentials**:
   Get an API key from Google AI Studio and set the environment variable:
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```
   *Note: If no API key is set, the application will run in mock mode with pre-baked responses for offline testing.*

---

## Running the Application

### 1. Launch FastAPI Backend
```bash
python -m backend.main
```
The backend API server will run at `http://127.0.0.1:8002`. You can view the OpenAPI documentation at `http://127.0.0.1:8002/docs`.

### 2. Launch Streamlit Frontend
```bash
streamlit run frontend/app.py
```
The Streamlit app will launch at `http://localhost:8502`.

---

## Running Automated Tests
Run the test suite using `pytest`:
```bash
pytest tests/
```
