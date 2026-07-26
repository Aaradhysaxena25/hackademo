import { useState, useRef, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Send, Bot, User, FileCode, Plus } from 'lucide-react';
import { useConversation, useConversations, useCreateConversation, useSendMessage } from '@/hooks/useChat';
import { useRepositories } from '@/hooks/useRepositories';
import { streamMessage } from '@/services/chat';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: { file_path: string; start_line: number; end_line: number; relevance_score: number }[];
}

export default function ChatPage() {
  const { conversationId } = useParams();
  const [activeConvId, setActiveConvId] = useState(conversationId || '');
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const { data: conversations } = useConversations();
  const { data: repos } = useRepositories();
  const { data: convDetail } = useConversation(activeConvId);
  const createConv = useCreateConversation();
  const sendMsg = useSendMessage(activeConvId);

  // Load messages when conversation changes
  useEffect(() => {
    if (convDetail?.messages) {
      setMessages(convDetail.messages.map((m: any) => ({
        id: m.id,
        role: m.role,
        content: m.content,
        sources: m.sources || [],
      })));
    }
  }, [convDetail]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleNewChat = async () => {
    const repoList = repos?.results || [];
    if (repoList.length === 0) return;
    try {
      const res = await createConv.mutateAsync({ repository_id: repoList[0].id });
      setActiveConvId(res.data.data.id);
      setMessages([]);
    } catch { /* handled */ }
  };

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;
    if (!activeConvId) {
      // Create a conversation first
      const repoList = repos?.results || [];
      if (repoList.length === 0) return;
      try {
        const res = await createConv.mutateAsync({ repository_id: repoList[0].id });
        setActiveConvId(res.data.data.id);
        // Send message after setting conv
        await sendMessageToConv(res.data.data.id, input.trim());
      } catch { /* handled */ }
      return;
    }
    await sendMessageToConv(activeConvId, input.trim());
  };

  const sendMessageToConv = async (_convId: string, content: string) => {
    const userMsg: Message = { id: Date.now().toString(), role: 'user', content };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    // Use streaming if available
    try {
      const assistantMsgId = (Date.now() + 1).toString();
      setMessages((prev) => [...prev, { id: assistantMsgId, role: 'assistant', content: '', sources: [] }]);

      let fullContent = '';
      let sources: any[] = [];

      for await (const event of streamMessage(activeConvId, content)) {
        if (event.type === 'chunk') {
          fullContent += event.content || '';
          setMessages((prev) =>
            prev.map((m) => m.id === assistantMsgId ? { ...m, content: fullContent } : m)
          );
        } else if (event.type === 'sources') {
          sources = event.sources || [];
          setMessages((prev) =>
            prev.map((m) => m.id === assistantMsgId ? { ...m, sources } : m)
          );
        } else if (event.type === 'done') {
          // Final state already set
        } else if (event.type === 'error') {
          setMessages((prev) =>
            prev.map((m) => m.id === assistantMsgId ? { ...m, content: 'Error: ' + (event.message || 'Something went wrong.') } : m)
          );
        }
      }
    } catch {
      // Fallback to non-streaming
      try {
        const res = await sendMsg.mutateAsync(content);
        const data = res.data.data;
        setMessages((prev) => {
          const filtered = prev.filter(m => m.role === 'user' || m.content !== '');
          return [...filtered.slice(0, -1), {
            id: data.assistant_message.id,
            role: 'assistant' as const,
            content: data.assistant_message.content,
            sources: data.assistant_message.sources || [],
          }];
        });
      } catch {
        setMessages((prev) => [...prev.filter(m => m.content !== ''), {
          id: (Date.now() + 2).toString(),
          role: 'assistant',
          content: 'Sorry, something went wrong. Please try again.',
        }]);
      }
    } finally {
      setIsLoading(false);
    }
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
          <p className="text-sm text-muted-foreground">
            {convDetail?.repository_name || 'Select a repository'}
          </p>
        </div>
        <Button variant="outline" size="sm" onClick={handleNewChat}>
          <Plus className="h-3 w-3" /> New Chat
        </Button>
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* Conversation sidebar */}
        <div className="w-56 border-r pr-3 mr-3 overflow-y-auto hidden md:block">
          <p className="text-xs font-medium text-muted-foreground mb-2 mt-3">Conversations</p>
          {conversations?.map((conv: any) => (
            <button
              key={conv.id}
              onClick={() => setActiveConvId(conv.id)}
              className={`w-full text-left px-2 py-1.5 rounded text-sm truncate mb-1 ${
                activeConvId === conv.id ? 'bg-primary/10 text-primary' : 'hover:bg-accent text-muted-foreground'
              }`}
            >
              {conv.title}
            </button>
          ))}
          {!conversations?.length && (
            <p className="text-xs text-muted-foreground">No conversations yet</p>
          )}
        </div>

        {/* Messages area */}
        <div className="flex-1 flex flex-col overflow-hidden">
          <div className="flex-1 overflow-y-auto py-4 space-y-4">
            {messages.length === 0 && !isLoading && (
              <div className="text-center py-16 text-muted-foreground">
                <Bot className="h-12 w-12 mx-auto mb-4 opacity-20" />
                <p>Ask a question about your codebase</p>
              </div>
            )}
            {messages.map((msg) => (
              <div key={msg.id} className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : ''}`}>
                {msg.role === 'assistant' && (
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                    <Bot className="h-4 w-4 text-primary" />
                  </div>
                )}
                <div className={`max-w-[80%] space-y-2`}>
                  <Card className={`p-4 ${msg.role === 'user' ? 'bg-primary text-primary-foreground' : ''}`}>
                    <div className="text-sm whitespace-pre-wrap">{msg.content}</div>
                  </Card>
                  {msg.sources && msg.sources.length > 0 && (
                    <div className="flex flex-wrap gap-1">
                      {msg.sources.map((s, i) => (
                        <span key={i} className="inline-flex items-center gap-1 text-xs bg-secondary px-2 py-1 rounded">
                          <FileCode className="h-3 w-3" />
                          {s.file_path}:{s.start_line}-{s.end_line}
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
                <Skeleton className="h-16 w-64" />
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="border-t pt-4">
            <div className="flex gap-2">
              <Textarea
                placeholder="Ask about your repository... (Enter to send)"
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
      </div>
    </div>
  );
}
