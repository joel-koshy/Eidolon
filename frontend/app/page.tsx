'use client';

import { useState, useEffect, useRef } from 'react';
import { Sparkles, UploadCloud, FileText, Film, Send, X, Layers, LogOut, MessageSquare, Clock, CheckCircle, Loader2 } from 'lucide-react';
import { useStore } from '@/lib/store';
import { generateVideo, getQueueStatus, getVideoUrl, sendChatMessage } from '@/lib/api';

export default function EidolonApp() {
  const [view, setView] = useState('landing');
  const [isTransitioning, setIsTransitioning] = useState(false);
  const isLoggedIn = useStore((state) => state.isLoggedIn);

  const navigateTo = (newView: string) => {
    setIsTransitioning(true);
    setTimeout(() => {
      setView(newView);
      setIsTransitioning(false);
    }, 250);
  };

  // Redirect to login if trying to access protected routes
  useEffect(() => {
    const protectedRoutes = ['generator', 'history', 'results'];
    if (protectedRoutes.includes(view) && !isLoggedIn) {
      navigateTo('login');
    }
  }, [view, isLoggedIn]);

  return (
    <>
      <style jsx global>{`
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
        
        body { 
          font-family: 'Inter', sans-serif;
          background-color: #080A0F;
        }

        .view-enter { animation: fadeIn 0.3s ease-out forwards; }
        .view-exit { animation: fadeOut 0.2s ease-in forwards; }

        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeOut {
          from { opacity: 1; transform: translateY(0); }
          to { opacity: 0; transform: translateY(-10px); }
        }

        .gradient-text {
          background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .glow-purple {
          box-shadow: 0 0 40px rgba(139, 92, 246, 0.3), 0 0 80px rgba(139, 92, 246, 0.15);
        }

        .glow-purple-hover:hover {
          box-shadow: 0 0 50px rgba(139, 92, 246, 0.5), 0 0 100px rgba(139, 92, 246, 0.25);
        }

        .glow-blue {
          box-shadow: 0 0 40px rgba(59, 130, 246, 0.3), 0 0 80px rgba(59, 130, 246, 0.15);
        }

        .nebula-purple {
          position: absolute;
          width: 600px;
          height: 600px;
          background: radial-gradient(circle, rgba(139, 92, 246, 0.15) 0%, transparent 70%);
          filter: blur(100px);
          pointer-events: none;
        }

        .nebula-blue {
          position: absolute;
          width: 600px;
          height: 600px;
          background: radial-gradient(circle, rgba(59, 130, 246, 0.12) 0%, transparent 70%);
          filter: blur(100px);
          pointer-events: none;
        }

        .glass-border {
          border: 1px solid rgba(255, 255, 255, 0.1);
          background: rgba(255, 255, 255, 0.02);
        }

        .glass-border-hover:hover {
          border: 1px solid rgba(255, 255, 255, 0.15);
          background: rgba(255, 255, 255, 0.03);
        }

        .liquid-glass {
          backdrop-filter: blur(40px);
          -webkit-backdrop-filter: blur(40px);
          background: rgba(0, 0, 0, 0.2);
          border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .scrollbar-thin::-webkit-scrollbar {
          width: 6px;
        }

        .scrollbar-thin::-webkit-scrollbar-track {
          background: transparent;
        }

        .scrollbar-thin::-webkit-scrollbar-thumb {
          background: rgba(255, 255, 255, 0.1);
          border-radius: 3px;
        }

        .scrollbar-thin::-webkit-scrollbar-thumb:hover {
          background: rgba(255, 255, 255, 0.2);
        }
      `}</style>

      <div className="min-h-screen text-white" style={{ backgroundColor: '#080A0F' }}>
        {/* Navbar - show on all views except landing */}
        {view !== 'landing' && <Navbar navigateTo={navigateTo} />}
        
        <div className={isTransitioning ? 'view-exit' : 'view-enter'}>
          {view === 'landing' && <LandingView navigateTo={navigateTo} />}
          {view === 'login' && <LoginView navigateTo={navigateTo} />}
          {view === 'register' && <RegisterView navigateTo={navigateTo} />}
          {view === 'generator' && <GeneratorView navigateTo={navigateTo} />}
          {view === 'history' && <HistoryView navigateTo={navigateTo} />}
          {view === 'results' && <ResultsView navigateTo={navigateTo} />}
        </div>
      </div>
    </>
  );
}

