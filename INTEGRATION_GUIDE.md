# Eidolon Frontend-Backend Integration Guide

## Overview

This guide explains how to integrate the Next.js frontend (`frontend-ui/`) with the Python backend (`backend/`) that generates Manim videos with AI voiceover.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USER BROWSER                                │
│                     (Next.js Frontend - Port 3000)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │   Landing    │→│   Generator   │→│   Results     │              │
│  │   Login/Reg  │  │   (Prompt)    │  │   (Video+Q&A) │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
└────────────────────────────────│───────────────────────────────────┘
                                  │ HTTP REST API
                                  ↓
┌─────────────────────────────────────────────────────────────────────┐
│                     PYTHON BACKEND API                               │
│                     (FastAPI - Port 8000)                            │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  POST /api/generate-video  (Upload prompt + files)           │  │
│  │  GET  /api/queue-status/:id  (Poll for progress)             │  │
│  │  GET  /api/video/:id  (Download video)                        │  │
│  │  POST /api/chat  (RAG Q&A)                                     │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                  │                                   │
│                                  ↓                                   │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │              VIDEO GENERATION PIPELINE                         │ │
│  │  1. Gemini AI → Generate Manim Code                           │ │
│  │  2. Manim CLI → Render Animation                              │ │
│  │  3. ElevenLabs → Generate Voiceover                           │ │
│  │  4. FFmpeg → Merge Audio + Video                              │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

## Setup Instructions

### 1. Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Set environment variables
# Add to .env file or export:
export GEMINI_API_KEY=your_gemini_key_here
export ELEVENLABS_API_KEY=your_elevenlabs_key_here  # Optional

# Start backend server
python api_server.py

# Server will run on http://localhost:8000
```

### 2. Frontend Setup

```bash
cd frontend-ui

# Install Node dependencies (if not already done)
npm install

# Update API base URL in code (see below)

# Start development server
npm run dev

# Frontend will run on http://localhost:3000
```

### 3. Connect Frontend to Backend

Update the frontend to call the real API instead of mocks. Here's what to modify:

#### A. Create API Client (`frontend-ui/lib/api.ts`)

```typescript
const API_BASE = 'http://localhost:8000';

export async function generateVideo(prompt: string, files: File[]) {
  const formData = new FormData();
  formData.append('prompt', prompt);
  files.forEach(file => formData.append('files', file));
  
  const response = await fetch(`${API_BASE}/api/generate-video`, {
    method: 'POST',
    body: formData,
  });
  
  return response.json();
}

export async function getQueueStatus(videoId: string) {
  const response = await fetch(`${API_BASE}/api/queue-status/${videoId}`);
  return response.json();
}

export async function getVideoUrl(videoId: string) {
  return `${API_BASE}/api/video/${videoId}`;
}

