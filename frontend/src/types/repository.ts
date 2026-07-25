export type RepoStatus = 'pending' | 'indexing' | 'ready' | 'failed';

export interface Repository {
  id: string;
  name: string;
  description?: string;
  source_type: 'github' | 'upload';
  github_url?: string;
  default_branch: string;
  status: RepoStatus;
  total_files: number;
  total_chunks: number;
  total_size_bytes: number;
  languages: Record<string, number>;
  last_indexed_at?: string;
  created_at: string;
  updated_at: string;
}

export interface RepositoryFile {
  id: string;
  file_path: string;
  file_name: string;
  language?: string;
  size_bytes: number;
  line_count: number;
}
