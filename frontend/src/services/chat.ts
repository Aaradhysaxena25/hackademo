import api from './api';

export const chatService = {
  listConversations: (params?: { repository_id?: string }) =>
    api.get('/chat/conversations/', { params }),

  createConversation: (repository_id: string, title?: string) =>
    api.post('/chat/conversations/', { repository_id, title }),

  getConversation: (id: string) => api.get(`/chat/conversations/${id}/`),

  deleteConversation: (id: string) => api.delete(`/chat/conversations/${id}/`),

  sendMessage: (conversationId: string, content: string) =>
    api.post(`/chat/conversations/${conversationId}/messages/`, { content }),

  listMessages: (conversationId: string) =>
    api.get(`/chat/conversations/${conversationId}/messages/list/`),
};

/**
 * Send a message and receive streaming SSE response.
 * Returns an async generator yielding parsed SSE events.
 */
export async function* streamMessage(
  conversationId: string,
  content: string
): AsyncGenerator<{ type: string; content?: string; sources?: any[]; token_count?: number; message?: string }> {
  const token = localStorage.getItem('access_token');
  const baseUrl = import.meta.env.VITE_API_URL || '/api/v1';

  const response = await fetch(`${baseUrl}/chat/conversations/${conversationId}/messages/stream/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({ content }),
  });

  if (!response.ok) {
    throw new Error(`Stream request failed: ${response.status}`);
  }

  const reader = response.body?.getReader();
  if (!reader) throw new Error('No response body');

  const decoder = new TextDecoder();
  let buffer = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop() || '';

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        try {
          const data = JSON.parse(line.slice(6));
          yield data;
        } catch {
          // Skip malformed JSON
        }
      }
    }
  }
}