export async function sendChatMessage(videoId: string, message: string, history: any[]) {
  const response = await fetch(`${API_BASE}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ video_id: videoId, message, history }),
  });
  
  return response.json();
}
```

#### B. Update Generator View (in `app/page.tsx`)

Replace this:
```typescript
const handleGenerate = () => {
  if (prompt.trim()) {
    addToQueue(prompt);
    setPrompt('');
    setFiles([]);
    alert('Added to render queue!');
  }
};
```

With:
```typescript
const handleGenerate = async () => {
  if (prompt.trim()) {
    try {
      const result = await generateVideo(prompt, files);
      addToQueue(prompt, result.video_id);  // Store video_id
      setPrompt('');
      setFiles([]);
      alert('Video generation started! Check the queue.');
    } catch (error) {
      alert('Error starting video generation');
    }
  }
};
```

#### C. Add Queue Polling

In the Navbar queue modal, poll for status updates:

```typescript
useEffect(() => {
  const interval = setInterval(async () => {
    for (const item of queue) {
      if (item.status !== 'complete' && item.status !== 'error') {
        try {
          const status = await getQueueStatus(item.videoId);
          updateQueueItemStatus(item.id, status.status, status.progress);
        } catch (error) {
          console.error('Failed to fetch status', error);
        }
      }
    }
  }, 3000);  // Poll every 3 seconds
  
  return () => clearInterval(interval);
}, [queue]);
```

#### D. Update Results View

Replace the hardcoded SpongeBob image with:

```typescript
const [videoUrl, setVideoUrl] = useState('');
const videoId = useStore(state => state.currentVideoId);  // Get from store

useEffect(() => {
  if (videoId) {
    setVideoUrl(getVideoUrl(videoId));
  }
}, [videoId]);

// In JSX:
<video src={videoUrl} controls className="w-full h-full" />
```

#### E. Connect Chat

Replace the TODO in `handleSend`:

```typescript
const handleSend = async () => {
  if (!input.trim()) return;
  
  const userMessage = { role: 'user' as const, content: input };
  setMessages(prev => [...prev, userMessage]);
  setInput('');
  
  try {
    const response = await sendChatMessage(videoId, input, messages);
    const assistantMessage = {
      role: 'assistant' as const,
      content: response.response
    };
    setMessages(prev => [...prev, assistantMessage]);
  } catch (error) {
    console.error('Chat error:', error);
  }
};
```

### 4. Update Store (frontend-ui/lib/store.ts)

Add video_id tracking to queue items:

```typescript
type QueueItem = {
  id: number;
  prompt: string;
  videoId?: string;  // Add this
  status: 'queued' | 'rendering' | 'complete' | 'error';
  progress?: number;  // Add this
  createdAt: number;
};

addToQueue: (prompt: string, videoId?: string) =>
  set((state) => ({
    queue: [
      ...state.queue,
      {
        id: Date.now(),
        prompt,
        videoId,
        status: 'queued',
        progress: 0,
        createdAt: Date.now(),
      },
    ],
  })),

// Add method to track current video
currentVideoId: null,
setCurrentVideoId: (id: string) => set({ currentVideoId: id }),
```

## API Endpoints Reference

### POST `/api/generate-video`
**Request:**
- `prompt` (form field): Text description of video
- `files` (multipart files): Optional PDF/TXT resources

**Response:**
```json
{
  "video_id": "uuid-string",
  "status": "queued",
  "message": "Video generation started"
}
```

### GET `/api/queue-status/:video_id`
**Response:**
```json
{
  "status": "rendering",
  "progress": 45,
  "message": "Rendering Manim animation...",
  "script": "from manim import *\n...",
  "video_url": null
}
```

Status values: `queued`, `generating_code`, `rendering`, `adding_voiceover`, `complete`, `error`

### GET `/api/video/:video_id`
**Response:** Video file (MP4)

### POST `/api/chat`
**Request:**
```json
{
  "video_id": "uuid-string",
  "message": "What is shown in the video?",
  "history": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

**Response:**
```json
{
  "response": "The video explains...",
  "video_id": "uuid-string"
}
```

## Testing the Integration

### 1. Test Backend Standalone

```bash
# In backend directory
python api_server.py

# Test with curl:
curl http://localhost:8000/

# Expected: {"status":"Eidolon API running","version":"1.0.0"}
```

### 2. Test Video Generation

```bash
curl -X POST http://localhost:8000/api/generate-video \
  -F "prompt=Explain the Pythagorean theorem" \
  -F "files=@test.pdf"
  
# Returns: {"video_id": "...", "status": "queued"}
```

### 3. Test Queue Status

```bash
curl http://localhost:8000/api/queue-status/VIDEO_ID_HERE
```

### 4. Test Full Workflow

1. Start backend: `python api_server.py`
2. Start frontend: `npm run dev`
3. Open http://localhost:3000
4. Login/Register
5. Enter prompt: "Explain integration by parts"
6. Click "Add to Queue"
7. Open queue modal (top right icon)
8. Watch progress update
9. Click completed video to view
10. Ask questions in Q&A chat

## Workflow Example

### User Flow:
1. **Landing** → Click "Start Creating"
2. **Login** → Enter email/password
3. **Generator** → Enter prompt + optional files → "Add to Queue"
4. **Queue Modal** → Watch progress (queued → generating_code → rendering → adding_voiceover → complete)
5. **Results** → Video plays with voiceover → Chat about content

### Backend Processing:
1. Receive prompt + files
2. Generate Manim code with Gemini AI
3. Save script to `generated_scripts/`
4. Render video with `manim` CLI
5. Generate voiceover with ElevenLabs
6. Merge audio + video with ffmpeg
7. Save final video to `outputs/`
8. Mark as complete in queue

## Troubleshooting

### Backend Issues

**"GEMINI_API_KEY not set"**
- Add API key to environment or `.env` file

**"Manim render failed"**
- Check generated code in `generated_scripts/`
- Verify Manim is installed: `manim --version`
- Check for syntax errors in generated code

**"Voiceover failed"**
- System will fall back to video without voiceover
- Check ElevenLabs API key and quota
- Verify `ffmpeg` is installed

### Frontend Issues

**"Failed to fetch"**
- Verify backend is running on port 8000
- Check CORS configuration in `api_server.py`
- Open browser console for errors

**Queue not updating**
- Check polling interval is running
- Verify video_id is being stored correctly
- Test `/api/queue-status/:id` endpoint directly

### Network Issues

**Cross-Origin Errors**
- Frontend must run on http://localhost:3000
- Backend CORS allows localhost:3000
- Don't use 127.0.0.1 mix with localhost

## Production Deployment

For production, you'll need:

1. **Database** (Supabase/PostgreSQL) instead of in-memory queue
2. **File Storage** (S3/Cloudflare R2) for videos
3. **Queue System** (Redis/Celery) for background jobs
4. **CDN** for video delivery
5. **Environment variables** properly configured
6. **HTTPS** for both frontend and backend
7. **Authentication** (JWT tokens)

## File Structure After Integration

```
Eidolon/
├── backend/
│   ├── api_server.py           # FastAPI server
│   ├── requirements.txt         # Python deps
│   ├── uploads/                 # User uploaded files
│   ├── generated_scripts/       # Generated Manim code
│   └── outputs/                 # Final videos
├── frontend-ui/
│   ├── app/
│   │   └── page.tsx             # Updated with API calls
│   ├── lib/
│   │   ├── api.ts               # NEW: API client
│   │   └── store.ts             # Updated with video_id
│   └── package.json
├── manim/
│   ├── video_improver_mobject.py
│   ├── voiceover_generator.py
│   └── ... (all your existing Manim tools)
└── .env                         # API keys
```

## Next Steps

1. Install backend dependencies
2. Create `frontend-ui/lib/api.ts` with the API client code above
3. Update frontend components to use real API calls
4. Test with a simple prompt like "Explain Pythagorean theorem"
5. Verify video generation, voiceover, and Q&A all work
6. Add error handling and loading states in UI
7. Consider implementing persistent storage (database)

Your Manim video generation system is now fully integrated with a professional web interface! 🎉
