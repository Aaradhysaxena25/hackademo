import api from './api';

export interface CreateRepoPayload {
  name: string;
  description?: string;
  source_type: 'upload' | 'github';
  github_url?: string;
}

export const repositoryService = {
  list: (params?: { status?: string; search?: string; page?: number }) =>
    api.get('/repositories/', { params }),

  get: (id: string) => api.get(`/repositories/${id}/`),

  create: (data: CreateRepoPayload) => api.post('/repositories/', data),

  update: (id: string, data: { name?: string; description?: string }) =>
    api.patch(`/repositories/${id}/`, data),

  delete: (id: string) => api.delete(`/repositories/${id}/`),

  reindex: (id: string) => api.post(`/repositories/${id}/reindex/`),

  listFiles: (id: string, params?: { path?: string; language?: string; search?: string }) =>
    api.get(`/repositories/${id}/files/`, { params }),

  upload: (name: string, file: File, description?: string) => {
    const formData = new FormData();
    formData.append('name', name);
    formData.append('source_type', 'upload');
    formData.append('file', file);
    if (description) formData.append('description', description);
    return api.post('/repositories/upload/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};
