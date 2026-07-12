import fitz
from pathlib import Path

def create_sample_property_pdf(dest_path: str):
    """
    Programmatically creates a mock property inspection report PDF using PyMuPDF.
    """
    doc = fitz.open()
    page1 = doc.new_page()
    
    page1.insert_text((50, 50), "Home Inspection & Risk Assessment Audit", fontsize=18)
    page1.insert_text((50, 75), "Property Address: 742 Evergreen Terrace, Springfield", fontsize=12)
    page1.insert_text((50, 95), "Date of Audit: June 15, 2026", fontsize=10)
    
    spec_text = (
        "1. PHYSICAL SPECIFICATIONS\n"
        "Building Size: 1800 sqft\n"
        "Lot Size: 7500 sqft\n"
        "Bedrooms: 3\n"
        "Bathrooms: 2.0\n"
        "Year Built: 1995\n"
    )
    page1.insert_textbox(fitz.Rect(50, 120, 550, 240), spec_text, fontsize=10)
    
    findings_text = (
        "2. INSPECTION FINDINGS & STRUCTURAL AUDIT\n\n"
        "Foundation System: Concrete crawlspace. Minor foundation hairline cracking noticed along the "
        "interior north block wall. Recommendations: Monitor for future expansion, but currently stable.\n\n"
        "Roof System: Asphalt Shingles. The roof is approximately 22 years old and showing wear. Several "
        "shingles are curling. Recommendations: Replacement of shingles needed within 1-2 years to prevent water damage.\n\n"
        "HVAC System: Forced air furnace. Age: 16 years. Units are functional but nearing their average useful lifespan."
    )
    page1.insert_textbox(fitz.Rect(50, 260, 550, 480), findings_text, fontsize=10)
    
    # Page 2: Title and legal
    page2 = doc.new_page()
    legal_text = (
        "3. TITLE SEARCH & LEGAL RECORD AUDIT\n\n"
        "Deed Type: Warranty Deed.\n"
        "Active Liens: No active tax or mortgage liens recorded.\n"
        "Easements: Standard utility easement registered along the eastern boundary (5 feet setback) for power lines.\n"
        "Zoning Status: Single Family Residential conforming use."
    )
    page2.insert_textbox(fitz.Rect(50, 50, 550, 250), legal_text, fontsize=10)
    
    doc.save(dest_path)
    doc.close()
    print(f"Property PDF created at {dest_path}")

if __name__ == "__main__":
    dest = Path(__file__).parent.parent / "data" / "sample_inspection.pdf"
    dest.parent.mkdir(exist_ok=True, parents=True)
    create_sample_property_pdf(str(dest))
