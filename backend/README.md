# AI Chatbot Backend

A modern, intelligent AI-powered chatbot backend built with FastAPI and powered by Groq's API.

## Features

- **Modern FastAPI Framework**: High-performance async API framework
- **AI-Powered Conversations**: Intelligent responses using Groq's Gemma2-9b-it model
- **Conversation Memory**: Maintains context across chat sessions
- **MongoDB Integration**: Persistent message storage
- **CORS Support**: Full cross-origin request support for frontend integration
- **Health Monitoring**: Built-in health check endpoints
- **Comprehensive Logging**: Detailed logging with AI Chatbot branding

## Environment Variables

The backend uses the following environment variables (configure in `.env`):

```env
# Server Configuration
PORT=8000
VITE_API_URL=http://localhost:8000

# Database
MONGO_URI=your_mongodb_connection_string

# AI Configuration
AI_CHATBOT_API_KEY=your_groq_api_key
AI_CHATBOT_MODEL_NAME=gemma2-9b-it
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   - Copy `.env.example` to `.env` (if available)
   - Update the environment variables with your values

5. **Start the server**
   ```bash
   python start_server.py
   ```

## API Endpoints

### Core Endpoints

- `GET /` - API information and available endpoints
- `GET /health` - Health check status
- `POST /chat` - Send chat message to AI Chatbot
- `DELETE /chat/clear` - Clear conversation history

### Chat Endpoint Usage

```json
POST /chat
{
  "message": "Hello, can you help me learn about Python?"
}

Response:
{
  "reply": "Hi there! I'm AI Chatbot, your friendly AI tutor. I'd love to help you learn about Python! ..."
}
```

## Testing

Run the included test script to verify everything is working:

```bash
python test_ai_chatbot_api.py
```

This will test:
- Health endpoint functionality
- API branding consistency
- Chat functionality
- Conversation management

## Architecture

```
app/
├── main.py          # FastAPI application setup
├── routes.py        # API route definitions
├── models.py        # Pydantic data models
├── schemas.py       # Data validation schemas
└── database.py      # MongoDB connection and setup
```

## AI Chatbot Personality

The AI Chatbot is designed as an intelligent tutor with:

- **Encouraging and supportive** personality
- **Patient and understanding** approach
- **Clear explanations** tailored to student level
- **Interactive learning** with follow-up questions
- **Examples and analogies** to aid understanding

## Development

### Running in Development Mode

The server runs with auto-reload enabled by default:

```bash
python start_server.py
```

### Logging

All operations are logged with the "AI Chatbot" prefix for easy identification:

```
AI Chatbot - Making API call to Grok for message: Hello...
AI Chatbot - Successfully generated response from Grok API
```

### Database Schema

Messages are stored with the following structure:

```json
{
  "_id": "ObjectId",
  "text": "Message content",
  "sender": "user|bot",
  "timestamp": "ISO datetime"
}
```

## Troubleshooting

### Common Issues

1. **API Key Issues**: Ensure `AI_CHATBOT_API_KEY` is set correctly
2. **MongoDB Connection**: Verify `MONGO_URI` is accessible
3. **Port Conflicts**: Change `PORT` if 8000 is already in use
4. **CORS Errors**: Current config allows all origins for development

### Environment Variable Migration

If upgrading from an older version, update your environment variables:

- `API_KEY` → `AI_CHATBOT_API_KEY`
- `MODEL_NAME` → `AI_CHATBOT_MODEL_NAME`

## Contributing

1. Follow the established code style
2. Maintain the AI Chatbot branding consistency
3. Update tests when adding new features
4. Ensure all logging uses the "AI Chatbot" prefix

## License

This project is part of the AI Chatbot application suite.
