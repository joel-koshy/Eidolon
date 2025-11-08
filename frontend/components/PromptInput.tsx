'use client';

import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, X, FileText, Send } from 'lucide-react';

interface PromptInputProps {
  onSubmit: (prompt: string, resources: File[]) => void;
}

export default function PromptInput({ onSubmit }: PromptInputProps) {
  const [prompt, setPrompt] = useState('');
  const [files, setFiles] = useState<File[]>([]);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFiles((prev) => [...prev, ...acceptedFiles]);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
  });

  const removeFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (prompt.trim()) {
      onSubmit(prompt, files);
    }
  };

  return (
    <div className="w-full max-w-4xl">
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-6 sm:p-8 border border-white/20">
        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Prompt Input */}
          <div>
            <label htmlFor="prompt" className="block text-white text-base sm:text-lg font-bold mb-3">
              What video would you like to create?
            </label>
            <textarea
              id="prompt"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe the educational video you want to create... (e.g., 'Explain the Pythagorean theorem with visual proofs')"
              className="w-full px-5 py-4 bg-white/95 border-2 border-blue-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 placeholder-gray-500 min-h-[140px] resize-y text-base leading-relaxed shadow-inner"
              required
            />
          </div>

          {/* File Upload Area */}
          <div>
            <label className="block text-white text-base sm:text-lg font-bold mb-3">
              Upload Resources (Optional)
            </label>
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-xl py-12 px-8 text-center cursor-pointer transition-all ${
                isDragActive
                  ? 'border-blue-400 bg-blue-500/30 scale-[1.02]'
                  : 'border-white/50 bg-white/5 hover:bg-white/10 hover:border-blue-400'
              }`}
            >
              <input {...getInputProps()} />
              <div className="flex flex-col items-center justify-center space-y-4">
                <Upload className="h-12 w-12 text-blue-300" />
                <div className="space-y-2">
                  <p className="text-white text-lg font-semibold">
                    {isDragActive ? 'Drop files here...' : 'Drag & drop files here'}
                  </p>
                  <p className="text-gray-300 text-sm">
                    or click to browse (PDF, TXT, DOCX)
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* File List */}
          {files.length > 0 && (
            <div className="space-y-3">
              <p className="text-white font-bold text-base">Uploaded Files:</p>
              <div className="space-y-3">
                {files.map((file, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between bg-white/20 rounded-xl p-4 backdrop-blur hover:bg-white/25 transition-colors"
                >
                  <div className="flex items-center space-x-3 flex-1 min-w-0">
                    <FileText className="h-5 w-5 text-blue-300 flex-shrink-0" />
                    <span className="text-white text-sm font-medium truncate">{file.name}</span>
                    <span className="text-gray-300 text-xs flex-shrink-0">
                      ({(file.size / 1024).toFixed(1)} KB)
                    </span>
                  </div>
                  <button
                    type="button"
                    onClick={() => removeFile(index)}
                    className="text-red-300 hover:text-red-500 transition-colors ml-3 flex-shrink-0"
                  >
                    <X className="h-5 w-5" />
                  </button>
                </div>
                ))}
              </div>
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={!prompt.trim()}
            className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold py-5 px-8 rounded-xl hover:from-blue-600 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-[1.02] active:scale-95 flex items-center justify-center space-x-3 shadow-2xl text-lg"
          >
            <Send className="h-6 w-6" />
            <span>Generate Video</span>
          </button>
        </form>
      </div>
    </div>
  );
}
