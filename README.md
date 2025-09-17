# 🤖 AI Chatbot with RAG

A full-stack AI chatbot application with **Retrieval-Augmented Generation (RAG)** capabilities, built with Angular, FastAPI, LangChain, and FAISS vector database.

## ✨ Key Features

- **🧠 RAG-Powered Responses**: Upload documents and get contextual answers from your knowledge base
- **🔍 Semantic Search**: Advanced document search with FAISS vector database
- **📄 Multi-Format Support**: PDF, TXT, DOCX, and Markdown file processing
- **💬 Dual Chat Modes**: Standard AI chat and RAG-enhanced conversations
- **📊 Knowledge Base Management**: Upload, search, and manage documents with analytics
- **🎨 Modern UI**: Beautiful Angular Material interface with responsive design
- **⚡ LangChain Integration**: Professional-grade RAG implementation
- **📈 Real-time Analytics**: Track knowledge base statistics and usage

## Project Structure

```
ai-chatbot/
├── frontend/                 # Angular frontend with Material UI
│   ├── src/app/
│   │   ├── chat/            # Main chat component
│   │   ├── documents/       # 📚 NEW: Document management component
│   │   ├── app.component.*  # Root application component
│   │   └── app.config.ts    # Application configuration
│   ├── package.json         # Dependencies (Angular 20+ & Material)
│   └── angular.json         # Angular build configuration
├── backend/                 # FastAPI backend with RAG
│   ├── app/
│   │   ├── main.py          # FastAPI application entry point
│   │   ├── routes.py        # Chat endpoints (standard + RAG)
│   │   ├── document_routes.py # 📄 NEW: Document management APIs
│   │   ├── rag_service.py   # 🧠 NEW: LangChain RAG implementation
│   │   ├── vector_store.py  # 🔍 NEW: FAISS vector database service
│   │   ├── database.py      # MongoDB connection & models
│   │   └── models.py        # Pydantic request/response models
│   ├── requirements.txt     # All dependencies (LangChain, FAISS, etc.)
│   ├── .env                 # Environment configuration
│   ├── start_server.py      # Development server launcher
│   └── data/               # 💾 Vector store & uploaded documents
│       └── vector_store/    # FAISS index files (auto-created)
└── README.md               # This comprehensive guide
```

## 🛠️ Technology Stack

### **Backend**
- **FastAPI** - High-performance async web framework
- **LangChain** - RAG framework and document processing
- **FAISS** - Facebook's vector similarity search
- **Groq** - Fast LLM inference API
- **MongoDB** - Document database for chat history
- **HuggingFace Transformers** - Embedding models

### **Frontend** 
- **Angular 20+** - Modern TypeScript framework
- **Angular Material** - Beautiful UI components
- **RxJS** - Reactive programming
- **TypeScript** - Type-safe development

### **AI & RAG Components**
- **Sentence Transformers** - Text embeddings (all-MiniLM-L6-v2)
- **Document Loaders** - PDF, DOCX, TXT, Markdown support
- **Text Splitters** - Intelligent document chunking
- **Vector Store** - Persistent FAISS index with metadata

## ✅ Prerequisites

- **Node.js** v18+ (for Angular frontend)
- **Python** 3.8+ (for FastAPI backend) 
- **MongoDB** (local instance or MongoDB Atlas)
- **Angular CLI** (`npm install -g @angular/cli`)
- **Groq API Key** (sign up at https://groq.com)

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create and configure environment variables:
   ```bash
   # Create .env file in backend directory
   echo "AI_CHATBOT_API_KEY=your_groq_api_key_here" > .env
   echo "AI_CHATBOT_MODEL_NAME=gemma2-9b-it" >> .env
   echo "MONGO_URI=mongodb://localhost:27017" >> .env
   ```
   
   **Required Environment Variables:**
   - `AI_CHATBOT_API_KEY` - Your Groq API key
   - `AI_CHATBOT_MODEL_NAME` - Model name (default: gemma2-9b-it)
   - `MONGO_URI` - MongoDB connection string

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Running the Application

### Start the Backend Server

1. Navigate to backend directory and activate virtual environment:
   ```bash
   cd backend
   venv\Scripts\activate
   ```

2. Start the FastAPI server:
   ```bash
   python start.py
   ```
   
   Or alternatively:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

   The backend will be available at: http://localhost:8000

### Start the Frontend Application

1. In a new terminal, navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Start the Angular development server:
   ```bash
   ng serve
   ```

   The frontend will be available at: http://localhost:4200

## 📡 API Endpoints

### **Chat Endpoints**
- `POST /chat` - Standard AI chat (without RAG)
- `POST /chat/rag` - 🆕 **RAG-Enhanced Chat** (recommended)
- `DELETE /chat/clear` - Clear conversation history

### **Document Management** 
- `POST /documents/upload` - Upload documents (PDF, TXT, DOCX, MD)
- `GET /documents/search?query=...&limit=10` - Search knowledge base
- `GET /documents/stats` - Get knowledge base statistics  
- `POST /documents/test-query` - Test RAG with custom query
- `GET /documents/supported-formats` - List supported file types

### **System Endpoints**
- `GET /` - API information and available endpoints
- `GET /health` - Application health check

### **Example Usage**

#### Standard Chat
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "What is machine learning?"}'
```

#### RAG-Enhanced Chat
```bash
curl -X POST "http://localhost:8000/chat/rag" \
     -H "Content-Type: application/json" \
     -d '{"message": "Explain the concepts from the uploaded document"}'
