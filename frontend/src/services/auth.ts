import api from './api';

export interface LoginPayload {
  email: string;
  password: string;
}

export interface RegisterPayload {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
}

export const authService = {
  login: (data: LoginPayload) => api.post('/accounts/auth/login/', data),
  register: (data: RegisterPayload) => api.post('/accounts/auth/register/', data),
  refresh: (refresh: string) => api.post('/accounts/auth/refresh/', { refresh }),
  logout: (refresh: string) => api.post('/accounts/auth/logout/', { refresh }),
  getProfile: () => api.get('/accounts/profile/'),
  updateProfile: (data: Partial<{ first_name: string; last_name: string }>) =>
    api.patch('/accounts/profile/', data),
  changePassword: (data: { old_password: string; new_password: string }) =>
    api.post('/accounts/auth/password/change/', data),
};
