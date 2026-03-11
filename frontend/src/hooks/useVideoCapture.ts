// Hook for video/camera capture (Live Vision)

import { useState, useRef, useCallback, useEffect } from 'react';

export const useVideoCapture = (onFrameCapture: (data: string) => void, captureInterval: number = 3000) => {
  const [isCapturing, setIsCapturing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  const startCapture = useCallback(async () => {
    try {
      setError(null);
      console.log('📹 Requesting camera permission...');
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      console.log('✅ Camera permission granted');

      // 保存stream到ref
      streamRef.current = stream;

      // 设置状态为true，触发video元素渲染
      setIsCapturing(true);
    } catch (error: any) {
      console.error('❌ Error starting video capture:', error);
      const errorMsg = error.name === 'NotAllowedError'
        ? 'Camera permission denied. Please allow camera access in your browser settings.'
        : error.name === 'NotFoundError'
        ? 'No camera found. Please connect a camera.'
        : `Error: ${error.message}`;
      setError(errorMsg);
      alert(errorMsg);
    }
  }, [captureInterval]);

  const captureFrame = useCallback(() => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');

    if (!context) return;

    // Set canvas size to video size
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw video frame to canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert to base64
    const base64 = canvas.toDataURL('image/jpeg', 0.8).split(',')[1];
    onFrameCapture(base64);
  }, [onFrameCapture]);

  const stopCapture = useCallback(() => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }

    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }

    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }

    setIsCapturing(false);
  }, []);

  // 当isCapturing变为true且有stream时，连接video元素
  useEffect(() => {
    if (isCapturing && streamRef.current && videoRef.current) {
      console.log('✅ Video element found, setting stream...');
      videoRef.current.srcObject = streamRef.current;

      videoRef.current.onloadedmetadata = () => {
        console.log('✅ Video metadata loaded');
        videoRef.current?.play().then(() => {
          console.log('✅ Video playing');
        }).catch(err => {
          console.error('❌ Error playing video:', err);
        });
      };

      // Start capturing frames at intervals
      intervalRef.current = setInterval(() => {
        captureFrame();
      }, captureInterval);
    }
  }, [isCapturing, captureFrame, captureInterval]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  return {
    isCapturing,
    startCapture,
    stopCapture,
    videoRef,
    canvasRef,
    error,
  };
};
