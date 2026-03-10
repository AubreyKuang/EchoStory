// Type definitions for EchoStory

export interface StorySegment {
  id: string;
  text: string;
  illustration_url?: string;
  emotion?: 'happy' | 'excited' | 'calm' | 'worried' | 'sad' | 'neutral';
  timestamp: string;
}

export interface Session {
  id: string;
  created_at: string;
  story_segments: StorySegment[];
  status: 'active' | 'completed' | 'archived';
}

export interface WSMessage {
  type: 'session_initialized' | 'audio_response' | 'text_response' |
        'vision_detection' | 'illustration_generated' | 'segment_saved' |
        'interrupted' | 'error';
  data?: any;
  message?: string;
  session_id?: string;
  url?: string;
  description?: string;
}

export interface VisionDetection {
  objects_detected: string[];
  description: string;
}

export interface AudioResponseData {
  text: string;
  function_calls: FunctionCall[];
  is_complete: boolean;
}

export interface FunctionCall {
  name: string;
  args: Record<string, any>;
}
