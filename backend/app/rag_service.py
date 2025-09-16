import os
from typing import List, Dict, Any, Optional
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.schema import Document
from dotenv import load_dotenv

from app.vector_store import get_vector_store
import logging

load_dotenv()
logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.vector_store = get_vector_store()
        
        # Initialize Groq LLM
        self.llm = ChatGroq(
            groq_api_key=os.getenv("AI_CHATBOT_API_KEY"),
            model_name=os.getenv("AI_CHATBOT_MODEL_NAME", "gemma2-9b-it"),
            temperature=0.7,
            max_tokens=500
        )
        
        # Create custom prompt template
        self.prompt_template = self._create_prompt_template()
        
        # Initialize RAG chain
        self.rag_chain = self._create_rag_chain()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create a custom prompt template for the RAG chain."""
        template = """
You are AI Chatbot, an intelligent AI tutor. Use the following context from the knowledge base to help answer the student's question. 

If the context provides relevant information, incorporate it into your response naturally. If the context doesn't contain relevant information for the question, respond based on your general knowledge but mention that you're drawing from general knowledge rather than the knowledge base.

Context from Knowledge Base:
{context}

Previous Conversation:
{chat_history}

Student's Question: {question}

Guidelines:
- Be encouraging and supportive
- Use clear explanations with examples when helpful
- If using information from the context, cite it naturally (e.g., "According to the document...")
- If the context doesn't help, clearly state you're using general knowledge
- Keep responses educational and engaging
- Ask follow-up questions to ensure understanding

Answer:"""

        return PromptTemplate(
            template=template,
            input_variables=["context", "chat_history", "question"]
        )
    
    def _create_rag_chain(self) -> RetrievalQA:
        """Create the RAG chain with retriever and LLM."""
        retriever = self.vector_store.get_retriever(
            search_kwargs={"k": 5}
        )
        
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": self.prompt_template},
            return_source_documents=True
        )
    
    def query_with_context(
        self, 
        question: str, 
        chat_history: str = "", 
        k: int = 5
    ) -> Dict[str, Any]:
        """Query the RAG system with context-aware retrieval."""
        try:
            # First, get relevant documents
            relevant_docs = self.vector_store.similarity_search(question, k=k)
            
            if not relevant_docs:
                # Fall back to general knowledge response
                return self._fallback_response(question, chat_history)
            
            # Prepare context from retrieved documents
            context = self._format_context(relevant_docs)
            
            # Query the RAG chain
            result = self.rag_chain({
                "query": question,
                "context": context,
                "chat_history": chat_history
            })
            
            return {
                "answer": result["result"],
                "source_documents": [
                    {
                        "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                        "metadata": doc.metadata,
                        "source": doc.metadata.get("source", "Unknown")
                    }
                    for doc in result.get("source_documents", [])
                ],
                "has_context": True,
                "context_used": len(relevant_docs) > 0
            }
            
        except Exception as e:
            logger.error(f"Error in RAG query: {e}")
            return self._fallback_response(question, chat_history)
    
    def _format_context(self, documents: List[Document]) -> str:
        """Format retrieved documents into context string."""
        if not documents:
            return "No relevant context found in the knowledge base."
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            source = doc.metadata.get("source", "Unknown source")
            content = doc.page_content.strip()
            context_parts.append(f"[Document {i} - {source}]:\n{content}\n")
        
        return "\n".join(context_parts)
    
    def _fallback_response(self, question: str, chat_history: str = "") -> Dict[str, Any]:
        """Generate response using only the LLM when no context is available."""
        try:
            fallback_prompt = f"""
You are AI Chatbot, an intelligent AI tutor. A student has asked you a question, but there's no relevant information in the current knowledge base.

Previous Conversation:
{chat_history}

Student's Question: {question}

Please provide a helpful response based on your general knowledge. Mention that you're drawing from general knowledge since the specific information isn't in the current knowledge base. Be encouraging and educational.

Answer:"""
            
            response = self.llm.invoke(fallback_prompt)
            
            return {
                "answer": response.content,
                "source_documents": [],
                "has_context": False,
                "context_used": False
            }
            
        except Exception as e:
            logger.error(f"Error in fallback response: {e}")
            return {
                "answer": "I apologize, but I'm having trouble processing your question right now. Please try again.",
                "source_documents": [],
                "has_context": False,
                "context_used": False
            }
    
    def add_documents_to_knowledge_base(self, documents: List[Document]) -> Dict[str, Any]:
        """Add documents to the vector store."""
        try:
            ids = self.vector_store.add_documents(documents)
            
            # Recreate the RAG chain to include new documents
            self.rag_chain = self._create_rag_chain()
            
            return {
                "success": True,
                "message": f"Successfully added {len(documents)} documents to knowledge base",
                "document_ids": ids
            }
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            return {
                "success": False,
                "message": f"Failed to add documents: {str(e)}"
            }
    
    def search_knowledge_base(self, query: str, k: int = 10) -> List[Dict[str, Any]]:
        """Search the knowledge base directly."""
        try:
            docs = self.vector_store.similarity_search(query, k=k)
            return [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "source": doc.metadata.get("source", "Unknown")
                }
                for doc in docs
            ]
        except Exception as e:
            logger.error(f"Error searching knowledge base: {e}")
            return []
    
    def get_knowledge_base_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base."""
        return self.vector_store.get_stats()

# Global RAG service instance
rag_service = None

def get_rag_service() -> RAGService:
    """Get the global RAG service instance."""
    global rag_service
    if rag_service is None:
        rag_service = RAGService()
    return rag_service
