# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Eidolon is an AI-powered educational video generation platform that transforms text prompts and resources into Manim animations with voiceover. The system uses LLMs (Gemini) for script generation, Manim for animation, and ElevenLabs for voice synthesis.

## Architecture

This is a distributed microservices architecture with three main components:

### 1. Frontend (`frontend-ui/`)
Next.js 13 application with App Router providing the user interface.

### 2. Backend API (`backend/` or `queueHandler/`)
Two potential backend implementations:
- **`backend/`**: FastAPI server with direct Gemini integration (simpler, single-process)
- **`queueHandler/`**: FastAPI + Celery + Redis (production-ready, distributed)

### 3. Manim Renderer (`manim/`)
Containerized Manim service that watches for scripts and renders videos. Includes AI-powered iterative improvement system.

## Key System Interactions

```
Frontend (Next.js:3000)
    ↓ HTTP POST /api/generate-video
QueueHandler/Backend (FastAPI:8000)
    ↓ Writes .py script to /shared/scripts/
Manim Container (watcher.py)
    ↓ Renders video → /shared/videos/
    ↓ Backend polls for completion
Frontend polls /api/queue-status/{id}
    ↓ Retrieves video via /api/video/{id}
```

## Common Development Commands

### Full Stack Development

Start all services with Docker Compose:
```powershell
docker-compose up --build
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Redis: localhost:6379

### Frontend Development

```powershell
cd frontend-ui
npm install              # First time only
npm run dev             # Development server at :3000
npm run build           # Production build
npm run lint            # ESLint validation
npm run typecheck       # TypeScript validation
```

**Frontend uses mock APIs by default**. To connect to real backend, ensure `lib/api.ts` points to `http://localhost:8000`.

### Backend Development (queueHandler)

```powershell
cd queueHandler
pip install -r requirements.txt

# Run API server directly (for development)
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

For Celery worker testing:
```powershell
celery -A src.worker worker --loglevel=info
```

### Backend Development (legacy standalone)

```powershell
cd backend
pip install -r requirements.txt

# Set API keys
$env:GEMINI_API_KEY='your-key-here'
$env:ELEVENLABS_API_KEY='your-key-here'  # Optional

python api_server.py    # Runs on :8000
```

### Manim Development

Test Manim rendering locally:
```powershell
cd manim
manim -pql test.py SceneName
```

Run AI-powered iterative improvement:
```powershell
python video_improver.py --script test.py --max-iterations 5 --target-score 8.0
```

Run voiceover generation:
```powershell
python voiceover_generator.py --script test.py --video media/output.mp4
```

### Testing the Full Pipeline

1. Start services: `docker-compose up`
2. Open frontend: http://localhost:3000
3. Submit prompt: "Explain the Pythagorean theorem"
4. Monitor logs:
   - Backend: Check job queued
   - Manim watcher: Check script picked up and rendered
   - Backend: Check video URL returned
5. Frontend should poll and display video when complete

## Environment Variables

### Required for Backend
```
GEMINI_API_KEY=your_gemini_api_key_here
```

### Optional for Backend
```
ELEVENLABS_API_KEY=your_elevenlabs_key_here  # For voiceover
REDIS_URL=redis://redis:6379                  # For queueHandler
```

### Frontend
No environment variables required for development (uses mock data).

## Code Architecture

### Frontend Architecture

**State Management**: Zustand store (`lib/store.ts`) with three slices:
- `auth`: User login/logout state
- `queue`: Video generation queue tracking
- `currentVideoId`: Active video for playback

**API Client** (`lib/api.ts`): Centralized HTTP client for backend communication
- `generateVideo()`: POST video generation request
- `getQueueStatus()`: Poll for rendering progress
- `sendChatMessage()`: RAG-based Q&A
- `getVideoUrl()`: Video file URL construction

**Component Structure**: 
- `components/ui/`: shadcn/ui primitives (47 components)
- Pages: App Router structure in `app/`
- Custom styling: Tailwind CSS with dark theme

**Data Flow**: localStorage for cross-page persistence → will need migration to backend storage for production.

### Backend Architecture (queueHandler)

**Celery Task Queue** pattern:
1. **API Server** (`src/main.py`): Receives HTTP requests, enqueues tasks
2. **Celery Worker** (`src/worker.py`): Processes tasks asynchronously
3. **Redis**: Message broker and result backend
4. **Manim Container**: Separate service watching shared volume

**Task Flow**:
- HTTP request → In-memory job status created → Celery task dispatched
- Worker generates Manim code with Gemini → Writes to `/shared/scripts/{job_id}.py`
- Manim watcher picks up script → Renders → Outputs to `/shared/videos/{job_id}.mp4`
- Frontend polls API for status updates

**Key Design**: Decoupled rendering through filesystem communication (shared Docker volume).

### Manim Architecture

**Watcher Pattern** (`watcher.py`):
- Infinite loop checking `/shared/scripts/` every 2 seconds
- Extracts Scene class name via regex
- Renders with `manim -ql` command
- Moves output to `/shared/videos/`
- Cleans up source script

**AI Improvement System** (`video_improver.py`):
- Iterative loop: Render → Analyze (Gemini Vision) → Score → Improve code → Repeat
- Scores on 5 dimensions: Visual Clarity, Pacing, Pedagogical Effectiveness, Technical Quality, Completeness
- Saves all iterations with full history for comparison
- Target: 8.0/10 score or max iterations (default 5)

**Voiceover System** (`voiceover_generator.py`):
- Extracts script text from Manim code
- Generates voiceover with ElevenLabs API
- Merges audio+video with FFmpeg
- Fallback: Returns video without voiceover if API fails

## Important Patterns

### Error Handling

**Frontend**: Minimal error handling currently. Add try/catch around API calls and use toast notifications for user feedback.

**Backend**: BackgroundTasks pattern means errors don't propagate to HTTP response. Check queue status for error messages.

**Manim**: Validation via AST parsing before rendering. Invalid scripts are deleted to prevent queue blocking.

### File Naming Convention

- Frontend: lowercase kebab-case (`alert-dialog.tsx`)
- Backend: snake_case (`api_server.py`)
- Components: PascalCase for exports (`export default function VideoPlayer()`)

### API Response Patterns

All API endpoints return JSON with consistent structure:
```typescript
{
  "video_id": string,       // UUID job identifier
  "status": string,         // queued | generating_code | rendering | complete | error
  "progress": number,       // 0-100
  "message": string,        // Human-readable status
  "video_url"?: string,     // Available when status === "complete"
  "error"?: string          // Available when status === "error"
}
```

### Docker Compose Shared Volume

Critical: `/shared` volume enables inter-service communication without HTTP:
- `queueHandler/worker` writes scripts → `/shared/scripts/`
- `manim` container reads scripts, writes videos → `/shared/videos/`
- `queueHandler/api` serves videos from `/shared/videos/`

## Testing Strategy

### Frontend Tests
Currently no tests. Recommended:
```powershell
# Install testing libraries
npm install -D @testing-library/react @testing-library/jest-dom jest

