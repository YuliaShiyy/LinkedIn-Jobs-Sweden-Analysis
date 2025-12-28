import re
from typing import Dict, Any

from .extractor import JobExtractor


class HybridPipeline:
    """
    Combines Deterministic Rules (Regex/Keywords) with Probabilistic AI (LLM).
    Thesis Alignment: "Hybrid AI with Rule-Based Engineering Reasoning"
    """

    def __init__(self):
        print("Initializing Hybrid Pipeline (Rule Engine + AI)...")
        self.ai_extractor = JobExtractor()

        # --- Rule-Based Efficiency ---
        # 1. Email Regular Expression (General)
        self.email_regex = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

        # 2. Swedish/English Keyword Rule Base
        self.critical_keywords = {
            "driving_license": ["driving license", "körkort", "b-körkort"],
            "security_clearance": ["security clearance", "säkerhetsprövning", "laglydighetsintyg"],
            "remote_keywords": ["remote", "distans", "hemifrån"]
        }

    def _apply_rules(self, text: str) -> Dict[str, Any]:
        """
        Deterministic layer: Extract data that rules can handle faster and cheaper than LLMs.
        """
        text_lower = text.lower()
        rules_result = {}

        # Rule 1: Extract Contact Email
        emails = self.email_regex.findall(text)
        rules_result['contact_email'] = emails[0] if emails else None

        # Rule 2: Check for Driving License (Commonly found in service industry/logistics jobs)
        rules_result['has_driving_license'] = any(kw in text_lower for kw in self.critical_keywords["driving_license"])

        # Rule 3: Preliminary Remote Check ((The rules-based predictions can be cross-validated with the AI results)
        rules_result['rule_based_remote'] = any(kw in text_lower for kw in self.critical_keywords["remote_keywords"])

        return rules_result

    def process_job(self, raw_text: str) -> Dict[str, Any]:
        """
        Main execution flow: Unstructured Text -> Hybrid Processing -> Structured Dict
        """
        # Step 1: Rule Engine (Fast Filtering)
        final_data = self._apply_rules(raw_text)

        # Step 2: AI Engine (Deep Semantic Extraction)
        ai_result = self.ai_extractor.extract(raw_text)

        # Step 3: Fusion Strategy
        if ai_result:
            # AI is responsible for complex normalization and generalization.
            final_data['title_normalized'] = ai_result.normalized_title
            final_data['experience_min'] = ai_result.min_years_experience
            final_data['hard_skills'] = ai_result.hard_skills
            final_data['soft_skills'] = ai_result.soft_skills
            final_data['languages'] = ai_result.language_requirements

            # Hybrid decision example: Remote state
            # If the rule detects 'distans' or the AI identifies it as Remote, we consider it Remote (high recall strategy).
            final_data['is_remote'] = ai_result.is_remote or final_data.get('rule_based_remote', False)

            final_data['extraction_status'] = "Success"
        else:
            final_data['extraction_status'] = "AI Failed"
            # Even if the AI fails, we still retain the email and keyword information extracted from the rules.

        return final_data