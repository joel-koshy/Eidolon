'use client';

import { FileText, Loader2 } from 'lucide-react';

interface VideoScriptProps {
  script: string;
  isGenerating: boolean;
}

export default function VideoScript({ script, isGenerating }: VideoScriptProps) {
  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-6 sm:p-8 border border-white/20">
      <div className="flex items-center space-x-3 mb-6">
        <FileText className="h-7 w-7 text-blue-300" />
        <h2 className="text-2xl sm:text-3xl font-bold text-white">Video Script</h2>
      </div>

      {isGenerating && !script ? (
        <div className="flex flex-col items-center justify-center py-16 space-y-6">
          <Loader2 className="h-16 w-16 text-blue-300 animate-spin" />
          <p className="text-white text-xl font-semibold">Generating your video script...</p>
          <p className="text-gray-300 text-base">This may take a moment</p>
        </div>
      ) : (
        <div className="bg-gray-900/60 rounded-xl p-6 sm:p-8 border border-gray-700/50">
          <div className="text-gray-100 whitespace-pre-wrap font-mono text-sm sm:text-base leading-loose max-h-96 overflow-y-auto custom-scrollbar">
            {script || 'Your script will appear here...'}
          </div>
        </div>
      )}
    </div>
  );
}
