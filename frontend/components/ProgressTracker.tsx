'use client';

import { CheckCircle2, Circle, Loader2 } from 'lucide-react';

interface ProgressTrackerProps {
  currentStage: 'input' | 'script' | 'generating' | 'complete';
}

const stages = [
  { id: 'input', label: 'Input' },
  { id: 'script', label: 'Script' },
  { id: 'generating', label: 'Video' },
  { id: 'complete', label: 'Complete' },
];

export default function ProgressTracker({ currentStage }: ProgressTrackerProps) {
  const getCurrentIndex = () => stages.findIndex((s) => s.id === currentStage);
  const currentIndex = getCurrentIndex();

  return (
    <div className="mb-16 px-4">
      <div className="flex items-center justify-center gap-2 sm:gap-4 max-w-3xl mx-auto">
        {stages.map((stage, index) => {
          const isComplete = index < currentIndex;
          const isCurrent = index === currentIndex;
          const isPending = index > currentIndex;

          return (
            <div key={stage.id} className="flex items-center">
              <div className="flex flex-col items-center min-w-[100px] sm:min-w-[120px]">
                <div
                  className={`flex items-center justify-center w-14 h-14 rounded-full border-3 transition-all shadow-lg ${
                    isComplete
                      ? 'bg-green-500 border-green-400'
                      : isCurrent
                      ? 'bg-blue-500 border-blue-400 animate-pulse'
                      : 'bg-gray-700 border-gray-600'
                  }`}
                >
                  {isComplete ? (
                    <CheckCircle2 className="h-7 w-7 text-white" />
                  ) : isCurrent ? (
                    <Loader2 className="h-7 w-7 text-white animate-spin" />
                  ) : (
                    <Circle className="h-7 w-7 text-gray-400" />
                  )}
                </div>
                <p
                  className={`mt-2 text-xs sm:text-sm font-semibold text-center whitespace-nowrap ${
                    isComplete || isCurrent ? 'text-white' : 'text-gray-400'
                  }`}
                >
                  {stage.label}
                </p>
              </div>
              {index < stages.length - 1 && (
                <div
                  className={`hidden sm:block w-12 h-1 transition-all ${
                    isComplete ? 'bg-green-500' : 'bg-gray-700'
                  }`}
                />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
