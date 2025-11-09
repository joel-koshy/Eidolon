import { create } from 'zustand';

type User = {
  email: string;
  id: string;
} | null;

type QueueItem = {
  id: number;
  prompt: string;
  videoId?: string;
  status: 'queued' | 'rendering' | 'complete' | 'error';
  progress?: number;
  message?: string;
  videoUrl?: string;
  createdAt: number;
};

type Store = {
  // Auth Slice
  isLoggedIn: boolean;
  user: User;
  login: (email: string) => void;
  logout: () => void;
  
  // Queue Slice
  queue: QueueItem[];
  addToQueue: (prompt: string, videoId?: string) => void;
  updateQueueItemStatus: (id: number, status: QueueItem['status'], progress?: number, message?: string, videoUrl?: string) => void;
  removeFromQueue: (id: number) => void;
  
  // Current video
  currentVideoId: string | null;
  setCurrentVideoId: (id: string) => void;
};

export const useStore = create<Store>((set) => ({
  // Auth Slice
  isLoggedIn: false,
  user: null,
  login: (email: string) =>
    set({
      isLoggedIn: true,
      user: { email, id: Date.now().toString() },
    }),
  logout: () =>
    set({
      isLoggedIn: false,
      user: null,
    }),

  // Queue Slice
  queue: [],
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
  updateQueueItemStatus: (id: number, status: QueueItem['status'], progress?: number, message?: string, videoUrl?: string) =>
    set((state) => ({
      queue: state.queue.map((item) =>
        item.id === id ? { ...item, status, progress, message, videoUrl } : item
      ),
    })),
  removeFromQueue: (id: number) =>
    set((state) => ({
      queue: state.queue.filter((item) => item.id !== id),
    })),
    //@ts-ignore
      setQueue: (newQueue) => set({ queue: newQueue }),
  
  // Current video
  currentVideoId: null,
  setCurrentVideoId: (id: string) => set({ currentVideoId: id }),
}));
