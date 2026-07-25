export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  profile: UserProfile;
  github_connected: boolean;
  github_username?: string;
  created_at: string;
}

export interface UserProfile {
  avatar_url?: string;
  bio?: string;
  company?: string;
  location?: string;
  preferred_llm: string;
  settings: Record<string, unknown>;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
}

export interface AuthResponse {
  access: string;
  refresh: string;
  user: User;
}
