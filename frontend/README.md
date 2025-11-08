# Eidolon Video Generator - Frontend

A modern Next.js frontend for an AI-powered educational video generation application using Manim animations.

## Features

- **Prompt Input**: Users can describe the video they want to create
- **Resource Upload**: Drag-and-drop interface for uploading PDFs, DOCX, and TXT files
- **Script Generation**: Real-time display of AI-generated video scripts
- **Video Generation**: Visual feedback during Manim animation rendering
- **RAG-Powered Chat**: Interactive Q&A based on uploaded resources and video content
- **Progress Tracking**: Visual workflow stages from input to completion

## Tech Stack

- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4
- **UI Components**: Custom components with Lucide React icons
- **File Upload**: react-dropzone
- **HTTP Client**: Native Fetch API

## Getting Started

### Prerequisites

- Node.js 20+ and npm
- A backend API server (see Backend Integration section)

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
cp .env.example .env.local
```

3. Update `.env.local` with your backend URL:
```env
BACKEND_URL=http://localhost:8000
```

### Development

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── app/
│   ├── api/                    # API route handlers
│   │   ├── chat/              # RAG-based chat endpoint
│   │   ├── generate-script/   # Script generation endpoint
│   │   └── video-status/      # Video status polling endpoint
│   ├── globals.css            # Global styles
│   ├── layout.tsx             # Root layout
│   └── page.tsx               # Main page component
├── components/
│   ├── ChatInterface.tsx      # RAG Q&A chat component
│   ├── ProgressTracker.tsx    # Workflow progress indicator
│   ├── PromptInput.tsx        # User input and file upload
│   ├── VideoPlayer.tsx        # Video playback component
│   └── VideoScript.tsx        # Script display component
└── public/                    # Static assets
```

## Backend Integration

The frontend expects the following backend API endpoints:

### 1. Generate Script
**POST** `/api/generate-script`

**Request**: FormData
- `prompt`: string - User's video description
- `resources`: File[] - Uploaded resource files

**Response**:
```json
{
  "sessionId": "string",
  "script": "string",
  "status": "success"
}
```

### 2. Video Status
**GET** `/api/video-status/:sessionId`

**Response**:
```json
{
  "status": "generating" | "completed" | "error",
  "videoUrl": "string",
  "progress": "number",
  "message": "string"
}
```

### 3. Chat (RAG)
**POST** `/api/chat`

**Request**:
```json
{
  "sessionId": "string",
  "message": "string"
}
```

**Response**:
```json
{
  "response": "string",
  "sessionId": "string",
  "timestamp": "string"
}
```

## Customization

### Styling
- Modify `app/globals.css` for global styles
- Update Tailwind configuration in `tailwind.config.ts`
- Component styles use Tailwind utility classes

### API Routes
The API routes in `app/api/` currently contain mock implementations. Update these files to integrate with your actual backend:

1. Replace mock responses with actual backend API calls
2. Update the `BACKEND_URL` environment variable
3. Handle authentication if required
4. Add error handling and retry logic

### File Upload
Modify accepted file types in `components/PromptInput.tsx`:
```typescript
accept: {
  'application/pdf': ['.pdf'],
  'text/plain': ['.txt'],
  // Add more types here
}
```

## Workflow

1. **Input Stage**: User enters prompt and uploads optional resources
2. **Script Generation**: Backend generates video script using LLM and RAG
3. **Video Generation**: Manim code is generated and executed in Docker
4. **Completion**: Video is displayed, chat is enabled for Q&A

## Development Notes

- The app uses Next.js App Router with React Server Components
- All interactive components are marked with `'use client'`
- API routes use Next.js 16+ conventions with async params
- Mock data is provided for development without a backend

## Browser Support

- Modern browsers with ES2017+ support
- Video playback requires HTML5 video support
- File upload uses native File API

## License

This project is part of the Eidolon video generation system.

This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
