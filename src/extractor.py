import json
import re
from typing import List, Optional

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic.v1 import BaseModel, Field
from langchain_ollama import ChatOllama

# --- 1. Data Structures (Tolerant Mode) ---
class JobPostingSchema(BaseModel):
    normalized_title: Optional[str] = Field(default=None, description="The standardized job title in English.")
    min_years_experience: Optional[int] = Field(default=0, description="Minimum years of experience required.")
    hard_skills: Optional[List[str]] = Field(default_factory=list, description="List of technical skills/tools.")
    soft_skills: Optional[List[str]] = Field(default_factory=list, description="List of soft skills.")
    is_remote: Optional[bool] = Field(default=False, description="True if remote work is mentioned.")
    language_requirements: Optional[List[str]] = Field(default_factory=list, description="List of required languages.")


# --- 2. Extraction engine (Prompt syntax fixed) ---
class JobExtractor:
    def __init__(self, model_name: str = "llama3.2"):
        # Using temperature=0 reduces the probability of incoherent speech.
        self.llm = ChatOllama(model=model_name, temperature=0)

        system_instruction = """
        You are an expert HR Data Analyst. 
        Extract job requirements strictly as a JSON object.

        CRITICAL RULES:
        1. Output ONLY the JSON object. 
        2. Do NOT include markdown formatting like ```json.
        3. Do NOT include any introductory text.
        4. Translate Swedish values to English.

        Target JSON Format:
        {{
            "normalized_title": "string",
            "min_years_experience": int,
            "hard_skills": ["skill1", "skill2"],
            "soft_skills": ["skill1", "skill2"],
            "is_remote": boolean,
            "language_requirements": ["lang1", "lang2"]
        }}
        """

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_instruction),
            ("user", "Job Description:\n{text}")
        ])

        # Manually process text without using a parser.
        self.chain = self.prompt | self.llm

    def _clean_json_text(self, raw_text: str) -> str:
        """
        Clean up dirty data output from Llama 3
        """
        text = raw_text.strip()

        # 1. Try to extract content from a markdown code block.
        match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
        if match:
            text = match.group(1)

        # 2. Find the first { and the last }
        start = text.find("{")
        end = text.rfind("}") + 1

        if start != -1 and end != -1:
            return text[start:end]

        return text

    def extract(self, job_text: str) -> Optional[JobPostingSchema]:
        try:
            safe_text = str(job_text)[:3000]

            # 1. Get the original reply
            response = self.chain.invoke({"text": safe_text})
            raw_content = response.content

            # 2. Clean text
            json_str = self._clean_json_text(raw_content)

            # 3. Parsing JSON
            data = json.loads(json_str)

            return JobPostingSchema(**data)

        except json.JSONDecodeError:
            print(f"⚠️ JSON parsing failed (Raw output invalid): {raw_content[:50]}...")
            return None
        except Exception as e:
            print(f"⚠️ Extraction error: {e}")
            return None