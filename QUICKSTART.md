# Eidolon - Quick Start Guide

Get up and running with the Eidolon Video Generator frontend in minutes.

## Prerequisites

- Node.js 20 or higher
- npm (comes with Node.js)
- A modern web browser

## Installation & Setup

### 1. Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Create Environment File (Optional)
```bash
cp .env.example .env.local
```

### 4. Start Development Server
```bash
npm run dev
```

### 5. Open in Browser
Navigate to [http://localhost:3000](http://localhost:3000)

## What You'll See

The application has a beautiful gradient interface with four main stages:

1. **Prompt & Resources** - Enter your video idea and upload files
2. **Script Generation** - View the AI-generated script
3. **Video Generation** - Watch as your Manim video is created
4. **Complete** - View your video and ask questions via chat

## Testing the Application

The frontend currently uses mock data, so you can test the entire workflow without a backend:

1. **Enter a prompt** like "Explain the Pythagorean theorem with visual proofs"
2. **Upload files** (optional) - PDFs, DOCX, or TXT files
3. **Click "Generate Video"**
4. **Watch the workflow**:
   - Script appears immediately (mock data)
   - Video generation starts automatically
   - After ~10 seconds, a sample video will load
   - Chat interface becomes active
5. **Ask questions** in the chat to see RAG responses (mock data)

## Available Scripts

```bash
npm run dev      # Start development server (port 3000)
npm run build    # Build for production
npm run start    # Start production server
npm run lint     # Run ESLint
```

## Project Features

### ✨ User Interface
- Modern gradient design with glass morphism effects
- Responsive layout (desktop, tablet, mobile)
- Drag-and-drop file upload
- Real-time progress tracking
- Custom scrollbars and animations

### 🎯 Core Components
- **PromptInput**: Multi-line text input + file uploader
- **VideoScript**: Displays generated script with syntax highlighting
- **VideoPlayer**: HTML5 video player with download button
- **ChatInterface**: Q&A interface with message history
- **ProgressTracker**: Visual workflow indicator

### 🔌 API Routes (Mock)
All API routes return mock data for development:
- `/api/generate-script` - Returns mock script and session ID
- `/api/video-status/:sessionId` - Simulates video generation (10s)
- `/api/chat` - Returns mock RAG responses

## Next Steps

### For Frontend Development
- Customize components in `components/`
- Modify styles in `app/globals.css`
- Update TypeScript types in `types/`
- Add new features to `app/page.tsx`

### For Backend Integration
1. Create a backend API server (Python/FastAPI recommended)
2. Implement the three API endpoints (see README.md)
3. Update environment variable `BACKEND_URL` in `.env.local`
4. Replace mock implementations in `app/api/` routes

## Troubleshooting

### Port 3000 Already in Use
```bash
# Use a different port
npm run dev -- -p 3001
```

### Build Errors
```bash
# Clear Next.js cache
rm -rf .next
npm run build
```

### Dependencies Issues
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
```

## File Upload Types

Currently accepts:
- PDF (`.pdf`)
- Text (`.txt`)
- Word Documents (`.docx`)

To add more types, edit `components/PromptInput.tsx`:
```typescript
accept: {
  'application/pdf': ['.pdf'],
  'text/plain': ['.txt'],
  // Add your types here
}
```

## Keyboard Shortcuts

- `Enter` in chat input → Send message
- `Ctrl/Cmd + Enter` in prompt → Submit (when implemented)

## Browser Support

Tested on:
- Chrome 120+
- Firefox 121+
- Safari 17+
- Edge 120+

## Need Help?

- Check `README.md` for detailed documentation
- See `frontend/README.md` for frontend-specific info
- Review API specification for backend integration
- Open an issue on GitHub

## What's Included

```
frontend/
├── app/
│   ├── api/              ✓ Mock API routes
│   ├── page.tsx          ✓ Main application
│   ├── layout.tsx        ✓ Root layout
│   └── globals.css       ✓ Custom styles
├── components/           ✓ All UI components
├── types/               ✓ TypeScript definitions
└── public/              ✓ Static assets
```

## Production Deployment

```bash
# Build the application
npm run build

# Test production build locally
npm start

# Deploy to Vercel (recommended)
vercel deploy
```

---

**Happy coding! 🚀**

For more information, see the main [README.md](README.md)
