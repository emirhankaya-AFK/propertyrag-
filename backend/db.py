import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from .config import settings

def get_db_connection():
    conn = sqlite3.connect(settings.SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS properties (
        id TEXT PRIMARY KEY,
        address TEXT NOT NULL,
        purchase_price REAL NOT NULL,
        down_payment REAL,
        interest_rate REAL,
        holding_period_years INTEGER,
        building_sqft INTEGER,
        lot_size_sqft INTEGER,
        bedrooms INTEGER,
        bathrooms REAL,
        year_built INTEGER,
        annual_tax REAL,
        monthly_rent_estimate REAL,
        file_path TEXT,
        created_at TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id TEXT PRIMARY KEY,
        property_id TEXT NOT NULL,
        doc_type TEXT NOT NULL,
        file_path TEXT NOT NULL,
        raw_text TEXT,
        parsed_metadata TEXT,
        FOREIGN KEY (property_id) REFERENCES properties (id) ON DELETE CASCADE
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS risks (
        property_id TEXT PRIMARY KEY,
        overall_risk_score INTEGER,
        risks_json TEXT,
        FOREIGN KEY (property_id) REFERENCES properties (id) ON DELETE CASCADE
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS investments (
        property_id TEXT PRIMARY KEY,
        cap_rate REAL,
        cash_on_cash REAL,
        npv REAL,
        irr REAL,
        data_json TEXT,
        FOREIGN KEY (property_id) REFERENCES properties (id) ON DELETE CASCADE
    )
    """)
    conn.commit()
    conn.close()

# Property operations
def save_property(prop: Dict[str, Any]) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO properties (
        id, address, purchase_price, down_payment, interest_rate, holding_period_years,
        building_sqft, lot_size_sqft, bedrooms, bathrooms, year_built, annual_tax,
        monthly_rent_estimate, file_path, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        prop["id"], prop["address"], prop["purchase_price"],
        prop.get("down_payment"), prop.get("interest_rate"), prop.get("holding_period_years"),
        prop.get("building_sqft", 1500), prop.get("lot_size_sqft", 7000),
        prop.get("bedrooms", 3), prop.get("bathrooms", 2.0), prop.get("year_built", 2000),
        prop.get("annual_tax", prop["purchase_price"] * 0.012),
        prop.get("monthly_rent_estimate", prop["purchase_price"] * 0.007),
        prop.get("file_path"),
        prop.get("created_at", datetime.now().isoformat())
    ))
    conn.commit()
    conn.close()

def get_property(prop_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    row = cursor.execute("SELECT * FROM properties WHERE id = ?", (prop_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def list_properties() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM properties ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_property(prop_id: str) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM properties WHERE id = ?", (prop_id,))
    cursor.execute("DELETE FROM documents WHERE property_id = ?", (prop_id,))
    cursor.execute("DELETE FROM risks WHERE property_id = ?", (prop_id,))
    cursor.execute("DELETE FROM investments WHERE property_id = ?", (prop_id,))
    conn.commit()
    conn.close()

# Document operations
def save_document(doc: Dict[str, Any]) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO documents (id, property_id, doc_type, file_path, raw_text, parsed_metadata)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        doc["id"], doc["property_id"], doc["doc_type"], doc["file_path"],
        doc.get("raw_text"), json.dumps(doc.get("parsed_metadata", {}))
    ))
    conn.commit()
    conn.close()

def list_property_documents(prop_id: str) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM documents WHERE property_id = ?", (prop_id,)).fetchall()
    conn.close()
    docs = []
    for r in rows:
        d = dict(r)
        d["parsed_metadata"] = json.loads(d["parsed_metadata"]) if d["parsed_metadata"] else {}
        docs.append(d)
    return docs

# Risk operations
def save_risk_assessment(prop_id: str, score: int, risks: List[Dict[str, Any]]) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO risks (property_id, overall_risk_score, risks_json)
    VALUES (?, ?, ?)
    """, (prop_id, score, json.dumps(risks)))
    conn.commit()
    conn.close()

def get_risk_assessment(prop_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    row = cursor.execute("SELECT * FROM risks WHERE property_id = ?", (prop_id,)).fetchone()
    conn.close()
    if row:
        r = dict(row)
        r["risks"] = json.loads(r["risks_json"])
        return r
    return None

# Investment operations
def save_investment_analysis(prop_id: str, cap_rate: float, coc: float, npv: float, irr: float, data: Dict[str, Any]) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO investments (property_id, cap_rate, cash_on_cash, npv, irr, data_json)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (prop_id, cap_rate, coc, npv, irr, json.dumps(data)))
    conn.commit()
    conn.close()

def get_investment_analysis(prop_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    row = cursor.execute("SELECT * FROM investments WHERE property_id = ?", (prop_id,)).fetchone()
    conn.close()
    if row:
        r = dict(row)
        r["data"] = json.loads(r["data_json"])
        return r
    return None
