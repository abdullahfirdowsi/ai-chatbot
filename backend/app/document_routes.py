import os
import tempfile
from typing import List, Dict, Any
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from langchain.schema import Document

from app.rag_service import get_rag_service
from app.vector_store import DocumentLoaderFactory
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/documents", tags=["documents"])

# Allowed file extensions
ALLOWED_EXTENSIONS = {'.pdf', '.txt', '.docx', '.md'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(None),
    description: str = Form(None)
):
    """Upload and process a document for the knowledge base."""
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400, 
                detail=f"File type {file_extension} not supported. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Check file size
        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large. Maximum size is 10MB")
        
        # Save temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        try:
            # Process document
            documents = await process_uploaded_file(
                tmp_file_path, 
                file_extension[1:],  # Remove the dot
                file.filename,
                title or file.filename,
                description
            )
            
            # Add to knowledge base
            rag_service = get_rag_service()
            result = rag_service.add_documents_to_knowledge_base(documents)
            
            return {
                "success": True,
                "message": f"Successfully processed and indexed {len(documents)} document chunks",
                "filename": file.filename,
                "chunks_created": len(documents),
                "document_ids": result.get("document_ids", [])
            }
            
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")

async def process_uploaded_file(
    file_path: str, 
    file_type: str, 
    original_filename: str,
    title: str = None,
    description: str = None
) -> List[Document]:
    """Process an uploaded file and return Document objects."""
    try:
        # Load document using appropriate loader
        loader = DocumentLoaderFactory.get_loader(file_path, file_type)
        documents = loader.load()
        
        # Add metadata to all documents
        for doc in documents:
            doc.metadata.update({
                "source": original_filename,
                "title": title or original_filename,
                "description": description or "",
                "file_type": file_type,
                "upload_date": str(Path(file_path).stat().st_mtime)
            })
        
        logger.info(f"Processed {len(documents)} documents from {original_filename}")
        return documents
        
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")
        raise

@router.get("/search")
async def search_documents(query: str, limit: int = 10):
    """Search documents in the knowledge base."""
    try:
        if not query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        rag_service = get_rag_service()
        results = rag_service.search_knowledge_base(query, k=limit)
        
        return {
            "success": True,
            "query": query,
            "results": results,
            "total_results": len(results)
        }
        
    except Exception as e:
        logger.error(f"Error searching documents: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.get("/stats")
async def get_knowledge_base_stats():
    """Get statistics about the knowledge base."""
    try:
        rag_service = get_rag_service()
        stats = rag_service.get_knowledge_base_stats()
        
        return {
            "success": True,
            "stats": stats
        }
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")

@router.post("/test-query")
async def test_rag_query(query: str = Form(...), use_context: bool = Form(True)):
    """Test RAG functionality with a query."""
    try:
        if not query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        rag_service = get_rag_service()
        
        if use_context:
            result = rag_service.query_with_context(query)
        else:
            # Direct LLM query without context
            result = rag_service._fallback_response(query)
        
        return {
            "success": True,
            "query": query,
            "answer": result["answer"],
            "context_used": result["context_used"],
            "has_context": result["has_context"],
            "source_documents": result["source_documents"]
        }
        
    except Exception as e:
        logger.error(f"Error in test query: {e}")
        raise HTTPException(status_code=500, detail=f"Test query failed: {str(e)}")

@router.delete("/clear")
async def clear_knowledge_base():
    """Clear the entire knowledge base (use with caution)."""
    try:
        # Note: FAISS doesn't support selective deletion
        # This would require recreating the vector store
        logger.warning("Knowledge base clear requested - not implemented for FAISS")
        
        return {
            "success": False,
            "message": "Knowledge base clearing not supported with FAISS. Consider rebuilding the index."
        }
        
    except Exception as e:
        logger.error(f"Error clearing knowledge base: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to clear knowledge base: {str(e)}")

@router.get("/supported-formats")
async def get_supported_formats():
    """Get list of supported document formats."""
    return {
        "supported_formats": [
            {
                "extension": ".pdf",
                "description": "PDF documents",
                "mime_types": ["application/pdf"]
            },
            {
                "extension": ".txt",
                "description": "Plain text files",
                "mime_types": ["text/plain"]
            },
            {
                "extension": ".docx",
                "description": "Microsoft Word documents",
                "mime_types": ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
            },
            {
                "extension": ".md",
                "description": "Markdown files",
                "mime_types": ["text/markdown"]
            }
        ],
        "max_file_size": f"{MAX_FILE_SIZE // (1024 * 1024)}MB"
    }
