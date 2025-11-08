'use client';

import { useState } from 'react';
import PromptInput from '@/components/PromptInput';
import VideoScript from '@/components/VideoScript';
import VideoPlayer from '@/components/VideoPlayer';
import ChatInterface from '@/components/ChatInterface';
import ProgressTracker from '@/components/ProgressTracker';

export default function Home() {
  const [stage, setStage] = useState<'input' | 'script' | 'generating' | 'complete'>('input');
  const [prompt, setPrompt] = useState('');
  const [resources, setResources] = useState<File[]>([]);
  const [script, setScript] = useState('');
  const [videoUrl, setVideoUrl] = useState('');
  const [sessionId, setSessionId] = useState('');

  const handleSubmitPrompt = async (userPrompt: string, userResources: File[]) => {
    setPrompt(userPrompt);
    setResources(userResources);
    setStage('script');
    
    // Upload resources and send prompt to backend
    const formData = new FormData();
    formData.append('prompt', userPrompt);
    userResources.forEach((file) => {
      formData.append('resources', file);
    });

    try {
      const response = await fetch('/api/generate-script', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      setSessionId(data.sessionId);
      setScript(data.script);
      setStage('generating');

      // Start polling for video generation status
      pollVideoStatus(data.sessionId);
    } catch (error) {
      console.error('Error generating script:', error);
    }
  };

  const pollVideoStatus = async (id: string) => {
    const interval = setInterval(async () => {
      try {
        const response = await fetch(`/api/video-status/${id}`);
        const data = await response.json();

        if (data.status === 'completed') {
          setVideoUrl(data.videoUrl);
          setStage('complete');
          clearInterval(interval);
        } else if (data.status === 'error') {
          console.error('Video generation error:', data.error);
          clearInterval(interval);
        }
      } catch (error) {
        console.error('Error polling video status:', error);
      }
    }, 3000);
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 py-8">
      <div className="container mx-auto px-4 sm:px-6 max-w-7xl">
        <header className="text-center mb-12">
          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-white mb-4 drop-shadow-2xl">
            Eidolon Video Generator
          </h1>
          <p className="text-base sm:text-lg text-gray-100 max-w-2xl mx-auto leading-relaxed">
            Transform your ideas into educational videos with AI-powered Manim animations
          </p>
        </header>

        <ProgressTracker currentStage={stage} />

        {stage === 'input' && (
          <div className="flex justify-center">
            <PromptInput onSubmit={handleSubmitPrompt} />
          </div>
        )}

        {(stage === 'script' || stage === 'generating' || stage === 'complete') && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mt-8">
            <div className="lg:col-span-2 space-y-8">
              <VideoScript script={script} isGenerating={stage === 'script'} />
              
              {(stage === 'generating' || stage === 'complete') && (
                <VideoPlayer 
                  videoUrl={videoUrl} 
                  isGenerating={stage === 'generating'} 
                />
              )}
            </div>

            <div className="lg:col-span-1">
              <ChatInterface 
                sessionId={sessionId}
                enabled={stage === 'complete'}
              />
            </div>
          </div>
        )}
      </div>
    </main>
  );
}