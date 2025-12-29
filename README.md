# LinkedIn Jobs Analysis

This project documents the evolution of a data pipeline designed to analyze the Swedish job market. It started as a traditional data analysis project and was upgraded into an AI-powered engineering solution to handle unstructured data challenges.
It is part of the broader [LinkedIn Jobs Pipeline Project](https://github.com/yuliashiyy/linkedin-jobs-pipeline).

---
## 📈 Project Evolution

The project was built in two distinct phases to address the limitations of traditional keyword matching:

Phase 1: The Foundation (Traditional EDA)
 - Goal: Understand basic metrics (City distribution, Top companies).

 - Method: Pandas, Regex, and Standard Visualization.

Phase 2: The AI Upgrade (Local RAG & LLMs) 
 - Goal: Solve semantic normalization and extract structured skills from unstructured text.

 - Method: Implemented Local LLMs (Ollama/Llama 3) and a RAG (Retrieval-Augmented Generation) architecture.

 - Result: The system now outputs standardized JSON objects (Schema-enforced), intelligently separating technical stacks from personality traits, and enables Context-Aware Search (RAG).


---
## 📊 Features by Phase
Phase 1: Data Cleaning & Analysis
- Data Deduplication: Removed duplicate job entries based on `job_id`.
- Metric Calculation: Computed "Competitiveness" metric:
    \[
    Competitiveness = \frac{Applications}{Days Posted + 1}
    \]
- Visualizations: Static charts for geographical distribution and application trends. 

Phase 2: AI-Enhanced Capabilities
- Hybrid Extraction Engine:
  - Combines Rules (for emails/licenses) + Generative AI (for nuanced skills).
  - Robust parsing logic to handle "noisy" outputs from Local SLMs.
- Semantic Normalization:
  - Auto-translates Swedish requirements to English standards.

- Local RAG System:
  - Vector-based semantic search using ChromaDB.
  - Context-aware Q&A without sending data to the cloud.
---

## 📂 Project Structure
    linkedin-jobs-analysis/
    │
    ├── data/
    │ ├── linkedin_jobs_sample.csv
    │ └── linkedin_jobs_cleaned_with_skills.csv
    │
    ├── notebooks/
    │ ├── analysis.ipynb
    │ └── ai_features_demo.ipynb
    |
    ├── src/
    │ ├── __init__.py
    │ ├── extractor.py
    │ ├── rag_engine.py
    │ └── hybrid_logic.py
    |
    ├── visualizations/
    │ ├── top10_cities.png
    │ ├── top10_companies.png
    │ ├── applications_distribution.png
    │ ├── competitiveness_distribution.png
    │ ├── top20_skills.png
    │ └── skills_wordcloud.png
    │
    ├── report/
    │ └── linkedin_jobs_analysis.docx
    │
    ├── requirements.txt
    └── README.md

---

## ⚙️ Requirements
See `requirements.txt` for full dependencies. Key technologies include:
- Python 3.10+
- Ollama (running llama3.2)
- LangChain
- ChromaDB


---

## 🚀 Usage
Step 1: Basic Analysis (Phase 1)
To see standard data visualization:
1. Clone the repo:
   ```bash
   git clone https://github.com/yuliashiyy/linkedin-jobs-analysis.git

2. Install requirements:
   ```bash
    pip install -r requirements.txt

3. Open the notebook:
   ```bash
    jupyter notebook notebooks/analysis.ipynb

Step 2: AI Features (Phase 2 Upgrade)
To experience the Local LLM and RAG pipeline:
1. Install Ollama: Download from ollama.com.
   
2.Pull Model: ollama pull llama3.2

3.Run Notebook:
  ```bash
  jupyter notebook notebooks/02_ai_features_demo.ipynb
  ```

---

## ⚙️ Technology Stack Upgrade

| Component | Phase 1 (Original) | Phase 2 (Upgraded) |
| :--- | :--- | :--- |
| **Language Handling** | Translation APIs | **LLM Semantic Understanding** |
| **Parsing Strategy** | Keyword Matching / Regex | **Contextual Extraction (JSON)** |
| **Search Logic** | Filter-based (e.g., city match) | **Vector Similarity (RAG)** |
| **Core Engine** | Pandas + Plotly | **LangChain + Ollama + ChromaDB** |

## 📌 Related Repositories

- [LinkedIn Jobs Scraper](https://github.com/yuliashiyy/linkedin-jobs-scraper)  
- [LinkedIn Jobs Pipeline](https://github.com/yuliashiyy/linkedin-jobs-pipeline)  
