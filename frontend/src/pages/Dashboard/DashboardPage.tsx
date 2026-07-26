import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { FolderGit2, MessageSquare, Search, FileCode, Plus } from 'lucide-react';
import { Link } from 'react-router-dom';
import { analyticsService } from '@/services/analytics';
import { repositoryService } from '@/services/repositories';

export default function DashboardPage() {
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: async () => {
      const res = await analyticsService.getDashboardStats();
      return res.data.data;
    },
  });

  const { data: reposData, isLoading: reposLoading } = useQuery({
    queryKey: ['repositories'],
    queryFn: async () => {
      const res = await repositoryService.list();
      return res.data;
    },
  });

  const statCards = [
    { label: 'Repositories', value: stats?.total_repositories ?? 0, icon: FolderGit2, color: 'text-blue-500' },
    { label: 'Conversations', value: stats?.total_conversations ?? 0, icon: MessageSquare, color: 'text-green-500' },
    { label: 'Searches', value: stats?.total_searches ?? 0, icon: Search, color: 'text-purple-500' },
    { label: 'Code Chunks', value: stats?.total_chunks ?? 0, icon: FileCode, color: 'text-orange-500' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Dashboard</h1>
          <p className="text-muted-foreground">Welcome back to CodePilot AI</p>
        </div>
        <Link to="/app/repositories">
          <Button><Plus className="h-4 w-4" /> Import Repository</Button>
        </Link>
      </div>

      {/* Stats */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {statCards.map((stat) => (
          <Card key={stat.label}>
            <CardContent className="p-6">
              {statsLoading ? (
                <Skeleton className="h-12 w-full" />
              ) : (
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground">{stat.label}</p>
                    <p className="text-2xl font-bold">{stat.value}</p>
                  </div>
                  <stat.icon className={`h-8 w-8 ${stat.color} opacity-80`} />
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Repositories */}
      <Card>
        <CardHeader>
          <CardTitle>Your Repositories</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {reposLoading ? (
            <>
              <Skeleton className="h-14 w-full" />
              <Skeleton className="h-14 w-full" />
            </>
          ) : reposData?.results?.length > 0 ? (
            reposData.results.slice(0, 5).map((repo: any) => (
              <Link
                key={repo.id}
                to={`/app/repositories/${repo.id}`}
                className="flex items-center justify-between rounded-md border p-3 hover:bg-accent transition-colors"
              >
                <div className="flex items-center gap-3">
                  <FolderGit2 className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm font-medium">{repo.name}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs text-muted-foreground">{repo.total_files} files</span>
                  <Badge variant={repo.status === 'ready' ? 'success' : repo.status === 'indexing' ? 'warning' : 'secondary'}>
                    {repo.status}
                  </Badge>
                </div>
              </Link>
            ))
          ) : (
            <div className="text-center py-8 text-muted-foreground">
              <FolderGit2 className="h-10 w-10 mx-auto mb-2 opacity-30" />
              <p>No repositories yet</p>
              <Link to="/app/repositories" className="text-primary text-sm hover:underline">Import your first repository</Link>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
