// Main page - EchoStory App

'use client';

import React, { useState, useEffect } from 'react';
import { LiveCanvas } from '@/components/LiveCanvas';
import { ControlPanel } from '@/components/ControlPanel';
import { CameraOverlay } from '@/components/CameraOverlay';
import { useWebSocket } from '@/hooks/useWebSocket';
import { useAudioRecorder } from '@/hooks/useAudioRecorder';
import { useVideoCapture } from '@/hooks/useVideoCapture';
import { useSpeechSynthesis } from '@/hooks/useSpeechSynthesis';
import { StorySegment, WSMessage } from '@/types';

export default function Home() {
  const [segments, setSegments] = useState<StorySegment[]>([]);
  const [currentText, setCurrentText] = useState<string>('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [emotion, setEmotion] = useState<string>('neutral');
  const [detectedObjects, setDetectedObjects] = useState<string[]>([]);

  // WebSocket connection
  const {
    isConnected,
    sessionId,
    sendAudioChunk,
    sendVideoFrame,
    sendTextInput,
    interrupt,
    on,
  } = useWebSocket();

  // Audio recording
  const { isRecording, startRecording, stopRecording } = useAudioRecorder(sendAudioChunk);

  // Video capture
  const {
    isCapturing,
    startCapture,
    stopCapture,
    videoRef,
    canvasRef,
  } = useVideoCapture(sendVideoFrame);

  // Speech synthesis (AI voice output)
  const {
    speak,
    cancel: cancelSpeech,
    isSpeaking: isAISpeaking,
  } = useSpeechSynthesis({
    rate: 0.9,
    pitch: 1.1,
  });

  // Handle WebSocket messages
  useEffect(() => {
    // Handle audio/text responses
    on('audio_response', (message: WSMessage) => {
      const data = message.data;
      if (data?.text) {
        setCurrentText(data.text);
        // Speak the AI response
        speak(data.text);
        setIsGenerating(false);
      }

      // Handle function calls (illustrations)
      if (data?.function_calls && data.function_calls.length > 0) {
        setIsGenerating(true);
      }
    });

    on('text_response', (message: WSMessage) => {
      const data = message.data;
      if (data?.text) {
        setCurrentText(data.text);
        // Speak the AI response
        speak(data.text);
      }
    });

    // Handle vision detection
    on('vision_detection', (message: WSMessage) => {
      const data = message.data;
      if (data?.objects_detected) {
        setDetectedObjects(data.objects_detected);
      }
    });

    // Handle illustration generation
    on('illustration_generated', (message: WSMessage) => {
      if (message.url) {
        const newSegment: StorySegment = {
          id: Date.now().toString(),
          text: currentText || message.description || '',
          illustration_url: message.url,
          emotion: emotion,
          timestamp: new Date().toISOString(),
        };

        setSegments((prev) => [...prev, newSegment]);
        setCurrentText('');
        setIsGenerating(false);
      }
    });

    // Handle interruption
    on('interrupted', () => {
      setIsGenerating(false);
      setCurrentText('');
      // Also cancel AI speech
      cancelSpeech();
    });

    // Handle errors
    on('error', (message: WSMessage) => {
      console.error('Error:', message.message);
      setIsGenerating(false);
    });
  }, [on, currentText, emotion]);

  // Handle recording state changes
  useEffect(() => {
    if (isRecording) {
      setIsGenerating(true);
    }
  }, [isRecording]);

  return (
    <main className="relative w-full min-h-screen">
      {/* Main Story Canvas */}
      <LiveCanvas
        segments={segments}
        currentText={currentText}
        isGenerating={isGenerating}
        emotion={emotion}
      />

      {/* Camera Overlay */}
      <CameraOverlay
        videoRef={videoRef}
        canvasRef={canvasRef}
        isCapturing={isCapturing}
        detectedObjects={detectedObjects}
      />

      {/* Control Panel */}
      <ControlPanel
        isRecording={isRecording}
        onStartRecording={startRecording}
        onStopRecording={stopRecording}
        isCapturing={isCapturing}
        onStartCapture={startCapture}
        onStopCapture={stopCapture}
        onInterrupt={interrupt}
        isConnected={isConnected}
        isAISpeaking={isAISpeaking}
      />

      {/* Session Info (Debug) */}
      {process.env.NODE_ENV === 'development' && sessionId && (
        <div className="fixed top-4 left-4 bg-black bg-opacity-75 text-white text-xs px-3 py-2 rounded">
          Session: {sessionId.substring(0, 8)}
        </div>
      )}
    </main>
  );
}
