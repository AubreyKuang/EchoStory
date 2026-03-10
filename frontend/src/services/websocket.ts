// WebSocket service for real-time communication with backend

import { WSMessage } from '@/types';

export class WebSocketService {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private messageHandlers: Map<string, (data: any) => void> = new Map();
  private sessionId: string | null = null;

  constructor(private url: string) {}

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        this.ws = new WebSocket(this.url);

        this.ws.onopen = () => {
          console.log('WebSocket connected');
          this.reconnectAttempts = 0;
          resolve();
        };

        this.ws.onmessage = (event) => {
          this.handleMessage(event.data);
        };

        this.ws.onerror = (error) => {
          console.error('WebSocket error:', error);
          reject(error);
        };

        this.ws.onclose = () => {
          console.log('WebSocket disconnected');
          this.attemptReconnect();
        };
      } catch (error) {
        reject(error);
      }
    });
  }

  private handleMessage(data: string) {
    try {
      const message: WSMessage = JSON.parse(data);
      console.log('Received message:', message);

      // Store session ID if provided
      if (message.session_id) {
        this.sessionId = message.session_id;
      }

      // Call registered handlers
      const handler = this.messageHandlers.get(message.type);
      if (handler) {
        handler(message);
      }

      // Call wildcard handler
      const wildcardHandler = this.messageHandlers.get('*');
      if (wildcardHandler) {
        wildcardHandler(message);
      }
    } catch (error) {
      console.error('Error parsing message:', error);
    }
  }

  private attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`Reconnecting... Attempt ${this.reconnectAttempts}`);

      setTimeout(() => {
        this.connect().catch(console.error);
      }, this.reconnectDelay * this.reconnectAttempts);
    }
  }

  on(messageType: string, handler: (data: any) => void) {
    this.messageHandlers.set(messageType, handler);
  }

  off(messageType: string) {
    this.messageHandlers.delete(messageType);
  }

  send(message: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    } else {
      console.error('WebSocket is not connected');
    }
  }

  sendAudioChunk(audioData: string, isFinal: boolean = false) {
    this.send({
      type: 'audio_chunk',
      data: audioData,
      is_final: isFinal,
    });
  }

  sendVideoFrame(frameData: string) {
    this.send({
      type: 'video_frame',
      data: frameData,
    });
  }

  sendTextInput(text: string) {
    this.send({
      type: 'text_input',
      text,
    });
  }

  interrupt() {
    this.send({
      type: 'interrupt',
    });
  }

  generateIllustration(description: string, sceneType?: string) {
    this.send({
      type: 'generate_illustration',
      description,
      scene_type: sceneType,
    });
  }

  saveSegment(segment: any) {
    this.send({
      type: 'save_segment',
      segment,
    });
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  getSessionId(): string | null {
    return this.sessionId;
  }

  isConnected(): boolean {
    return this.ws !== null && this.ws.readyState === WebSocket.OPEN;
  }
}

// Singleton instance
let wsInstance: WebSocketService | null = null;

export const getWebSocketService = (): WebSocketService => {
  if (!wsInstance) {
    const wsUrl = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000/ws/story';
    wsInstance = new WebSocketService(wsUrl);
  }
  return wsInstance;
};
