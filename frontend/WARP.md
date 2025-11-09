# AI Video Generator - Project Overview

## Project Description
A Next.js web application for generating AI-powered Manim animation videos. Users provide text prompts and optional resource files to create educational video content with automated script generation and Q&A capabilities.

---

## Core Components

### 1. **Routing & Pages** (`app/`)
Next.js 13+ App Router with three main routes:

#### **Home Page** (`app/page.tsx`)
- **Purpose**: Video generation input interface
- **Key Features**:
  - Text prompt input with textarea
  - Drag-and-drop file upload (PDF, TXT, MD)
  - File management (add/remove files)
  - Client-side state management with `useState`
  - Navigation to processing page via Next.js router
- **Data Flow**: Stores prompt and file names in `localStorage` before navigation

#### **Processing Page** (`app/processing/page.tsx`)
- **Purpose**: Progress tracking and script preview during video generation
- **Key Features**:
  - Multi-step progress indicator (3 stages)
  - Animated progress bar with percentage display
  - Real-time script generation preview
  - Timer-based state transitions using `useEffect`
- **Mock Implementation**: Simulates 15-second processing with hardcoded Pythagorean theorem script
- **Data Flow**: Retrieves prompt from `localStorage`, stores generated script, redirects to results

#### **Results Page** (`app/results/page.tsx`)
- **Purpose**: Video playback and interactive Q&A interface
- **Key Features**:
  - HTML5 video player with controls
  - Script display panel
  - Real-time chat interface for Q&A
  - Message history with user/assistant differentiation
  - Auto-scrolling message feed
- **Mock Implementation**: Uses sample video URL, provides randomized predefined responses

#### **Root Layout** (`app/layout.tsx`)
- **Purpose**: Application-wide layout and metadata
- **Configuration**: 
  - Inter font from Google Fonts
  - HTML structure with metadata
  - Global CSS imports

### 2. **UI Component Library** (`components/ui/`)
shadcn/ui-based component system (47 components) built on Radix UI primitives:

**Key Components**:
- **Form Controls**: `button.tsx`, `input.tsx`, `textarea.tsx`, `checkbox.tsx`, `select.tsx`, `radio-group.tsx`, `slider.tsx`, `switch.tsx`
- **Layout**: `card.tsx`, `separator.tsx`, `scroll-area.tsx`, `resizable.tsx`, `tabs.tsx`
- **Overlays**: `dialog.tsx`, `sheet.tsx`, `drawer.tsx`, `popover.tsx`, `hover-card.tsx`, `tooltip.tsx`, `alert-dialog.tsx`
- **Feedback**: `toast.tsx`, `toaster.tsx`, `alert.tsx`, `progress.tsx`, `skeleton.tsx`
- **Navigation**: `navigation-menu.tsx`, `menubar.tsx`, `dropdown-menu.tsx`, `context-menu.tsx`, `breadcrumb.tsx`, `pagination.tsx`
- **Data Display**: `table.tsx`, `avatar.tsx`, `badge.tsx`, `calendar.tsx`, `carousel.tsx`, `chart.tsx`
- **Advanced**: `command.tsx`, `accordion.tsx`, `collapsible.tsx`, `form.tsx`, `input-otp.tsx`

**Design Patterns**:
- Component composition using Radix UI Slot pattern
- Variant-based styling with `class-variance-authority` (CVA)
- Forwarded refs for DOM access
- TypeScript generics for type safety
- Consistent prop spreading for extensibility

### 3. **Utility Modules** (`lib/`)

#### **`utils.ts`**
- **Function**: `cn(...inputs: ClassValue[])`
- **Purpose**: Merge Tailwind CSS classes with conflict resolution
- **Implementation**: Combines `clsx` for conditional classes and `tailwind-merge` for deduplication

### 4. **Custom Hooks** (`hooks/`)

#### **`use-toast.ts`**
- **Purpose**: Global toast notification management
- **Architecture**: 
  - Reducer pattern for state management
  - Event listener system for cross-component communication
  - Memory-based state (`memoryState`) outside React lifecycle
- **Features**:
  - Toast queue with limit (1 toast)
  - Auto-dismiss with configurable delay (1000000ms)
  - Imperative API (`toast()`, `dismiss()`, `update()`)
  - React hook API (`useToast()`)
- **Action Types**: ADD_TOAST, UPDATE_TOAST, DISMISS_TOAST, REMOVE_TOAST

---

## Component Interactions

### Data Flow Architecture

