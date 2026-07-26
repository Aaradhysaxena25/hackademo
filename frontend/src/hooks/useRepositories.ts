import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { repositoryService, CreateRepoPayload } from '@/services/repositories';

export function useRepositories(params?: { status?: string; search?: string }) {
  return useQuery({
    queryKey: ['repositories', params],
    queryFn: async () => {
      const res = await repositoryService.list(params);
      return res.data;
    },
  });
}

export function useRepository(id: string) {
  return useQuery({
    queryKey: ['repository', id],
    queryFn: async () => {
      const res = await repositoryService.get(id);
      return res.data.data;
    },
    enabled: !!id,
  });
}

export function useCreateRepository() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: CreateRepoPayload) => repositoryService.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['repositories'] });
    },
  });
}

export function useDeleteRepository() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => repositoryService.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['repositories'] });
    },
  });
}

export function useRepositoryFiles(repoId: string, params?: { path?: string; language?: string }) {
  return useQuery({
    queryKey: ['repository-files', repoId, params],
    queryFn: async () => {
      const res = await repositoryService.listFiles(repoId, params);
      return res.data;
    },
    enabled: !!repoId,
  });
}
