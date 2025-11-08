'use client';

import { useState, useRef, useEffect } from 'react';
import { MessageCircle, Send, Bot, User } from 'lucide-react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatInterfaceProps {
  sessionId: string;
  enabled: boolean;
}

export default function ChatInterface({ sessionId, enabled }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (enabled && messages.length === 0) {
      setMessages([
        {
          role: 'assistant',
          content:
            "Hello! I'm your AI assistant. I can answer questions about the video content, the uploaded resources, and the script. How can I help you?",
          timestamp: new Date(),
        },
      ]);
    }
  }, [enabled]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          sessionId,
          message: input,
        }),
      });

      const data = await response.json();

      const assistantMessage: Message = {
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl border border-white/20 flex flex-col h-[600px] lg:h-[700px]">
      {/* Header */}
      <div className="flex items-center space-x-3 p-5 border-b border-white/30">
        <MessageCircle className="h-7 w-7 text-green-300" />
        <h2 className="text-xl sm:text-2xl font-bold text-white">Ask Questions</h2>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-5 space-y-5 custom-scrollbar">
        {!enabled ? (
          <div className="flex items-center justify-center h-full px-4">
            <p className="text-gray-300 text-center text-base leading-relaxed">
              Chat will be enabled once your video is generated
            </p>
          </div>
        ) : (
          <>
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex items-start gap-3 ${
                  message.role === 'user' ? 'flex-row-reverse' : ''
                }`}
              >
                <div
                  className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center shadow-lg ${
                    message.role === 'user' ? 'bg-blue-600' : 'bg-green-600'
                  }`}
                >
                  {message.role === 'user' ? (
                    <User className="h-5 w-5 text-white" />
                  ) : (
                    <Bot className="h-5 w-5 text-white" />
                  )}
                </div>
                <div
                  className={`flex-1 rounded-xl p-4 shadow-md ${
                    message.role === 'user'
                      ? 'bg-blue-600/90 text-white'
                      : 'bg-gray-700/90 text-gray-100'
                  }`}
                >
                  <p className="text-sm sm:text-base whitespace-pre-wrap leading-relaxed">{message.content}</p>
                  <p className="text-xs mt-2 opacity-70">
                    {message.timestamp.toLocaleTimeString()}
                  </p>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-10 h-10 rounded-full bg-green-600 flex items-center justify-center shadow-lg">
                  <Bot className="h-5 w-5 text-white" />
                </div>
                <div className="flex-1 rounded-xl p-4 bg-gray-700/90 shadow-md">
                  <div className="flex space-x-2">
                    <div className="w-2.5 h-2.5 bg-gray-300 rounded-full animate-bounce"></div>
                    <div className="w-2.5 h-2.5 bg-gray-300 rounded-full animate-bounce delay-75"></div>
                    <div className="w-2.5 h-2.5 bg-gray-300 rounded-full animate-bounce delay-150"></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="p-5 border-t border-white/30">
        <div className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={enabled ? 'Ask a question...' : 'Chat disabled'}
            disabled={!enabled || isLoading}
            className="flex-1 px-4 py-3 bg-white/95 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent text-gray-900 placeholder-gray-500 disabled:opacity-50 disabled:cursor-not-allowed text-base shadow-inner"
          />
          <button
            type="submit"
            disabled={!enabled || !input.trim() || isLoading}
            className="bg-green-600 hover:bg-green-700 text-white p-3 rounded-xl disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-lg"
          >
            <Send className="h-6 w-6" />
          </button>
        </div>
      </form>
    </div>
  );
}
