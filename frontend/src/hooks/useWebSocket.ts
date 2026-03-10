// React hook for WebSocket connection

import { useEffect, useState, useCallback } from 'react';
import { getWebSocketService } from '@/services/websocket';
import { WSMessage } from '@/types';

export const useWebSocket = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [lastMessage, setLastMessage] = useState<WSMessage | null>(null);
  const ws = getWebSocketService();

  useEffect(() => {
    const connect = async () => {
      try {
        await ws.connect();
        setIsConnected(true);

        // Listen for session initialization
        ws.on('session_initialized', (message: WSMessage) => {
          setSessionId(message.session_id || null);
        });

        // Listen for all messages
        ws.on('*', (message: WSMessage) => {
          setLastMessage(message);
        });
      } catch (error) {
        console.error('Failed to connect:', error);
        setIsConnected(false);
      }
    };

    connect();

    return () => {
      ws.disconnect();
      setIsConnected(false);
    };
  }, []);

  const sendAudioChunk = useCallback((audioData: string, isFinal: boolean = false) => {
    ws.sendAudioChunk(audioData, isFinal);
  }, [ws]);

  const sendVideoFrame = useCallback((frameData: string) => {
    ws.sendVideoFrame(frameData);
  }, [ws]);

  const sendTextInput = useCallback((text: string) => {
    ws.sendTextInput(text);
  }, [ws]);

  const interrupt = useCallback(() => {
    ws.interrupt();
  }, [ws]);

  const on = useCallback((messageType: string, handler: (data: any) => void) => {
    ws.on(messageType, handler);
  }, [ws]);

  const off = useCallback((messageType: string) => {
    ws.off(messageType);
  }, [ws]);

  return {
    isConnected,
    sessionId,
    lastMessage,
    sendAudioChunk,
    sendVideoFrame,
    sendTextInput,
    interrupt,
    on,
    off,
  };
};
