# Eidolon - AI-Powered Educational Video Generator

Eidolon is an intelligent video generation application that transforms educational prompts and resources into engaging animated videos using Manim. The system leverages LLM technology and RAG (Retrieval Augmented Generation) to create contextually accurate educational content.

## Overview

The application consists of two main components:

1. **Frontend**: Next.js-based web interface for user interaction
2. **Backend**: (To be implemented) Python backend for LLM integration, RAG, and Manim video generation

## System Architecture

```
┌─────────────────┐
│   User Input    │
│  (Prompt +      │
│   Resources)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Frontend      │
│   (Next.js)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Backend API   │
│   - LLM         │
│   - RAG System  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Manim Generator │
│ (Docker)        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Video Output   │
│  + RAG Chat     │
└─────────────────┘
```

## Features

### Current (Frontend)
- ✅ Modern, responsive UI with Tailwind CSS
- ✅ Drag-and-drop file upload for educational resources
- ✅ Real-time script display
- ✅ Video player with download functionality
- ✅ Interactive chat interface for Q&A
- ✅ Visual progress tracking through workflow stages
- ✅ Mock API implementations for development

### To Be Implemented (Backend)
- ⏳ LLM integration for script generation
- ⏳ RAG system for resource processing
- ⏳ Manim code generation
- ⏳ Docker container for Manim execution
- ⏳ Video file storage and serving
- ⏳ Session management
- ⏳ Contextual Q&A system

## Project Structure

```
Eidolon/
├── frontend/              # Next.js frontend application
│   ├── app/              # Next.js app directory
│   │   ├── api/         # API route handlers
│   │   ├── page.tsx     # Main application page
│   │   └── layout.tsx   # Root layout
│   ├── components/       # React components
│   ├── types/           # TypeScript type definitions
│   └── public/          # Static assets
│
├── manim/               # Manim-related files (to be developed)
│   └── (Backend video generation code)
│
└── README.md           # This file
```

## Getting Started

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file:
```bash
cp .env.example .env.local
```

4. Start development server:
```bash
npm run dev
```

5. Open [http://localhost:3000](http://localhost:3000)

### Backend Setup (To Be Implemented)

The backend will require:
- Python 3.9+
- FastAPI or Flask
- LangChain for LLM integration
- Vector database (e.g., ChromaDB, Pinecone)
- Docker for Manim execution
- File storage solution

## Workflow

1. **User Input**: User provides a prompt describing the desired video and optionally uploads educational resources (PDFs, textbooks, etc.)

2. **RAG Processing**: Backend processes uploaded resources using embeddings and stores them in a vector database

3. **Script Generation**: LLM generates a video script based on the prompt and relevant context from uploaded resources

4. **Manim Code Generation**: LLM converts the script into Manim Python code for animations

5. **Video Rendering**: Manim code is executed in a Docker container to generate the video

6. **Interactive Q&A**: Users can ask questions about the video content, script, or uploaded resources via RAG-powered chat

## Technology Stack

### Frontend
- **Framework**: Next.js 16 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4
- **Icons**: Lucide React
- **File Upload**: react-dropzone

### Backend (Planned)
- **Framework**: FastAPI / Flask
- **LLM**: OpenAI GPT-4, Anthropic Claude, or similar
- **RAG**: LangChain + Vector Database
- **Animation**: Manim Community Edition
- **Containerization**: Docker
- **Storage**: S3 or similar

## API Specification

### Generate Script
```
POST /api/generate-script
Content-Type: multipart/form-data

Body:
- prompt: string
- resources: File[]

Response: {
  sessionId: string,
  script: string,
  status: 'success' | 'error'
}
```

### Check Video Status
```
GET /api/video-status/:sessionId

Response: {
  status: 'generating' | 'completed' | 'error',
  videoUrl?: string,
  progress?: number,
  message?: string
}
```

### Chat (RAG)
```
POST /api/chat
Content-Type: application/json

Body: {
  sessionId: string,
  message: string
}

Response: {
  response: string,
  sessionId: string,
  timestamp: string
}
```

## Development Roadmap

- [x] Frontend UI/UX design and implementation
- [x] Mock API endpoints for development
- [ ] Backend API server setup
- [ ] LLM integration for script generation
- [ ] RAG system implementation
- [ ] Manim code generator
- [ ] Docker container for Manim
- [ ] Video storage and serving
- [ ] Production deployment
- [ ] User authentication
- [ ] Usage analytics

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Contact

For questions or support, please open an issue on the GitHub repository.
