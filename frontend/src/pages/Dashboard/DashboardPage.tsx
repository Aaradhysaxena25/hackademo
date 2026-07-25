import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { FolderGit2, MessageSquare, Search, FileCode, Plus } from 'lucide-react';
import { Link } from 'react-router-dom';

const stats = [
  { label: 'Repositories', value: '5', icon: FolderGit2, color: 'text-blue-500' },
  { label: 'Conversations', value: '12', icon: MessageSquare, color: 'text-green-500' },
  { label: 'Searches', value: '48', icon: Search, color: 'text-purple-500' },
  { label: 'Code Chunks', value: '2.4K', icon: FileCode, color: 'text-orange-500' },
];

export default function DashboardPage() {
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
        {stats.map((stat) => (
          <Card key={stat.label}>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">{stat.label}</p>
                  <p className="text-2xl font-bold">{stat.value}</p>
                </div>
                <stat.icon className={`h-8 w-8 ${stat.color} opacity-80`} />
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Recent Repos and Activity */}
      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Recent Repositories</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {[
              { name: 'my-project', status: 'ready', lang: 'Python' },
              { name: 'api-service', status: 'ready', lang: 'TypeScript' },
              { name: 'frontend-app', status: 'indexing', lang: 'React' },
            ].map((repo) => (
              <div key={repo.name} className="flex items-center justify-between rounded-md border p-3">
                <div className="flex items-center gap-3">
                  <FolderGit2 className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm font-medium">{repo.name}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs text-muted-foreground">{repo.lang}</span>
                  <Badge variant={repo.status === 'ready' ? 'success' : 'warning'}>
                    {repo.status}
                  </Badge>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Recent Conversations</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {[
              { title: 'How does auth work?', repo: 'my-project', time: '2h ago' },
              { title: 'Find all API endpoints', repo: 'api-service', time: '1d ago' },
              { title: 'Explain database schema', repo: 'my-project', time: '2d ago' },
            ].map((conv) => (
              <div key={conv.title} className="flex items-center justify-between rounded-md border p-3">
                <div>
                  <p className="text-sm font-medium">{conv.title}</p>
                  <p className="text-xs text-muted-foreground">{conv.repo}</p>
                </div>
                <span className="text-xs text-muted-foreground">{conv.time}</span>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
