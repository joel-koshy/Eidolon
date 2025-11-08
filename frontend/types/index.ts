// API Response Types

export interface GenerateScriptResponse {
  sessionId: string;
  script: string;
  status: 'success' | 'error';
  error?: string;
}

export interface VideoStatusResponse {
  status: 'generating' | 'completed' | 'error';
  videoUrl?: string;
  progress?: number;
  message?: string;
  error?: string;
}

export interface ChatResponse {
  response: string;
  sessionId: string;
  timestamp: string;
  error?: string;
}

// Application State Types

export type WorkflowStage = 'input' | 'script' | 'generating' | 'complete';

export interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface Session {
  id: string;
  prompt: string;
  resources: File[];
  script: string;
  videoUrl: string;
  stage: WorkflowStage;
}

// Component Props Types

export interface PromptInputProps {
  onSubmit: (prompt: string, resources: File[]) => void;
}

export interface VideoScriptProps {
  script: string;
  isGenerating: boolean;
}

export interface VideoPlayerProps {
  videoUrl: string;
  isGenerating: boolean;
}

export interface ChatInterfaceProps {
  sessionId: string;
  enabled: boolean;
}

export interface ProgressTrackerProps {
  currentStage: WorkflowStage;
}
