// Hook for video/camera capture (Live Vision)

import { useState, useRef, useCallback, useEffect } from 'react';

export const useVideoCapture = (onFrameCapture: (data: string) => void, captureInterval: number = 3000) => {
  const [isCapturing, setIsCapturing] = useState(false);
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  const startCapture = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
      }

      // Start capturing frames at intervals
      intervalRef.current = setInterval(() => {
        captureFrame();
      }, captureInterval);

      setIsCapturing(true);
    } catch (error) {
      console.error('Error starting video capture:', error);
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

    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream;
      stream.getTracks().forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }

    setIsCapturing(false);
  }, []);

  useEffect(() => {
    return () => {
      stopCapture();
    };
  }, [stopCapture]);

  return {
    isCapturing,
    startCapture,
    stopCapture,
    videoRef,
    canvasRef,
  };
};
