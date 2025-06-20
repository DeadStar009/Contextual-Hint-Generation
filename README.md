# Contextual Hint Generation System

A smart hint generation system that provides contextual hints for programming problems based on the user's progress and understanding.

## Features
- Interactive code editor with real-time hint generation
- Context-aware hints based on:
  - Problem statement
  - Current code status
  - Time spent on problem
  - Progress level
- Multi-stage LLM pipeline for intelligent hint generation
- HuggingFace inference endpoints integration
- LangChain-based modular architecture

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with:
```
HUGGINGFACE_API_KEY=your_api_key_here
```

4. Start the backend:
```bash
cd backend
uvicorn main:app --reload
```

5. Start the frontend:
```bash
cd frontend
npm install
npm run dev
```

## Architecture
- Frontend: React-based code editor with hint display
- Backend: FastAPI server with LangChain-based hint generation pipeline
- Models: HuggingFace inference endpoints for:
  - Hint type classification
  - Hint generation
  - Hint verification 