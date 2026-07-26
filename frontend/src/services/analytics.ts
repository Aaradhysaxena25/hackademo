import api from './api';

export const analyticsService = {
  getDashboardStats: () => api.get('/analytics/dashboard/'),
  getRepositoryAnalytics: (repoId: string) => api.get(`/analytics/repositories/${repoId}/`),
  getUsageStats: (days?: number) => api.get('/analytics/usage/', { params: { days } }),
  getActivity: () => api.get('/analytics/activity/'),
};
