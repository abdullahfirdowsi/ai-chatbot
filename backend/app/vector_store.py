import os
import pickle
from typing import List, Optional, Dict, Any
from pathlib import Path

import faiss
import numpy as np
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.document_loaders import (
    PyPDFLoader, 
    TextLoader, 
    Docx2txtLoader,
    UnstructuredMarkdownLoader
)

import logging

logger = logging.getLogger(__name__)

class VectorStoreManager:
    def __init__(self, persist_directory: str = "data/vector_store"):
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize embeddings model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Load existing vector store or create new one
        self.vector_store = self._load_or_create_vector_store()
        
    def _load_or_create_vector_store(self) -> FAISS:
        """Load existing FAISS vector store or create a new one."""
        vector_store_path = self.persist_directory / "faiss_index"
        
        if vector_store_path.exists():
            try:
                logger.info("Loading existing FAISS vector store...")
                return FAISS.load_local(
                    str(vector_store_path), 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
            except Exception as e:
                logger.warning(f"Failed to load existing vector store: {e}")
                logger.info("Creating new vector store...")
        
        # Create new empty vector store
        sample_doc = Document(page_content="", metadata={})
        vector_store = FAISS.from_documents([sample_doc], self.embeddings)
        return vector_store
    
    def add_documents(self, documents: List[Document]) -> List[str]:
        """Add documents to the vector store."""
        try:
            # Split documents into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            # Add unique IDs to chunks
            for i, chunk in enumerate(chunks):
                chunk.metadata.update({
                    "chunk_id": f"{chunk.metadata.get('source', 'unknown')}_{i}",
                    "chunk_index": i
                })
            
            # Add to vector store
            ids = self.vector_store.add_documents(chunks)
            
            # Save the updated vector store
            self._save_vector_store()
            
            logger.info(f"Added {len(chunks)} document chunks to vector store")
            return ids
            
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")
            raise
    
    def similarity_search(self, query: str, k: int = 5, score_threshold: float = 0.7) -> List[Document]:
        """Search for similar documents."""
        try:
            # Perform similarity search with scores
            docs_with_scores = self.vector_store.similarity_search_with_score(query, k=k)
            
            # Filter by score threshold
            filtered_docs = [
                doc for doc, score in docs_with_scores 
                if score >= score_threshold
            ]
            
            logger.info(f"Found {len(filtered_docs)} relevant documents for query: {query[:50]}...")
            return filtered_docs
            
        except Exception as e:
            logger.error(f"Error during similarity search: {e}")
            return []
    
    def get_retriever(self, search_kwargs: Dict[str, Any] = None):
        """Get a LangChain retriever interface."""
        if search_kwargs is None:
            search_kwargs = {"k": 5}
        
        return self.vector_store.as_retriever(search_kwargs=search_kwargs)
    
    def delete_documents(self, document_ids: List[str]) -> bool:
        """Delete documents by IDs (Note: FAISS doesn't support direct deletion)."""
        logger.warning("FAISS doesn't support direct document deletion. Consider rebuilding the index.")
        return False
    
    def _save_vector_store(self):
        """Save the vector store to disk."""
        try:
            vector_store_path = self.persist_directory / "faiss_index"
            self.vector_store.save_local(str(vector_store_path))
            logger.info("Vector store saved successfully")
        except Exception as e:
            logger.error(f"Error saving vector store: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get vector store statistics."""
        try:
            total_docs = self.vector_store.index.ntotal if hasattr(self.vector_store, 'index') else 0
            return {
                "total_documents": total_docs,
                "embedding_dimension": self.embeddings.client.get_sentence_embedding_dimension() if hasattr(self.embeddings, 'client') else 384,
                "persist_directory": str(self.persist_directory)
            }
        except Exception as e:
            logger.error(f"Error getting vector store stats: {e}")
            return {"error": str(e)}

# Document loader factory
class DocumentLoaderFactory:
    @staticmethod
    def get_loader(file_path: str, file_type: str):
        """Get appropriate document loader based on file type."""
        loaders = {
            'pdf': PyPDFLoader,
            'txt': TextLoader,
            'docx': Docx2txtLoader,
            'md': UnstructuredMarkdownLoader,
        }
        
        loader_class = loaders.get(file_type.lower())
        if not loader_class:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        return loader_class(file_path)

# Global vector store instance
vector_store_manager = None

def get_vector_store() -> VectorStoreManager:
    """Get the global vector store manager instance."""
    global vector_store_manager
    if vector_store_manager is None:
        vector_store_manager = VectorStoreManager()
    return vector_store_manager