// ==================== NAVBAR ====================
function Navbar({ navigateTo }: { navigateTo: (view: string) => void }) {
  const [isQueueOpen, setIsQueueOpen] = useState(false);
  const queue = useStore((state) => state.queue);
  const updateQueueItemStatus = useStore((state) => state.updateQueueItemStatus);
  const setCurrentVideoId = useStore((state) => state.setCurrentVideoId);
  const logout = useStore((state) => state.logout);
  const user = useStore((state) => state.user);
  // @ts-ignore
  const setQueue = useStore((state) => state.setQueue);

  useEffect(() => {
    async function fetchPendingVideos() {
      try {
        const response = await fetch("/api/queued-prompts", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          console.error("Failed to fetch pending videos:", response.statusText);
          return;
        }

        const data = await response.json();

        if (data.success && Array.isArray(data.data)) {
          // Update the Zustand store
          setQueue(data.data);
          console.log("Queue initialized with pending videos:", data.data);
        } else {
          console.error("Unexpected data format:", data);
        }
      } catch (err) {
        console.error("Error fetching pending videos:", err);
      }
    }

    fetchPendingVideos();
    // Cleanup on unmount
  }, [setQueue]);

  // Poll queue status
  useEffect(() => {
    console.log('Starting queue status polling...');
    const interval = setInterval(async () => {
      for (const item of queue) {
        if (item.videoId && item.status !== 'complete' && item.status !== 'error') {
          try {
            const status = await getQueueStatus(item.id.toString());
            updateQueueItemStatus(
              item.id,
              // @ts-ignore
              status
            );
          } catch (error) {
            console.error('Failed to fetch status', error);
          }
        }
      }
    }, 3000); // Poll every 3 seconds
    
    return () => clearInterval(interval);
  }, [queue, updateQueueItemStatus]);

  const handleLogout = () => {
    logout();
    navigateTo('landing');
  };

  return (
    <>
      <nav className="glass-border border-b sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => navigateTo('generator')}
              className="text-2xl font-black gradient-text hover:opacity-80 transition-opacity"
            >
              EIDOLON
            </button>

            <div className="flex items-center gap-6">
              <button
                onClick={() => navigateTo('history')}
                className="text-gray-400 hover:text-white font-medium transition-colors"
              >
                History
              </button>

              <button
                onClick={() => setIsQueueOpen(true)}
                className="relative p-2 glass-border rounded-lg hover:bg-white/5 transition-colors"
              >
                <Layers className="w-5 h-5 text-purple-400" />
                {queue.length > 0 && (
                  <span className="absolute -top-1 -right-1 w-5 h-5 bg-purple-600 rounded-full text-xs flex items-center justify-center glow-purple">
                    {queue.length}
                  </span>
                )}
              </button>

              <button
                onClick={handleLogout}
                className="p-2 glass-border rounded-lg hover:bg-white/5 transition-colors"
                title="Logout"
              >
                <LogOut className="w-5 h-5 text-gray-400" />
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Queue Modal */}
      {isQueueOpen && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-6">
          <div className="liquid-glass rounded-2xl p-8 max-w-2xl w-full max-h-[80vh] overflow-hidden flex flex-col">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <Layers className="w-7 h-7 text-purple-400" />
                <h2 className="text-3xl font-bold text-white tracking-tight">Render Queue</h2>
              </div>
              <button
                onClick={() => setIsQueueOpen(false)}
                className="p-2 glass-border rounded-lg hover:bg-white/10 transition-colors"
              >
                <X className="w-5 h-5 text-gray-400" />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto space-y-4 scrollbar-thin">
              {queue.length === 0 ? (
                <div className="text-center py-16">
                  <Clock className="w-16 h-16 text-gray-700 mx-auto mb-4" />
                  <p className="text-gray-400 text-lg">Your render queue is empty</p>
                </div>
              ) : (
                queue.map((item) => (
                  <button
                    key={item.id}
                    onClick={() => {
                      if (item.status === 'complete' && item.videoId) {
                        setCurrentVideoId(item.videoId);
                        setIsQueueOpen(false);
                        navigateTo('results');
                      }
                    }}
                    className={`w-full glass-border rounded-xl p-6 text-left transition-all ${
                      item.status === 'complete' ? 'glass-border-hover cursor-pointer' : 'cursor-default'
                    }`}
                  >
                    <div className="flex items-start gap-4">
                      <div className="flex-shrink-0 mt-1">
                        {item.status === 'complete' ? (
                          <CheckCircle className="w-6 h-6 text-purple-400" />
                        ) : item.status === 'rendering' || item.status === 'queued' ? (
                          <Loader2 className="w-6 h-6 text-purple-400 animate-spin" />
                        ) : item.status === 'error' ? (
                          <X className="w-6 h-6 text-red-400" />
                        ) : (
                          <Clock className="w-6 h-6 text-gray-600" />
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-white font-medium mb-2 line-clamp-2">{item.prompt}</p>
                        <p className={`text-sm mb-1 ${
                          item.status === 'complete' ? 'text-purple-400' :
                          item.status === 'rendering' || item.status === 'queued' ? 'text-blue-400' :
                          item.status === 'error' ? 'text-red-400' :
                          'text-gray-500'
                        }`}>
                          {item.message || (
                            item.status === 'complete' ? 'Complete - Click to view' :
                            item.status === 'rendering' ? 'Rendering...' :
                            item.status === 'error' ? 'Error' :
                            'Queued'
                          )}
                        </p>
                        {item.progress !== undefined && item.status !== 'complete' && (
                          <div className="w-full bg-gray-800 rounded-full h-2 mt-2">
                            <div
                              className="bg-purple-500 h-2 rounded-full transition-all duration-300"
                              style={{ width: `${item.progress}%` }}
                            />
                          </div>
                        )}
                      </div>
                    </div>
                  </button>
                ))
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}

// ==================== LANDING VIEW ====================
function LandingView({ navigateTo }: { navigateTo: (view: string) => void }) {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center relative overflow-hidden" style={{ backgroundColor: '#080A0F' }}>
      <div className="nebula-purple" style={{ top: '15%', left: '10%' }}></div>
      <div className="nebula-blue" style={{ bottom: '20%', right: '15%' }}></div>

      <div className="relative z-10 text-center space-y-16 px-6 py-24">
        <div className="space-y-8">
          <h1 className="text-8xl md:text-9xl font-black gradient-text tracking-tight leading-none">
            EIDOLON
          </h1>
          
          <p className="text-xl md:text-2xl text-gray-400 max-w-3xl mx-auto leading-relaxed">
            Create stunning AI-powered Manim animations with the next generation of video synthesis
          </p>
        </div>

        <button
          onClick={() => navigateTo('login')}
          className="group relative px-14 py-5 bg-gradient-to-r from-purple-600 to-purple-500 rounded-full font-bold text-lg text-white overflow-hidden transition-all duration-300 hover:scale-[1.02] glow-purple glow-purple-hover"
        >
          <span className="relative z-10 flex items-center gap-3">
            <Sparkles className="w-6 h-6" />
            Start Creating
          </span>
        </button>
      </div>
    </div>
  );
}

// ==================== LOGIN VIEW ====================
function LoginView({ navigateTo }: { navigateTo: (view: string) => void }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const login = useStore((state) => state.login);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (email && password) {
      login(email);
      navigateTo('generator');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-6 py-24 relative overflow-hidden" style={{ backgroundColor: '#080A0F' }}>
      <div className="nebula-purple" style={{ top: '20%', right: '10%' }}></div>

      <div className="w-full max-w-md space-y-8 relative z-10">
        <div className="text-center space-y-4">
          <h1 className="text-6xl font-black gradient-text tracking-tight">EIDOLON</h1>
          <p className="text-gray-400 text-lg">Sign in to your account</p>
        </div>

        <form onSubmit={handleSubmit} className="glass-border rounded-2xl p-10 space-y-6">
          <div>
            <label className="block text-white font-semibold mb-3">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              className="w-full glass-border rounded-xl px-6 py-4 text-white placeholder:text-gray-600 focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition-all"
              required
            />
          </div>

          <div>
            <label className="block text-white font-semibold mb-3">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full glass-border rounded-xl px-6 py-4 text-white placeholder:text-gray-600 focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition-all"
              required
            />
          </div>

          <button
            type="submit"
            className="w-full px-8 py-4 bg-gradient-to-r from-purple-600 to-purple-500 rounded-xl font-bold text-white hover:scale-[1.02] transition-transform glow-purple glow-purple-hover"
          >
            Login
          </button>
        </form>

        <p className="text-center text-gray-400">
          Don't have an account?{' '}
          <button
            onClick={() => navigateTo('register')}
            className="text-purple-400 hover:text-purple-300 font-medium transition-colors"
          >
            Register
          </button>
        </p>
      </div>
    </div>
  );
}

// ==================== REGISTER VIEW ====================
function RegisterView({ navigateTo }: { navigateTo: (view: string) => void }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const login = useStore((state) => state.login);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (email && password && password === confirmPassword) {
      login(email);
      navigateTo('generator');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-6 py-24 relative overflow-hidden" style={{ backgroundColor: '#080A0F' }}>
      <div className="nebula-blue" style={{ bottom: '20%', left: '10%' }}></div>

      <div className="w-full max-w-md space-y-8 relative z-10">
        <div className="text-center space-y-4">
          <h1 className="text-6xl font-black gradient-text tracking-tight">EIDOLON</h1>
          <p className="text-gray-400 text-lg">Create your account</p>
        </div>

        <form onSubmit={handleSubmit} className="glass-border rounded-2xl p-10 space-y-6">
          <div>
            <label className="block text-white font-semibold mb-3">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              className="w-full glass-border rounded-xl px-6 py-4 text-white placeholder:text-gray-600 focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition-all"
              required
            />
          </div>

          <div>
            <label className="block text-white font-semibold mb-3">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full glass-border rounded-xl px-6 py-4 text-white placeholder:text-gray-600 focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition-all"
              required
            />
          </div>

          <div>
            <label className="block text-white font-semibold mb-3">Confirm Password</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full glass-border rounded-xl px-6 py-4 text-white placeholder:text-gray-600 focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition-all"
              required
            />
          </div>

          <button
            type="submit"
            className="w-full px-8 py-4 bg-gradient-to-r from-purple-600 to-purple-500 rounded-xl font-bold text-white hover:scale-[1.02] transition-transform glow-purple glow-purple-hover"
          >
            Register
          </button>
        </form>

        <p className="text-center text-gray-400">
          Already have an account?{' '}
          <button
            onClick={() => navigateTo('login')}
            className="text-purple-400 hover:text-purple-300 font-medium transition-colors"
          >
            Login
          </button>
        </p>
      </div>
    </div>
  );
}

// ==================== GENERATOR VIEW ====================
function GeneratorView({ navigateTo }: { navigateTo: (view: string) => void }) {
  const [prompt, setPrompt] = useState('');
  const [files, setFiles] = useState<File[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [allVideos, setAllVideos] = useState<any[]>([]);
  const addToQueue = useStore((state) => state.addToQueue);
  const setCurrentVideoId = useStore((state) => state.setCurrentVideoId);
  const queue = useStore((state) => state.queue);
  
  // Load all videos from queue (completed ones)
  useEffect(() => {
    const completed = queue.filter(item => item.status === 'complete' && item.videoId);
    setAllVideos(completed);
  }, [queue]);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFiles = Array.from(e.dataTransfer.files).filter(file =>
      ['.pdf', '.txt'].some(ext => file.name.toLowerCase().endsWith(ext))
    );
    setFiles(prev => [...prev, ...droppedFiles]);
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const selectedFiles = Array.from(e.target.files).filter(file =>
        ['.pdf', '.txt'].some(ext => file.name.toLowerCase().endsWith(ext))
      );
      setFiles(prev => [...prev, ...selectedFiles]);
    }
  };

  const removeFile = (index: number) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleGenerate = async () => {
    if (prompt.trim()) {
      try {
        const result = await generateVideo(prompt, files);
        const queueId = Date.now();
        addToQueue(prompt, result.video_id);
        setPrompt('');
        setFiles([]);
        alert('Video generation started! Check the queue icon to see progress.');
      } catch (error) {
        console.error('Error generating video:', error);
        alert('Failed to start video generation. Make sure the backend is running.');
      }
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-6 py-24 relative overflow-hidden" style={{ backgroundColor: '#080A0F' }}>
      <div className="nebula-purple" style={{ top: '10%', right: '5%' }}></div>
      
      <div className="w-full max-w-5xl space-y-12 relative z-10">
        <div className="text-center space-y-6 mb-16">
          <h1 className="text-6xl md:text-7xl font-extrabold gradient-text tracking-tight leading-none">EIDOLON</h1>
          <p className="text-gray-400 text-lg md:text-xl leading-relaxed">Design your vision, generate your masterpiece</p>
        </div>

        <div className="glass-border glass-border-hover rounded-2xl p-10 transition-all duration-300">
          <label className="block mb-6">
            <span className="text-white font-semibold text-2xl flex items-center gap-3 tracking-tight">
              <Sparkles className="w-6 h-6 text-purple-400" />
              Video Prompt
            </span>
            <span className="text-gray-400 text-sm mt-2 block">Describe the animation you want to create</span>
          </label>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Example: Create an animated video explaining the Pythagorean theorem with step-by-step visual proofs..."
            className="w-full min-h-[220px] bg-black/30 glass-border rounded-xl px-6 py-5 text-white placeholder:text-gray-600 text-base leading-relaxed resize-none focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-transparent transition-all"
          />
        </div>

        <div className="glass-border glass-border-hover rounded-2xl p-10 transition-all duration-300">
          <label className="block mb-6">
            <span className="text-white font-semibold text-2xl flex items-center gap-3 tracking-tight">
              <FileText className="w-6 h-6 text-purple-400" />
              Resource Files
            </span>
            <span className="text-gray-400 text-sm mt-2 block">Upload reference materials to enhance your video (optional)</span>
          </label>

          <div
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            className={`border-2 border-dashed rounded-xl p-16 text-center transition-all duration-300 ${
              isDragging
                ? 'border-purple-500/50 bg-purple-500/5 glow-purple'
                : 'border-white/10 bg-black/20 hover:border-white/20'
            }`}
          >
            <UploadCloud className="w-20 h-20 mx-auto mb-6 text-gray-600" />
            <p className="text-gray-400 text-lg mb-3 leading-relaxed">
              Drag & drop your resources (.pdf, .txt), or{' '}
              <label className="text-purple-400 hover:text-purple-300 cursor-pointer font-medium transition-colors">
                browse
                <input
                  type="file"
                  multiple
                  accept=".pdf,.txt"
                  onChange={handleFileSelect}
                  className="hidden"
                />
              </label>
            </p>
            <p className="text-gray-600 text-sm">Supported formats: PDF, TXT</p>
          </div>

          {files.length > 0 && (
            <div className="mt-8 space-y-3">
              <p className="text-gray-400 text-sm font-medium mb-4">{files.length} file(s) uploaded:</p>
              {files.map((file, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between glass-border glass-border-hover rounded-xl px-5 py-4 group transition-all"
                >
                  <span className="text-gray-300 text-sm truncate flex-1">{file.name}</span>
                  <button
                    onClick={() => removeFile(index)}
                    className="text-gray-500 hover:text-red-400 transition-colors ml-4"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="flex justify-center pt-8">
          <button
            onClick={handleGenerate}
            disabled={!prompt.trim()}
            className="relative px-16 py-6 bg-gradient-to-r from-purple-600 to-purple-500 rounded-full font-bold text-xl text-white overflow-hidden transition-all duration-300 hover:scale-[1.02] disabled:opacity-20 disabled:cursor-not-allowed disabled:hover:scale-100 glow-purple glow-purple-hover"
          >
            <span className="relative z-10 flex items-center gap-3">
              <Sparkles className="w-6 h-6" />
              Add to Queue
            </span>
          </button>
        </div>

        {/* Completed Videos Section */}
        {allVideos.length > 0 && (
          <div className="mt-16 space-y-8">
            <div className="text-center space-y-4">
              <h2 className="text-4xl font-bold text-white flex items-center justify-center gap-3">
                <Film className="w-10 h-10 text-purple-400" />
                Recently Completed
              </h2>
              <p className="text-gray-400 text-lg">Click any video to view it in full screen</p>
            </div>

            <div className="grid md:grid-cols-2 gap-8">
              {allVideos.slice(0, 6).map((video) => (
                <div
                  key={video.id}
                  className="glass-border glass-border-hover rounded-2xl overflow-hidden transition-all cursor-pointer group"
                  onClick={() => {
                    setCurrentVideoId(video.videoId);
                    navigateTo('results');
                  }}
                >
                  {/* Video Player */}
                  <div className="aspect-video bg-black relative">
                    <video
                      src={getVideoUrl(video.videoId)}
                      className="w-full h-full object-contain"
                      controls
                      onClick={(e) => e.stopPropagation()}
                    />
                  </div>

                  {/* Video Info */}
                  <div className="p-6 space-y-3">
                    <p className="text-white font-medium line-clamp-2 group-hover:text-purple-400 transition-colors">
                      {video.prompt}
                    </p>
                    <div className="flex items-center gap-2 text-sm text-gray-400">
                      <CheckCircle className="w-4 h-4 text-purple-400" />
                      <span>Rendered successfully</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ==================== HISTORY VIEW ====================
function HistoryView({ navigateTo }: { navigateTo: (view: string) => void }) {
  const [videos, setVideos] = useState<any[]>([]);

  useEffect(() => {
    // TODO: Add database logic here to fetch and set video history for the logged-in user
  }, []);

  return (
    <div className="min-h-screen px-6 py-24 relative overflow-hidden" style={{ backgroundColor: '#080A0F' }}>
      <div className="nebula-purple" style={{ top: '10%', left: '10%' }}></div>

      <div className="max-w-7xl mx-auto space-y-12 relative z-10">
        <div className="text-center space-y-6">
          <h1 className="text-6xl md:text-7xl font-extrabold gradient-text tracking-tight leading-none">History</h1>
          <p className="text-gray-400 text-xl leading-relaxed">Your previously generated videos</p>
        </div>

        {videos.length === 0 ? (
          <div className="glass-border rounded-2xl p-24 text-center">
            <Film className="w-24 h-24 text-gray-700 mx-auto mb-6" />
            <p className="text-gray-400 text-2xl leading-relaxed">Your previously generated videos will appear here.</p>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {videos.map((video, index) => (
              <div key={index} className="glass-border glass-border-hover rounded-2xl p-6 transition-all cursor-pointer">
                <div className="aspect-video glass-border rounded-xl mb-4 flex items-center justify-center">
                  <Film className="w-12 h-12 text-gray-700" />
                </div>
                <p className="text-white font-medium line-clamp-2">{video.prompt}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

// ==================== RESULTS VIEW ====================
function ResultsView({ navigateTo }: { navigateTo: (view: string) => void }) {
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [messages, setMessages] = useState<{ role: 'user' | 'assistant'; content: string }[]>([
    {
      role: 'assistant',
      content: 'Hello! I can answer questions about your generated video and the resources you provided. What would you like to know?',
    },
  ]);
  const [input, setInput] = useState('');
  const scrollRef = useRef<HTMLDivElement>(null);
  const currentVideoId = useStore((state) => state.currentVideoId);
  const [videoUrl, setVideoUrl] = useState('');

  useEffect(() => {
    if (currentVideoId) {
      setVideoUrl(getVideoUrl(currentVideoId));
    }
  }, [currentVideoId]);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || !currentVideoId) return;

    const userMessage = { role: 'user' as const, content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');

    try {
      const response = await sendChatMessage(currentVideoId, input, messages);
      const assistantMessage = {
        role: 'assistant' as const,
        content: response.response
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage = {
        role: 'assistant' as const,
        content: 'Sorry, I encountered an error. Please try again.'
      };
      setMessages(prev => [...prev, errorMessage]);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="h-screen relative overflow-hidden" style={{ backgroundColor: '#080A0F' }}>
      {/* Full-screen Video Container - accounting for navbar */}
      <div className="relative flex items-center justify-center p-8" style={{ height: 'calc(100vh - 73px)' }}>
        <div className="w-full h-full max-h-full glass-border rounded-2xl overflow-hidden flex items-center justify-center bg-black">
          {videoUrl ? (
            <video
              src={videoUrl}
              controls
              autoPlay
              className="w-full h-full"
              style={{ maxHeight: '100%', objectFit: 'contain' }}
            >
              Your browser does not support the video tag.
            </video>
          ) : (
            <div className="text-center space-y-8 p-16">
              <Film className="w-32 h-32 text-gray-700 mx-auto" />
              <p className="text-gray-400 text-3xl leading-relaxed">
                {currentVideoId ? 'Loading video...' : 'Select a video from the queue to view.'}
              </p>
            </div>
          )}
        </div>

        {/* Floating Chat Button */}
        <button
          onClick={() => setIsChatOpen(true)}
          className="fixed bottom-8 right-8 p-5 bg-gradient-to-r from-purple-600 to-purple-500 rounded-full glow-purple glow-purple-hover hover:scale-110 transition-transform z-30"
        >
          <MessageSquare className="w-7 h-7 text-white" />
        </button>
      </div>

      {/* Chat Modal */}
      {isChatOpen && (
        <div className="fixed inset-0 z-40 flex items-center justify-end p-8 pointer-events-none">
          <div className="liquid-glass rounded-2xl w-full max-w-md h-[calc(100vh-4rem)] flex flex-col pointer-events-auto">
            <div className="flex items-center justify-between p-6 border-b border-white/10">
              <div className="flex items-center gap-3">
                <Sparkles className="w-7 h-7 text-purple-400" />
                <h2 className="text-2xl font-bold text-white tracking-tight">Q&A Assistant</h2>
              </div>
              <button
                onClick={() => setIsChatOpen(false)}
                className="p-2 glass-border rounded-lg hover:bg-white/10 transition-colors"
              >
                <X className="w-5 h-5 text-gray-400" />
              </button>
            </div>

            <div 
              ref={scrollRef}
              className="flex-1 overflow-y-auto space-y-4 p-6 scrollbar-thin"
            >
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[85%] rounded-2xl px-6 py-4 ${
                      message.role === 'user'
                        ? 'bg-gradient-to-r from-purple-600 to-purple-500 text-white'
                        : 'glass-border text-gray-300'
                    }`}
                  >
                    <p className="text-base leading-relaxed">{message.content}</p>
                  </div>
                </div>
              ))}
            </div>

            <div className="p-6 border-t border-white/10">
              <div className="flex gap-3">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask a question..."
                  className="flex-1 glass-border rounded-xl px-6 py-4 text-white placeholder:text-gray-600 focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition-all"
                />
                <button
                  onClick={handleSend}
                  disabled={!input.trim()}
                  className="px-7 py-4 bg-gradient-to-r from-purple-600 to-purple-500 rounded-xl font-bold text-white hover:scale-[1.02] transition-transform disabled:opacity-20 disabled:cursor-not-allowed glow-purple glow-purple-hover"
                >
                  <Send className="w-6 h-6" />
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
