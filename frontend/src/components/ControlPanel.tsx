// Control Panel - Voice and vision controls

'use client';

import React from 'react';
import { motion } from 'framer-motion';

interface ControlPanelProps {
  isRecording: boolean;
  onStartRecording: () => void;
  onStopRecording: () => void;
  isCapturing: boolean;
  onStartCapture: () => void;
  onStopCapture: () => void;
  onInterrupt: () => void;
  isConnected: boolean;
  isAISpeaking?: boolean;
}

export const ControlPanel: React.FC<ControlPanelProps> = ({
  isRecording,
  onStartRecording,
  onStopRecording,
  isCapturing,
  onStartCapture,
  onStopCapture,
  onInterrupt,
  isConnected,
  isAISpeaking = false,
}) => {
  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white bg-opacity-95 shadow-2xl">
      <div className="container mx-auto px-8 py-6">
        <div className="flex items-center justify-center space-x-6">
          {/* Voice Recording Button */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={isRecording ? onStopRecording : onStartRecording}
            disabled={!isConnected}
            className={`
              relative w-20 h-20 rounded-full shadow-lg transition-all
              ${isRecording
                ? 'bg-red-500 hover:bg-red-600'
                : 'bg-warm-orange hover:bg-orange-400'
              }
              ${!isConnected ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
            `}
          >
            {isRecording ? (
              <motion.div
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 1, repeat: Infinity }}
                className="absolute inset-0 flex items-center justify-center"
              >
                <div className="w-6 h-6 bg-white rounded-sm"></div>
              </motion.div>
            ) : (
              <div className="absolute inset-0 flex items-center justify-center">
                <svg className="w-10 h-10 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
                  <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
                </svg>
              </div>
            )}
          </motion.button>

          {/* Interrupt Button */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={onInterrupt}
            disabled={!isConnected}
            className={`
              px-6 py-3 rounded-full font-medium shadow-md transition-all
              bg-light-purple hover:bg-purple-300 text-purple-900
              ${!isConnected ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
            `}
          >
            ⏸️ Wait!
          </motion.button>

          {/* Camera Toggle Button */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={isCapturing ? onStopCapture : onStartCapture}
            disabled={!isConnected}
            className={`
              w-20 h-20 rounded-full shadow-lg transition-all
              ${isCapturing
                ? 'bg-soft-green'
                : 'bg-calm-blue hover:bg-blue-300'
              }
              ${!isConnected ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
            `}
          >
            <div className="absolute inset-0 flex items-center justify-center">
              <svg className="w-10 h-10 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4z"/>
              </svg>
            </div>
            {isCapturing && (
              <motion.div
                animate={{ opacity: [1, 0.5, 1] }}
                transition={{ duration: 1.5, repeat: Infinity }}
                className="absolute top-2 right-2 w-3 h-3 bg-red-500 rounded-full"
              ></motion.div>
            )}
          </motion.button>

          {/* Connection Status */}
          <div className="absolute right-8 flex items-center space-x-2">
            <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
            <span className="text-sm text-gray-600">
              {isConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>
        </div>

        {/* Instructions */}
        <div className="mt-4 text-center">
          <p className="text-sm text-gray-500">
            {isRecording
              ? '🎤 Listening... Tell me about your day!'
              : isAISpeaking
              ? '🔊 AI is speaking... (Press "Wait!" to interrupt)'
              : '👆 Press the orange button to start talking'
            }
          </p>
        </div>
      </div>
    </div>
  );
};