```
┌─────────────┐           ┌──────────────┐           ┌─────────────┐
│  Home Page  │  localStorage  │ Processing   │  localStorage  │ Results     │
│  (Input)    ├──────────────>│  (Progress)  ├──────────────>│  (Playback) │
└─────────────┘           └──────────────┘           └─────────────┘
     │                          │                          │
     │ User Input               │ Mock Generation          │ Mock Q&A
     ▼                          ▼                          ▼
  - Prompt Text            - 3 Processing Steps       - Video Player
  - File Upload            - Script Preview           - Chat Interface
  - Validation             - Progress Tracking        - Resource Q&A
```

### Communication Methods

1. **Client-Side Routing**: Next.js `useRouter()` for page navigation
2. **Local Storage**: Cross-page data persistence
   - `videoPrompt`: User input prompt
   - `uploadedFiles`: JSON array of file names
   - `videoScript`: Generated video script
3. **React State**: Component-local state management with `useState`
4. **Side Effects**: Timer-based async operations with `useEffect`

### Styling System

```
Tailwind CSS (Base) 
    ↓
CSS Variables (--background, --foreground, etc.)
    ↓
shadcn/ui Theme System
    ↓
class-variance-authority (CVA) for variants
    ↓
cn() utility for composition
```

---

## Deployment Architecture

### Build Configuration

**Next.js Config** (`next.config.js`):
```javascript
{
  output: 'export',              // Static site generation
  eslint: { ignoreDuringBuilds: true },
  images: { unoptimized: true }  // Static export compatibility
}
```

**TypeScript** (`tsconfig.json`):
- Target: ES5
- Module: ESNext with bundler resolution
- Strict mode enabled
- Path alias: `@/*` → project root

**Tailwind** (`tailwind.config.ts`):
- Dark mode: Class-based
- CSS variables for theming
- Extended color system with HSL values
- Custom animations (accordion-down/up)
- Plugin: `tailwindcss-animate`

### Build Process

```bash
npm run dev        # Development server (Next.js)
npm run build      # Production build (static export)
npm run start      # Production preview
npm run lint       # ESLint validation
npm run typecheck  # TypeScript validation (no emit)
```

### Dependencies

**Core Framework**:
- `next@13.5.1` - React framework with App Router
- `react@18.2.0` - UI library
- `typescript@5.2.2` - Type safety

**UI Libraries**:
- `@radix-ui/react-*` - Unstyled accessible components (21 packages)
- `lucide-react@^0.446.0` - Icon library
- `tailwindcss@3.3.3` - Utility-first CSS

**Form Management**:
- `react-hook-form@^7.53.0` - Form state management
- `@hookform/resolvers@^3.9.0` - Validation integration
- `zod@^3.23.8` - Schema validation

**Additional Features**:
- `@supabase/supabase-js@^2.58.0` - Backend client (unused in current implementation)
- `date-fns@^3.6.0` - Date utilities
- `recharts@^2.12.7` - Charting library
- `sonner@^1.5.0` - Toast notifications

### Deployment Target

- **Type**: Static website (JAMstack)
- **Output**: HTML/CSS/JS files in `.next/` directory
- **Hosting**: Compatible with Vercel, Netlify, GitHub Pages, S3, etc.
- **Requirements**: 
  - Node.js 20.6.2+ for build process
  - No runtime server requirements (static export)

### Environment Variables

