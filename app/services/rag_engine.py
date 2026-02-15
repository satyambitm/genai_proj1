"""
RAG Engine — Retrieval-Augmented Generation with ChromaDB.

Enhances AI analysis by retrieving relevant medical reference information
from a vector store before generating responses.
"""

import os
import glob
from typing import Optional

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document

from app.config import get_settings

settings = get_settings()


class RAGEngine:
    """
    RAG Engine for medical knowledge retrieval and enhanced analysis.

    Uses ChromaDB as the vector store and OpenAI embeddings for
    semantic search over medical reference documents.
    """

    def __init__(self):
        self._vectorstore: Optional[Chroma] = None
        self._embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY,
            model="text-embedding-3-small",
        )
        self._text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n---\n", "\n## ", "\n### ", "\n\n", "\n", " "],
        )

    @property
    def vectorstore(self) -> Chroma:
        """Lazily initialize the vector store."""
        if self._vectorstore is None:
            self._vectorstore = Chroma(
                collection_name=settings.CHROMA_COLLECTION_NAME,
                embedding_function=self._embeddings,
                persist_directory=settings.CHROMA_PERSIST_DIR,
            )
        return self._vectorstore

    def ingest_documents(self, docs_dir: Optional[str] = None) -> int:
        """
        Load and ingest medical reference documents into the vector store.

        Args:
            docs_dir: Directory containing markdown reference documents.
                      Defaults to app/data/medical_references/

        Returns:
            Number of document chunks ingested.
        """
        if docs_dir is None:
            docs_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "data",
                "medical_references",
            )

        # Find all markdown files
        md_files = glob.glob(os.path.join(docs_dir, "*.md"))
        if not md_files:
            return 0

        all_documents = []
        for file_path in md_files:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            filename = os.path.basename(file_path)
            doc = Document(
                page_content=content,
                metadata={"source": filename, "path": file_path},
            )
            all_documents.append(doc)

        # Split into chunks
        chunks = self._text_splitter.split_documents(all_documents)

        # Add to vector store
        self.vectorstore.add_documents(chunks)

        return len(chunks)

    def query(self, query_text: str, k: int = 5) -> list[dict]:
        """
        Query the vector store for relevant medical context.

        Args:
            query_text: The medical query or report text to search for.
            k: Number of results to return.

        Returns:
            List of dicts with 'content' and 'source' keys.
        """
        results = self.vectorstore.similarity_search(query_text, k=k)

        return [
            {
                "content": doc.page_content,
                "source": doc.metadata.get("source", "unknown"),
            }
            for doc in results
        ]

    def enhance_analysis(self, report_text: str, analysis_summary: str) -> str:
        """
        Enhance an AI analysis by adding relevant medical context.

        Args:
            report_text: The original report text.
            analysis_summary: The AI-generated analysis summary.

        Returns:
            Additional context string from the knowledge base.
        """
        # Combine report and analysis for better semantic search
        search_query = f"{analysis_summary}\n\n{report_text[:500]}"

        results = self.query(search_query, k=3)
        if not results:
            return ""

        context_parts = []
        for r in results:
            source = r["source"]
            content = r["content"][:500]  # Limit context length
            context_parts.append(f"[Source: {source}]\n{content}")

        return "\n\n---\n\n".join(context_parts)

    def get_collection_stats(self) -> dict:
        """Get statistics about the vector store collection."""
        try:
            count = self.vectorstore._collection.count()
            return {
                "collection_name": settings.CHROMA_COLLECTION_NAME,
                "document_count": count,
                "persist_directory": settings.CHROMA_PERSIST_DIR,
            }
        except Exception:
            return {
                "collection_name": settings.CHROMA_COLLECTION_NAME,
                "document_count": 0,
                "persist_directory": settings.CHROMA_PERSIST_DIR,
            }


# ── Singleton Instance ─────────────────────────────────────────────────

_rag_engine: Optional[RAGEngine] = None


def get_rag_engine() -> RAGEngine:
    """Get or create the singleton RAG engine instance."""
    global _rag_engine
    if _rag_engine is None:
        _rag_engine = RAGEngine()
    return _rag_engine
