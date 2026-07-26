import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { chatService } from '@/services/chat';

export function useConversations(repositoryId?: string) {
  return useQuery({
    queryKey: ['conversations', repositoryId],
    queryFn: async () => {
      const res = await chatService.listConversations(
        repositoryId ? { repository_id: repositoryId } : undefined
      );
      return res.data.data;
    },
  });
}

export function useConversation(id: string) {
  return useQuery({
    queryKey: ['conversation', id],
    queryFn: async () => {
      const res = await chatService.getConversation(id);
      return res.data.data;
    },
    enabled: !!id,
  });
}

export function useCreateConversation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: { repository_id: string; title?: string }) =>
      chatService.createConversation(data.repository_id, data.title),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['conversations'] });
    },
  });
}

export function useSendMessage(conversationId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (content: string) => chatService.sendMessage(conversationId, content),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['conversation', conversationId] });
    },
  });
}