```

#### Upload Document
```bash
curl -X POST "http://localhost:8000/documents/upload" \
     -F "file=@your-document.pdf" \
     -F "title=Course Material"
```

## 🧪 Testing & Usage Guide

### **1. Test the Basic Setup**
1. Start both backend and frontend
2. Visit http://localhost:4200
3. Try the standard chat functionality
4. Check the API at http://localhost:8000

### **2. Test RAG Functionality**
1. Navigate to the "📚 Documents" tab
2. Upload a PDF, TXT, DOCX, or Markdown file
3. Wait for processing completion
4. Use the "Test RAG" tab to ask questions about your document
5. Check that responses reference your uploaded content

### **3. Verify Knowledge Base**
1. Go to the "📈 Statistics" tab
2. Check document count and embeddings
3. Use the "🔍 Search" tab to find specific content
4. Verify search results show relevant document chunks

## 📖 How RAG Works

1. **Document Upload**: Users upload documents (PDF, TXT, DOCX, MD)
2. **Text Processing**: Documents are split into chunks using LangChain
3. **Embedding Generation**: Text chunks converted to vectors using sentence-transformers
4. **Vector Storage**: Embeddings stored in FAISS database with metadata
5. **Query Processing**: User questions converted to embeddings
6. **Similarity Search**: FAISS finds most relevant document chunks
7. **Context Injection**: Relevant chunks added to LLM prompt
8. **Enhanced Response**: AI generates contextual answers with source citations

## 🛠️ Development Notes

### **RAG Configuration**
- **Chunk Size**: 1000 characters with 200 character overlap
- **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2 (384 dimensions)
- **Vector Database**: FAISS with persistent storage
- **Similarity Threshold**: 0.7 (configurable)
- **Context Window**: Top 5 relevant chunks per query

### **File Processing**
- **Supported Formats**: PDF, TXT, DOCX, Markdown
- **Max File Size**: 10MB per upload
- **Processing**: Automatic chunking and indexing
- **Metadata**: Source tracking and timestamps

### **Performance Optimizations**
- **Lazy Loading**: Vector store loads on demand
- **Caching**: Embedding models cached in memory
- **Async Processing**: Non-blocking document processing
- **Error Handling**: Graceful fallbacks to standard chat

## 🚀 Production Deployment

### **Backend Deployment**
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### **Frontend Build**
```bash
ng build --configuration production
# Serve dist/ folder with nginx or similar
```

### **Environment Variables**
```env
# Production .env
AI_CHATBOT_API_KEY=your_production_groq_key
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/
ENVIRONMENT=production
CORS_ORIGINS=["https://yourdomain.com"]
```

## 🔧 Troubleshooting

### **Common Issues**

**Backend won't start:**
- Check Python version (3.8+)
- Verify virtual environment is activated
- Ensure all requirements installed: `pip install -r requirements.txt`
- Check .env file exists with required variables

**Frontend build errors:**
- Update Node.js to v18+
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`

**RAG not working:**
- Verify documents uploaded successfully 
- Check FAISS index created in `backend/data/vector_store/`
- Test with `/documents/test-query` endpoint
- Check Groq API key is valid

**MongoDB connection issues:**
- Ensure MongoDB is running locally or connection string is correct
- Check firewall settings for MongoDB port (27017)
- Verify network access for MongoDB Atlas

## 🚀 Future Enhancements

### **Immediate Roadmap**
- [ ] **Multi-language Support** - Translate documents and responses
- [ ] **Advanced Analytics** - Usage metrics and performance tracking 
- [ ] **User Authentication** - Multi-user knowledge bases
- [ ] **Vector Database Migration** - ChromaDB or Pinecone integration
- [ ] **Advanced RAG** - HyDE, multi-query, and reranking

### **Long-term Vision**
- [ ] **Real-time Collaboration** - Shared knowledge bases
- [ ] **API Integrations** - Google Drive, Notion, Confluence
- [ ] **Advanced AI** - GPT-4, Claude-3, custom model fine-tuning
- [ ] **Mobile Apps** - iOS and Android applications
- [ ] **Enterprise Features** - SSO, RBAC, audit logs

---

## 🎆 **Ready to Get Started?**

1. Clone the repository
2. Follow the setup instructions above
3. Upload your first document
4. Experience the power of RAG! 🧠✨

For questions or contributions, feel free to open an issue or submit a pull request!
