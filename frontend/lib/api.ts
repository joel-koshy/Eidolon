// const API_BASE = 'http://localhost:8000';

export async function generateVideo(prompt: string, files: File[]) {
    const response = await fetch('/api/generate-video', {
    method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    prompt: prompt,
    userid: 'example-user-id',
  }),
}
  );
  
  if (!response.ok) {
    throw new Error('Failed to generate video');
  }
  
  return response.json();
}


export async function getQueueStatus(videoId: string): Promise<string> {
  const response = await fetch(`/api/video/${videoId}`);

  if (!response.ok) {
    throw new Error('Failed to get queue status');
  }

  const data = await response.json();
  return data.status; // return only the status
}


export function getVideoUrl(videoId: string) {
  return `/api/video/${videoId}`;
}

export async function sendChatMessage(videoId: string, message: string, history: any[]) {
  const response = await fetch(`/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ video_id: videoId, message, history }),
  });
  
  if (!response.ok) {
    throw new Error('Failed to send message');
  }
  
  return response.json();
}
