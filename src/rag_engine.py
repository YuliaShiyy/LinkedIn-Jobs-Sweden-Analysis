import os
import shutil
from typing import List, Optional

from langchain_community.document_loaders import CSVLoader
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_classic.chains import RetrievalQA

class JobRAGEngine:
    """
    Implements a RAG pipeline using LOCAL LLMs (Ollama).
    Thesis Alignment: "Privacy-Preserving AI" & "Local RAG"
    """

    def __init__(self, csv_path: str, source_column: str = "description", persist_dir: str = "./chroma_db_local"):
        self.csv_path = csv_path
        self.persist_dir = persist_dir

        # 1. Load Data
        print(f"Loading documents from {csv_path}...")
        try:
            self.loader = CSVLoader(file_path=csv_path, source_column=source_column, encoding="utf-8")
            self.documents = self.loader.load()
        except Exception as e:
            print(f"Error loading CSV: {e}")
            self.documents = []

        # 2. Embeddings (Generate vectors using a local model)
        # model="llama3.2" It must match the model name in your ollama run.
        print("Initializing Local Embeddings...")
        self.embeddings = OllamaEmbeddings(model="llama3.2")

        # 3. Vector DB
        if os.path.exists(persist_dir):
            print(f"Loading existing vector store from {persist_dir}...")
            self.vector_db = Chroma(persist_directory=persist_dir, embedding_function=self.embeddings)
        else:
            print("Creating new vector store (Local)...")
            self.vector_db = Chroma.from_documents(
                documents=self.documents,
                embedding=self.embeddings,
                persist_directory=persist_dir
            )

        # 4. LLM (Use Local Llama 3.2)
        print("Initializing Local LLM...")
        self.llm = ChatOllama(model="llama3.2", temperature=0)

    def query(self, user_question: str, k: int = 3) -> dict:
        if not self.documents:
            return {"answer": "No documents loaded.", "source_docs": []}

        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_db.as_retriever(search_kwargs={"k": k}),
            return_source_documents=True
        )

        print("Thinking (Local LLM takes a bit longer)...")
        response = qa_chain.invoke({"query": user_question})

        return {
            "answer": response['result'],
            "source_docs": [doc.metadata.get('source', 'Unknown') for doc in response['source_documents']]
        }

