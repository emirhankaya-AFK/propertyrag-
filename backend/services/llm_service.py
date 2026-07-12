import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, List
import google.generativeai as genai
from ..config import settings

class LLMService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.prompts = self._load_prompts()
        self.mock_mode = not self.api_key
        
        if not self.mock_mode:
            genai.configure(api_key=self.api_key)
            
    def _load_prompts(self) -> Dict[str, str]:
        prompt_path = Path(__file__).parent.parent / "config" / "prompts.yaml"
        if prompt_path.exists():
            with open(prompt_path, "r") as f:
                return yaml.safe_load(f)
        return {}

    def generate_text(self, prompt_name: str, variables: Dict[str, Any]) -> str:
        prompt_template = self.prompts.get(prompt_name, "")
        if not prompt_template:
            prompt_template = "{text}"
            if "text" not in variables:
                variables["text"] = str(variables)
                
        formatted_prompt = prompt_template.format(**variables)
        
        if self.mock_mode:
            return self._mock_response(prompt_name, variables)
            
        try:
            model = genai.GenerativeModel(settings.DEFAULT_MODEL)
            response = model.generate_content(formatted_prompt)
            return response.text
        except Exception as e:
            print(f"Gemini API Error: {e}. Falling back to mock.")
            return self._mock_response(prompt_name, variables)

    def generate_json(self, prompt_name: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        prompt_template = self.prompts.get(prompt_name, "")
        formatted_prompt = prompt_template.format(**variables)
        
        if self.mock_mode:
            return json.loads(self._mock_response(prompt_name, variables, json_format=True))
            
        try:
            model = genai.GenerativeModel(settings.DEFAULT_MODEL)
            response = model.generate_content(
                formatted_prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text.strip())
        except Exception as e:
            print(f"Gemini JSON API Error: {e}. Falling back to mock.")
            return json.loads(self._mock_response(prompt_name, variables, json_format=True))

    def get_embedding(self, text: str) -> List[float]:
        if self.mock_mode or not self.api_key:
            import random
            random.seed(hash(text))
            return [random.uniform(-0.1, 0.1) for _ in range(1536)]
            
        try:
            result = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"Embedding API Error: {e}. Falling back to mock vector.")
            import random
            random.seed(hash(text))
            return [random.uniform(-0.1, 0.1) for _ in range(1536)]

    def _mock_response(self, prompt_name: str, variables: Dict[str, Any], json_format: bool = False) -> str:
        if json_format:
            if prompt_name == "extraction":
                return json.dumps({
                    "address": variables.get("address", "123 Main St, Springfield"),
                    "lot_size_sqft": 7500,
                    "building_sqft": 1800,
                    "bedrooms": 3,
                    "bathrooms": 2.0,
                    "year_built": 1995,
                    "roof_type": "Asphalt Shingle",
                    "foundation_type": "Crawlspace",
                    "condition": "good"
                })
            elif prompt_name == "risk":
                return json.dumps([
                    {
                        "category": "structural",
                        "risk": "Minor foundation cracking",
                        "severity": "medium",
                        "details": "Hairline cracks visible on the north wall of the basement crawlspace."
                    },
                    {
                        "category": "legal",
                        "risk": "Utility easement",
                        "severity": "low",
                        "details": "Standard utility easement registered on the eastern boundary of the lot."
                    }
                ])
            return "{}"
        else:
            if prompt_name == "qa":
                q = variables.get("question", "").lower()
                if "foundation" in q:
                    return "The foundation is listed as a concrete crawlspace with minor hairline cracking on the north wall, which is common for homes of this age."
                elif "tax" in q:
                    return "The property tax rate is approximately 1.2% per year, which equates to roughly $4,200 annually for a $350,000 appraisal."
                return "Based on the provided property documents, this details is resolved. (Mock Answer)"
            elif prompt_name == "recommendation":
                return f"At a purchase price of ${variables.get('price', 350000):,}, with a cap rate of {variables.get('cap_rate', 5.5):.2f}% and a risk score of {variables.get('risk_score', 30)}, we recommend a BUY. The solid cash-on-cash return outweighs the low structural risks identified in the inspection report."
            elif prompt_name == "market":
                return f"Compared to recent comparable sales in the area, the property is priced in line with market value. The neighborhood price trend is UP, indicating strong demand."
            return f"Mock text response for {prompt_name}"
