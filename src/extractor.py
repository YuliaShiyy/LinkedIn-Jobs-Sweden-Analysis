from typing import List, Optional

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic.v1 import BaseModel, Field
from langchain_ollama import ChatOllama



# --- Ontology ---
class JobPostingSchema(BaseModel):
    normalized_title: str = Field(description="The standardized job title in English.")
    min_years_experience: int = Field(description="Minimum years of experience required. 0 if unknown.")
    hard_skills: List[str] = Field(description="List of technical skills/tools.")
    soft_skills: List[str] = Field(description="List of soft skills.")
    is_remote: bool = Field(description="True if remote work is mentioned.")
    language_requirements: List[str] = Field(description="List of required languages.")


class JobExtractor:
    def __init__(self, model_name: str = "llama3.2"):
        # Using the local Ollama model
        self.llm = ChatOllama(model=model_name, temperature=0)
        self.parser = PydanticOutputParser(pydantic_object=JobPostingSchema)

        system_instruction = """
        You are an expert HR Data Analyst. 
        Analyze the Job Description. Extract keys strictly as JSON.
        If input is Swedish, translate values to English.
        {format_instructions}
        """

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_instruction),
            ("user", "Job Description:\n{text}")
        ])

        self.chain = self.prompt | self.llm | self.parser

    def extract(self, job_text: str) -> Optional[JobPostingSchema]:
        try:
            safe_text = str(job_text)[:3000]  # Slightly control the local model context window
            return self.chain.invoke({
                "format_instructions": self.parser.get_format_instructions(),
                "text": safe_text
            })
        except Exception as e:
            print(f"⚠️ Extraction Error: {e}")
            return None