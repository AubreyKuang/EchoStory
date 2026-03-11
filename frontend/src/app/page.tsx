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
    rate: 0.95, // 稍微加快，更接近正常语速
    pitch: 1.05, // 稍微降低音调，更自然
    volume: 0.9,
  });

  // Handle WebSocket messages
  useEffect(() => {
    // Handle audio/text responses
    on('audio_response', (message: WSMessage) => {
      const data = message.data;
      console.log('📥 Audio response:', data);

      if (data?.text && data.text.trim()) {
        // Handle function calls (illustrations)
        if (data?.function_calls && data.function_calls.length > 0) {
          console.log('🎨 Function calls detected, creating segment with pending image...');
          setIsGenerating(true);

          // 立即创建segment（文字先显示，图片pending）
          const pendingSegment: StorySegment = {
            id: Date.now().toString(),
            text: data.text,
            emotion: emotion,
            timestamp: new Date().toISOString(),
            // illustration_url will be added later
          };
          setSegments((prev) => [...prev, pendingSegment]);
          setCurrentText(''); // 清空临时文字

          // 开始播放语音（和文字显示同步）
          setTimeout(() => speak(data.text), 200); // 与文字动画同步
        } else {
          // 没有图片生成，创建纯文字segment
          const textSegment: StorySegment = {
            id: Date.now().toString(),
            text: data.text,
            emotion: emotion,
            timestamp: new Date().toISOString(),
          };
          setSegments((prev) => [...prev, textSegment]);
          setCurrentText('');
          setIsGenerating(false);

          // 开始播放语音
          setTimeout(() => speak(data.text), 200);
        }
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
      console.log('🎨 Received illustration:', message);
      if (message.url) {
        // 更新最新的segment，添加图片URL
        setSegments((prev) => {
          if (prev.length === 0) return prev;

          const updated = [...prev];
          const lastSegment = updated[updated.length - 1];

          // 如果最后一个segment还没有图片，添加图片
          if (!lastSegment.illustration_url) {
            updated[updated.length - 1] = {
              ...lastSegment,
              illustration_url: message.url,
            };
            console.log('✅ Updated segment with image');
          } else {
            // 如果已经有图片了，创建新的segment
            console.log('⚠️ Last segment already has image, creating new one');
            updated.push({
              id: Date.now().toString(),
              text: message.description || 'A beautiful story scene',
              illustration_url: message.url,
              emotion: emotion,
              timestamp: new Date().toISOString(),
            });
          }

          return updated;
        });

        setIsGenerating(false);
      } else {
        console.error('❌ No URL in illustration message');
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
