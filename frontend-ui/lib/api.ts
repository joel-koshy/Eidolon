const API_BASE = 'http://localhost:8000';

export async function generateVideo(prompt: string, files: File[]) {
  const formData = new FormData();
  formData.append('prompt', prompt);
  files.forEach(file => formData.append('files', file));
  
  const response = await fetch(`${API_BASE}/api/generate-video`, {
    method: 'POST',
    body: formData,
  });
  
  if (!response.ok) {
    throw new Error('Failed to generate video');
  }
  
  return response.json();
}

export async function getQueueStatus(videoId: string) {
  const response = await fetch(`${API_BASE}/api/queue-status/${videoId}`);
  
  if (!response.ok) {
    throw new Error('Failed to get queue status');
  }
  
  return response.json();
}

export function getVideoUrl(videoId: string) {
  return `${API_BASE}/api/video/${videoId}`;
}

export async function sendChatMessage(videoId: string, message: string, history: any[]) {
  const response = await fetch(`${API_BASE}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ video_id: videoId, message, history }),
  });
  
  if (!response.ok) {
    throw new Error('Failed to send message');
  }
  
  return response.json();
}
