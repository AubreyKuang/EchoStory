// React hook for WebSocket connection

import { useEffect, useState, useCallback, useRef } from 'react';
import { getWebSocketService } from '@/services/websocket';
import { WSMessage } from '@/types';

export const useWebSocket = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [lastMessage, setLastMessage] = useState<WSMessage | null>(null);
  const ws = getWebSocketService();
  const connectingRef = useRef(false);

  useEffect(() => {
    // 防止重复连接
    if (connectingRef.current) {
      console.log('⏭️ Already connecting, skipping...');
      return;
    }

    connectingRef.current = true;

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
        connectingRef.current = false;
      }
    };

    connect();

    return () => {
      console.log('🔌 Cleaning up WebSocket...');
      ws.disconnect();
      setIsConnected(false);
      connectingRef.current = false;
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
