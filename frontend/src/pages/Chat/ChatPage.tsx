import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card } from '@/components/ui/card';
import { Send, Bot, User, FileCode, Plus } from 'lucide-react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: { file_path: string; start_line: number; end_line: number; relevance_score: number }[];
}

const mockMessages: Message[] = [
  {
    id: '1',
    role: 'user',
    content: 'How does the authentication middleware work in this project?',
  },
  {
    id: '2',
    role: 'assistant',
    content: `The authentication middleware in this project uses JWT (JSON Web Tokens). Here's how it works:

1. **Token Extraction**: The middleware extracts the Bearer token from the Authorization header.

2. **Token Validation**: It verifies the JWT signature using the secret key and checks expiration.

3. **User Attachment**: If valid, it attaches the user object to the request.

\`\`\`python
# src/middleware/auth.py (lines 15-35)
class JWTAuthMiddleware:
    def __call__(self, request):
        token = self.get_token(request)
        if token:
            payload = jwt.decode(token, settings.SECRET_KEY)
            request.user = User.objects.get(id=payload['user_id'])
        return self.get_response(request)
\`\`\`

The middleware is applied globally in settings.py and runs on every request.`,
    sources: [
      { file_path: 'src/middleware/auth.py', start_line: 15, end_line: 35, relevance_score: 0.94 },
      { file_path: 'src/settings.py', start_line: 42, end_line: 45, relevance_score: 0.82 },
    ],
  },
];

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>(mockMessages);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    // Simulate AI response
    setTimeout(() => {
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `Based on the codebase, here's what I found regarding "${userMessage.content.slice(0, 50)}...":\n\nThis is a mock response. Configure your OpenAI API key to get real AI-powered answers about your repository.`,
        sources: [],
      };
      setMessages((prev) => [...prev, aiMessage]);
      setIsLoading(false);
    }, 1500);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex h-[calc(100vh-7rem)] flex-col">
      {/* Header */}
      <div className="flex items-center justify-between pb-4 border-b">
        <div>
          <h1 className="text-lg font-semibold">AI Chat</h1>
          <p className="text-sm text-muted-foreground">my-project</p>
        </div>
        <Button variant="outline" size="sm"><Plus className="h-3 w-3" /> New Chat</Button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto py-4 space-y-4">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : ''}`}>
            {msg.role === 'assistant' && (
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                <Bot className="h-4 w-4 text-primary" />
              </div>
            )}
            <div className={`max-w-[80%] space-y-2 ${msg.role === 'user' ? 'order-first' : ''}`}>
              <Card className={`p-4 ${msg.role === 'user' ? 'bg-primary text-primary-foreground' : ''}`}>
                <div className="text-sm whitespace-pre-wrap">{msg.content}</div>
              </Card>
              {msg.sources && msg.sources.length > 0 && (
                <div className="flex flex-wrap gap-1">
                  {msg.sources.map((s, i) => (
                    <span key={i} className="inline-flex items-center gap-1 text-xs bg-secondary px-2 py-1 rounded">
                      <FileCode className="h-3 w-3" />
                      {s.file_path}:{s.start_line}-{s.end_line}
                      <span className="text-muted-foreground">({Math.round(s.relevance_score * 100)}%)</span>
                    </span>
                  ))}
                </div>
              )}
            </div>
            {msg.role === 'user' && (
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-secondary flex items-center justify-center">
                <User className="h-4 w-4" />
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="flex gap-3">
            <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
              <Bot className="h-4 w-4 text-primary animate-pulse" />
            </div>
            <Card className="p-4">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-muted-foreground/40 rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-muted-foreground/40 rounded-full animate-bounce [animation-delay:0.1s]" />
                <div className="w-2 h-2 bg-muted-foreground/40 rounded-full animate-bounce [animation-delay:0.2s]" />
              </div>
            </Card>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t pt-4">
        <div className="flex gap-2">
          <Textarea
            placeholder="Ask about your repository... (Enter to send, Shift+Enter for newline)"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            className="min-h-[44px] max-h-[120px] resize-none"
            rows={1}
          />
          <Button onClick={handleSend} disabled={!input.trim() || isLoading} size="icon">
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}
