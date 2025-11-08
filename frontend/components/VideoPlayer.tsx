'use client';

import { Video, Loader2, Download } from 'lucide-react';

interface VideoPlayerProps {
  videoUrl: string;
  isGenerating: boolean;
}

export default function VideoPlayer({ videoUrl, isGenerating }: VideoPlayerProps) {
  const handleDownload = () => {
    if (videoUrl) {
      const link = document.createElement('a');
      link.href = videoUrl;
      link.download = 'manim-video.mp4';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-6 sm:p-8 border border-white/20">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div className="flex items-center space-x-3">
          <Video className="h-7 w-7 text-purple-300" />
          <h2 className="text-2xl sm:text-3xl font-bold text-white">Generated Video</h2>
        </div>
        {videoUrl && (
          <button
            onClick={handleDownload}
            className="flex items-center justify-center space-x-2 bg-purple-600 hover:bg-purple-700 text-white px-5 py-3 rounded-xl transition-colors font-semibold shadow-lg"
          >
            <Download className="h-5 w-5" />
            <span>Download</span>
          </button>
        )}
      </div>

      <div className="relative bg-black rounded-xl overflow-hidden aspect-video shadow-2xl border border-gray-800">
        {isGenerating ? (
          <div className="absolute inset-0 flex flex-col items-center justify-center space-y-6 px-4">
            <Loader2 className="h-20 w-20 text-purple-300 animate-spin" />
            <div className="text-center max-w-md">
              <p className="text-white text-xl font-bold mb-3">Generating Manim Animation</p>
              <p className="text-gray-300 text-base">
                Creating your video with mathematical animations...
              </p>
            </div>
            <div className="w-72 bg-gray-700 rounded-full h-3 overflow-hidden">
              <div className="bg-gradient-to-r from-blue-500 to-purple-600 h-full animate-pulse"></div>
            </div>
          </div>
        ) : videoUrl ? (
          <video
            src={videoUrl}
            controls
            className="w-full h-full"
            controlsList="nodownload"
          >
            Your browser does not support the video tag.
          </video>
        ) : (
          <div className="absolute inset-0 flex items-center justify-center">
            <p className="text-gray-400 text-lg">Your video will appear here...</p>
          </div>
        )}
      </div>

      {videoUrl && (
        <div className="mt-6 p-5 bg-green-500/20 border border-green-500/50 rounded-xl">
          <p className="text-green-200 text-base font-semibold">
            ✓ Video generated successfully! You can now watch and download your video.
          </p>
        </div>
      )}
    </div>
  );
}
