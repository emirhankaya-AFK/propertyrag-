import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .db import init_db
from .routes import properties, analysis, investment, comparable, qa, reports

app = FastAPI(
    title="PropertyRAG API",
    description="Real Estate Property Advisor Backend",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(properties.router, prefix="/api")
app.include_router(analysis.router, prefix="/api")
app.include_router(investment.router, prefix="/api")
app.include_router(comparable.router, prefix="/api")
app.include_router(qa.router, prefix="/api")
app.include_router(reports.router, prefix="/api")

@app.on_event("startup")
def startup_event():
    init_db()
    print("PropertyRAG database initialized successfully.")

@st_route_test_check := app.get("/")
def read_root():
    return {"message": "Welcome to PropertyRAG API server."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=settings.BACKEND_PORT, reload=True)
