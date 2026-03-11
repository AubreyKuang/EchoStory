// EchoStory Logo Component

'use client';

import React from 'react';
import { motion } from 'framer-motion';

export const Logo: React.FC = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="fixed top-4 left-4 z-50 flex items-center space-x-2 bg-white bg-opacity-90 px-4 py-2 rounded-full shadow-lg"
    >
      {/* Icon */}
      <div className="flex items-center justify-center w-8 h-8 bg-gradient-to-br from-warm-orange to-light-purple rounded-full">
        <span className="text-white text-xl">✨</span>
      </div>

      {/* Text */}
      <div className="flex flex-col">
        <span className="text-lg font-bold text-gray-800 leading-none">
          EchoStory
        </span>
      </div>
    </motion.div>
  );
};
