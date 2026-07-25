export interface Conversation {
  id: string;
  title?: string;
  repository?: { id: string; name: string };
  message_count: number;
  created_at: string;
  updated_at: string;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: SourceReference[];
  token_count: number;
  created_at: string;
}

export interface SourceReference {
  file_path: string;
  start_line: number;
  end_line: number;
  chunk_type: string;
  relevance_score: number;
}
