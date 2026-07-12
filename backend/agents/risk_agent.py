import yaml
from pathlib import Path
from typing import List, Dict, Any
from ..services.llm_service import LLMService
from ..models.risk import RiskAssessment, RiskItem

class RiskAgent:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service
        self.risk_rules = self._load_risk_rules()

    def _load_risk_rules(self) -> Dict[str, Any]:
        rules_path = Path(__file__).parent.parent / "config" / "risk_rules.yaml"
        if rules_path.exists():
            with open(rules_path, "r") as f:
                return yaml.safe_load(f)
        return {}

    def assess_risks(self, property_id: str, doc_text: str) -> RiskAssessment:
        """
        Extracts risks from text using LLM and computes a weighted risk score based on risk rules.
        """
        sample_text = doc_text[:12000]
        variables = {"text": sample_text}
        
        # Extract risks list
        raw_risks = self.llm.generate_json("risk", variables)
        
        risk_items = []
        overall_score = 0
        
        # Calculate score penalties
        for r in raw_risks:
            item = RiskItem(
                category=r.get("category", "structural"),
                risk=r.get("risk", "Unknown risk"),
                severity=r.get("severity", "low"),
                details=r.get("details", "")
            )
            risk_items.append(item)
            
            # Map keyword penalty
            desc = item.risk.lower() + " " + item.details.lower()
            penalty = 0
            
            # Check rules
            for category, rules in self.risk_rules.items():
                for keyword, value in rules.items():
                    # If keyword matches the descriptions (e.g. "foundation", "lien")
                    clean_keyword = keyword.replace("_", " ")
                    if clean_keyword in desc:
                        penalty = max(penalty, value)
                        
            # If no keyword matches, assign base severity penalty
            if penalty == 0:
                severity_map = {"high": 20, "medium": 10, "low": 5}
                penalty = severity_map.get(item.severity, 5)
                
            overall_score += penalty
            
        # Bound score between 0 and 100
        overall_score = min(100, max(0, overall_score))
        
        return RiskAssessment(
            property_id=property_id,
            overall_risk_score=overall_score,
            risks=risk_items
        )