**Current**: Empty `.env` file
**Expected** (based on Supabase dependency):
- `NEXT_PUBLIC_SUPABASE_URL` (unused)
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` (unused)

---

## Runtime Behavior

### Application Lifecycle

1. **Initialization**:
   - Next.js hydrates static HTML on client
   - Inter font loads from Google Fonts CDN
   - Global CSS with Tailwind utilities applied
   - Dark mode variables available (not actively toggled)

2. **User Journey**:
   ```
   Landing (/) → Enter Prompt → Upload Files (optional) 
                      ↓
                 Generate Button
                      ↓
              Processing (/processing) → Progress Animation (15s)
                      ↓
              Results (/results) → Watch Video + Q&A
   ```

3. **State Management**:
   - **Page-level**: `useState` for form inputs, UI toggles
   - **Cross-page**: `localStorage` for data persistence
   - **Global**: Toast system via event listeners

### Request/Response Flow

**Current Implementation** (Mock):
- No external API calls
- Simulated processing delays with `setTimeout`
- Hardcoded responses for Q&A
- Sample video from external CDN

**Expected Future Implementation**:
- API route handlers in `app/api/` directory
- Supabase integration for backend
- Real AI model integration for:
  - Script generation
  - Manim code generation
  - Video rendering
  - Q&A with RAG (Retrieval-Augmented Generation)

### Error Handling

**Current State**: Minimal error handling
- Form validation: Disabled button when prompt is empty
- File filtering: Only accepts `.pdf`, `.txt`, `.md` extensions
- No error boundaries or try/catch blocks

**Recommended Additions**:
- React Error Boundaries in layout
- API error handling with toast notifications
- File size validation
- Network error recovery
- localStorage fallback handling

### Background Tasks

**Processing Page**:
- Timer interval running at 100ms frequency
- Calculates progress across 3 stages (3s, 4s, 8s)
- Auto-transitions between steps
- Auto-navigation after completion
- Cleanup on unmount to prevent memory leaks

**Results Page**:
- Auto-scrolling chat on new messages
- Debounced typing indicator (2s delay)
- Message history maintained in component state

---

## Development Guidelines

### Code Patterns

1. **File Naming**: 
   - Pages: `page.tsx`
   - Components: lowercase kebab-case (e.g., `alert-dialog.tsx`)
   - Utilities: lowercase (e.g., `utils.ts`)

2. **Component Structure**:
   ```typescript
   'use client'; // When using hooks/browser APIs
   
   import { ... } from '...';
   
   export default function ComponentName() {
     // State declarations
     // Side effects
     // Event handlers
     // Return JSX
   }
   ```

3. **Styling**:
   - Utility-first with Tailwind
   - Dark theme using hardcoded gray-900/950 backgrounds
   - Responsive with `lg:` breakpoints
   - Animations with `animate-in` utilities

4. **Import Aliases**:
   - `@/components` → `components/`
   - `@/lib` → `lib/`
   - `@/hooks` → `hooks/`
   - `@/app` → `app/`

### Testing Strategy

**Current**: No test files present

**Recommended Setup**:
- **Unit**: Jest + React Testing Library
- **E2E**: Playwright or Cypress
- **Type Safety**: `npm run typecheck` in CI/CD

### Performance Considerations

- Static export enables CDN caching
- Code splitting via Next.js App Router
- Image optimization disabled (unoptimized: true)
- Client-side only navigation (no SSR)
- Component tree limited depth

---

## Key Technical Decisions

1. **Static Export Over SSR**: Chosen for simplicity and CDN compatibility, sacrificing dynamic rendering
2. **localStorage Over Database**: Temporary solution for MVP, requires backend integration for production
3. **Mock Implementation**: All AI/backend logic is stubbed for frontend development
4. **shadcn/ui Over Material-UI**: Provides customizable, accessible components without heavy bundle size
5. **Client Components Only**: No server components utilized despite App Router support
6. **Direct Tailwind Styling**: Minimal CSS abstraction, trading reusability for development speed

## Future Integration Points

1. **Backend API**: 
   - `/api/generate-script` - LLM script generation
   - `/api/generate-video` - Manim rendering pipeline
   - `/api/chat` - RAG-based Q&A system

2. **Database** (Supabase):
   - User authentication
   - Video/script storage
   - Resource file uploads
   - Chat history persistence

3. **Video Processing**:
   - Manim Python integration
   - FFmpeg for video encoding
   - Cloud storage (S3/Cloudflare R2)
   - Processing queue system

4. **AI/ML Services**:
   - OpenAI/Anthropic for script generation
   - Embedding model for RAG
   - Vector database for semantic search

---

## Quick Start Commands

```bash
# Install dependencies
npm install

# Start development server
npm run dev  # http://localhost:3000

# Type checking
npm run typecheck

# Linting
npm run lint

# Production build
npm run build
npm run start

# Static export output
# .next/ directory contains deployable files
```

## File Structure Summary

```
project/
├── app/
│   ├── globals.css           # Tailwind + theme variables
│   ├── layout.tsx            # Root layout component
│   ├── page.tsx              # Home/input page
│   ├── processing/
│   │   └── page.tsx          # Progress tracking page
│   └── results/
│       └── page.tsx          # Results/playback page
├── components/
│   └── ui/                   # 47 shadcn/ui components
├── hooks/
│   └── use-toast.ts          # Toast notification system
├── lib/
│   └── utils.ts              # Class name utility
├── .env                      # Environment variables (empty)
├── components.json           # shadcn/ui configuration
├── next.config.js            # Next.js configuration
├── package.json              # Dependencies and scripts
├── postcss.config.js         # PostCSS plugins
├── tailwind.config.ts        # Tailwind theme configuration
└── tsconfig.json             # TypeScript configuration
```

## Known Limitations

- No backend integration (all functionality is mocked)
- No authentication system
- No file upload storage
- No actual video generation
- No real AI integration
- No error handling or loading states beyond UI
- No responsive mobile optimization
- localStorage data persists only in browser
- No accessibility testing performed
- ESLint disabled during builds
