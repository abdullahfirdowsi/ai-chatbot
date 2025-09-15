# VizTalk AI Tutor Chatbot

A full-stack AI tutor chatbot application built with Angular and FastAPI.

## Project Structure

```
viztalk-ai-tutor-chatbot/
├── frontend/                 # Angular frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── chat/         # Chat component
│   │   │   ├── app.component.* # Main app component
│   │   │   └── app.config.ts # App configuration
│   │   ├── styles.css        # Global styles
│   │   └── main.ts           # Bootstrap file
│   ├── package.json          # Frontend dependencies
│   └── angular.json          # Angular configuration
└── backend/                  # FastAPI backend
    ├── app/
    │   ├── main.py           # FastAPI app entry point
    │   ├── routes.py         # API routes
    │   ├── models.py         # Pydantic models
    │   ├── database.py       # MongoDB connection
    │   └── schemas.py        # Data schemas
    ├── requirements.txt      # Backend dependencies
    ├── .env                  # Environment variables
    └── start.py              # Backend startup script
```

## Features

- **Interactive Chat Interface**: Clean, modern chat UI built with Angular and Angular Material
- **AI Tutor Responses**: Context-aware responses based on educational topics
- **MongoDB Integration**: Persistent message storage
- **Real-time Communication**: HTTP-based chat with proper error handling
- **Responsive Design**: Works on desktop and mobile devices
- **Educational Focus**: Specialized responses for math, science, history, and writing

## Prerequisites

- Node.js (v18 or higher)
- Python 3.8 or higher
- MongoDB (local or cloud instance)
- Angular CLI (`npm install -g @angular/cli`)

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

4. Configure environment variables:
   - The `.env` file is already configured with MongoDB connection
   - Update `MONGO_URI` if needed for your MongoDB instance

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

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /chat` - Send chat message
  ```json
  {
    "message": "Your question here"
  }
  ```

## Testing

### Frontend Tests
```bash
cd frontend
ng test
```

### Backend Tests
The backend includes basic health checks and error handling.

## Features Overview

### Frontend (Angular)
- Modern Angular 18+ with standalone components
- Angular Material for UI components
- Responsive chat interface
- HTTP client integration
- Proper error handling
- TypeScript for type safety

### Backend (FastAPI)
- RESTful API with FastAPI
- MongoDB integration for message persistence
- CORS enabled for frontend communication
- Context-aware AI tutor responses
- Environment-based configuration
- Proper error handling and validation

## Development Notes

- The frontend is configured to connect to `http://localhost:8000/chat`
- CORS is enabled for development (restrict in production)
- MongoDB connection is configured via environment variables
- The chat responses are currently rule-based but can be enhanced with actual AI integration

## Deployment

For production deployment:

1. **Backend**: Use a production WSGI server like Gunicorn
2. **Frontend**: Build for production with `ng build --prod`
3. **Database**: Use a production MongoDB instance
4. **Environment**: Update CORS settings and environment variables

## Troubleshooting

- Ensure MongoDB is running and accessible
- Check that both frontend and backend ports are available
- Verify environment variables are properly set
- Make sure all dependencies are installed

## Future Enhancements

- Integration with actual AI/ML models (OpenAI, Google AI, etc.)
- User authentication and session management
- Chat history and conversation threads
- File upload and document analysis
- Real-time WebSocket communication
- Advanced tutoring features (problem solving, assessments)
