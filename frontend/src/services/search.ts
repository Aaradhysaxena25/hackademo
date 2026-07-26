import api from './api';

export interface SearchPayload {
  query: string;
  repository_ids: string[];
  filters?: { languages?: string[]; chunk_types?: string[] };
  limit?: number;
}

export const searchService = {
  search: (data: SearchPayload) => api.post('/embeddings/search/', data),
};