# Run tests
npm test
```

### Backend Tests
```powershell
# API endpoint testing
curl -X POST http://localhost:8000/api/generate-video -F "prompt=Test" -F "files=@test.pdf"
curl http://localhost:8000/api/queue-status/{video_id}
```

### Integration Tests
Use `queueHandler/basictests.http` file with REST Client extension in VS Code.

## Debugging

### Frontend Not Connecting to Backend
1. Check `lib/api.ts` has correct `API_BASE` URL
2. Verify CORS configuration in backend allows `localhost:3000`
3. Check browser console for network errors

### Video Not Rendering
1. Check Manim container logs: `docker logs manim-renderer`
2. Verify script was written to `/shared/scripts/`
3. Check for Python syntax errors in generated Manim code
4. Ensure Scene class exists and is properly named

### Celery Worker Not Processing
1. Check Redis is running: `docker ps | grep redis`
2. Verify `REDIS_URL` environment variable
3. Check worker logs: `docker logs queuehandler-worker`
4. Verify task is imported in `worker.py`

### Gemini API Errors
1. Verify `GEMINI_API_KEY` is set and valid
2. Check rate limits (60 requests/minute on free tier)
3. Test connection: `python backend/setup_api.py`

## Known Limitations

- **No persistent database**: Job queue is in-memory, lost on restart
- **No authentication**: Frontend has mock login only
- **File uploads not persisted**: Uploads saved to local disk, not cloud storage
- **Single concurrent render**: Manim watcher processes one video at a time
- **No retry logic**: Failed renders are not automatically retried
- **Voiceover timing**: Not synchronized with animation timing

## Production Deployment Considerations

**Required Changes**:
1. Replace in-memory queue with PostgreSQL/MongoDB
2. Add authentication (JWT tokens via Supabase)
3. Use S3/R2 for video storage instead of local filesystem
4. Implement proper Celery result backend (Redis persistence)
5. Add rate limiting and request validation
6. Enable HTTPS for all services
7. Use CDN for video delivery
8. Add monitoring (Sentry, DataDog, etc.)
9. Scale Celery workers horizontally
10. Add database migrations (Alembic)

## Key Files to Understand

1. **`docker-compose.yml`**: Orchestrates all services, defines volumes and networking
2. **`frontend-ui/lib/store.ts`**: Global state management schema
3. **`queueHandler/src/worker.py`**: Task processing logic and Gemini integration
4. **`manim/watcher.py`**: File-watching render loop
5. **`backend/api_server.py`**: Alternative single-process backend with inline rendering

## Common Pitfalls

1. **Port conflicts**: Ensure 3000, 8000, 6379 are available before `docker-compose up`
2. **Windows paths**: Use forward slashes in Docker volume paths, even on Windows
3. **API key visibility**: Never commit `.env` files with real API keys
4. **Scene class naming**: Manim watcher extracts class name via regex - ensure it matches `class XYZ(Scene)` pattern
5. **Video file size**: Large videos may exceed Gemini's upload limit (consider compression)
6. **Celery import paths**: Use absolute imports (`from src.worker import ...`) with `PYTHONPATH=/app`

## Additional Documentation

- **Frontend details**: `frontend-ui/WARP.md` (comprehensive frontend architecture)
- **Manim video improver**: `manim/README_VIDEO_IMPROVER.md`
- **Voiceover setup**: `manim/VOICEOVER_SETUP.md`
- **System architecture**: `manim/SYSTEM_OVERVIEW.md`
- **Integration guide**: `INTEGRATION_GUIDE.md` (frontend-backend connection)
- **Quick start**: `QUICKSTART.md`
