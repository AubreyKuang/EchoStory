// Live Canvas - The interactive storybook display

'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { StorySegment } from '@/types';

interface LiveCanvasProps {
  segments: StorySegment[];
  currentText?: string;
  isGenerating: boolean;
  emotion?: string;
}

export const LiveCanvas: React.FC<LiveCanvasProps> = ({
  segments,
  currentText,
  isGenerating,
  emotion = 'neutral',
}) => {
  const [backgroundGradient, setBackgroundGradient] = useState('from-calm-blue to-soft-green');

  // Update background based on emotion
  useEffect(() => {
    const emotionGradients: Record<string, string> = {
      happy: 'from-gentle-yellow to-warm-orange',
      excited: 'from-warm-orange to-light-purple',
      calm: 'from-calm-blue to-soft-green',
      worried: 'from-soft-green to-calm-blue',
      sad: 'from-calm-blue to-light-purple',
      neutral: 'from-calm-blue to-soft-green',
    };

    setBackgroundGradient(emotionGradients[emotion] || emotionGradients.neutral);
  }, [emotion]);

  const latestSegment = segments.length > 0 ? segments[segments.length - 1] : null;

  return (
    <div className={`relative w-full h-full min-h-screen bg-gradient-to-br ${backgroundGradient} transition-all duration-1000 overflow-hidden`}>
      {/* Main Story Display */}
      <div className="container mx-auto px-8 py-12 flex flex-col items-center justify-center min-h-screen">
        <AnimatePresence mode="wait">
          {latestSegment && (
            <motion.div
              key={latestSegment.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.6 }}
              className="w-full max-w-4xl"
            >
              {/* Illustration */}
              {latestSegment.illustration_url && (
                <motion.div
                  initial={{ scale: 0.9, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ delay: 0.2, duration: 0.5 }}
                  className="mb-8 rounded-3xl overflow-hidden shadow-2xl"
                >
                  <img
                    src={latestSegment.illustration_url}
                    alt="Story illustration"
                    className="w-full h-auto"
                  />
                </motion.div>
              )}

              {/* Story Text */}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.4 }}
                className="bg-white bg-opacity-90 rounded-2xl p-8 shadow-xl"
              >
                <p className="text-3xl font-medium text-gray-800 leading-relaxed text-center">
                  {latestSegment.text}
                </p>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Current AI Speech */}
        {currentText && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="fixed bottom-40 left-0 right-0 mx-auto max-w-3xl px-8"
          >
            <div className="bg-white bg-opacity-95 rounded-2xl p-6 shadow-lg">
              <p className="text-xl text-gray-700 text-center">
                {currentText}
              </p>
            </div>
          </motion.div>
        )}

        {/* Loading Indicator */}
        {isGenerating && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="fixed top-8 right-8"
          >
            <div className="flex items-center space-x-2 bg-white bg-opacity-90 rounded-full px-4 py-2 shadow-md">
              <div className="w-3 h-3 bg-warm-orange rounded-full animate-pulse-soft"></div>
              <span className="text-sm text-gray-600">Creating magic...</span>
            </div>
          </motion.div>
        )}
      </div>

      {/* Story Progress Indicators */}
      {segments.length > 0 && (
        <div className="fixed bottom-8 left-0 right-0 flex justify-center space-x-2">
          {segments.map((segment, index) => (
            <motion.div
              key={segment.id}
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: index * 0.1 }}
              className={`w-3 h-3 rounded-full ${
                index === segments.length - 1 ? 'bg-warm-orange' : 'bg-white bg-opacity-50'
              }`}
            />
          ))}
        </div>
      )}

      {/* Empty State */}
      {segments.length === 0 && !currentText && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="absolute inset-0 flex items-center justify-center"
        >
          <div className="text-center">
            <motion.div
              animate={{ scale: [1, 1.1, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
              className="text-6xl mb-4"
            >
              ✨
            </motion.div>
            <h2 className="text-3xl font-medium text-white mb-2">
              Ready to tell your story?
            </h2>
            <p className="text-xl text-white text-opacity-90">
              Press the button and start talking
            </p>
          </div>
        </motion.div>
      )}
    </div>
  );
};
