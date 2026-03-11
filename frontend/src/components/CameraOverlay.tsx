// Camera Overlay - Shows live video feed

'use client';

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface CameraOverlayProps {
  videoRef: React.RefObject<HTMLVideoElement>;
  canvasRef: React.RefObject<HTMLCanvasElement>;
  isCapturing: boolean;
  detectedObjects?: string[];
}

export const CameraOverlay: React.FC<CameraOverlayProps> = ({
  videoRef,
  canvasRef,
  isCapturing,
  detectedObjects = [],
}) => {
  return (
    <AnimatePresence>
      {isCapturing && (
        <motion.div
          initial={{ opacity: 0, x: 100 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: 100 }}
          className="fixed top-8 left-8 z-50"
        >
          <div className="bg-white rounded-2xl shadow-2xl overflow-hidden">
            {/* Video Feed */}
            <div className="relative w-64 h-48 bg-gray-900">
              <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                className="w-full h-full object-cover"
                style={{ transform: 'scaleX(-1)' }}
              />

              {/* Detected Objects Overlay */}
              {detectedObjects.length > 0 && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black to-transparent p-3"
                >
                  <div className="flex flex-wrap gap-2">
                    {detectedObjects.map((obj, index) => (
                      <motion.span
                        key={index}
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: index * 0.1 }}
                        className="px-2 py-1 bg-warm-orange text-white text-xs rounded-full"
                      >
                        {obj}
                      </motion.span>
                    ))}
                  </div>
                </motion.div>
              )}

              {/* Recording Indicator */}
              <div className="absolute top-3 right-3">
                <motion.div
                  animate={{ opacity: [1, 0.3, 1] }}
                  transition={{ duration: 1.5, repeat: Infinity }}
                  className="flex items-center space-x-1 bg-red-500 text-white text-xs px-2 py-1 rounded-full"
                >
                  <div className="w-2 h-2 bg-white rounded-full"></div>
                  <span>LIVE</span>
                </motion.div>
              </div>
            </div>

            {/* Label */}
            <div className="px-3 py-2 bg-calm-blue text-white text-sm text-center font-medium">
              👀 I can see your world!
            </div>
          </div>

          {/* Hidden canvas for frame capture */}
          <canvas ref={canvasRef} className="hidden" />
        </motion.div>
      )}
    </AnimatePresence>
  );
};
