import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { FolderGit2, Plus, Search, Upload, Github } from 'lucide-react';

const mockRepos = [
  { id: '1', name: 'my-project', description: 'A Python web app', source_type: 'upload', status: 'ready', total_files: 342, languages: { Python: 65, JavaScript: 25 }, created_at: '2024-01-15' },
  { id: '2', name: 'api-service', description: 'REST API service', source_type: 'github', status: 'ready', total_files: 128, languages: { TypeScript: 80, YAML: 20 }, created_at: '2024-01-10' },
  { id: '3', name: 'frontend-app', description: 'React frontend', source_type: 'github', status: 'indexing', total_files: 256, languages: { TypeScript: 70, CSS: 30 }, created_at: '2024-01-05' },
];

export default function RepositoryListPage() {
  const [search, setSearch] = useState('');

  const filtered = mockRepos.filter(r =>
    r.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Repositories</h1>
        <Button><Plus className="h-4 w-4" /> Import</Button>
      </div>

      {/* Search & Filters */}
      <div className="flex gap-3">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search repositories..."
            className="pl-9"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>

      {/* Repository Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {filtered.map((repo) => (
          <Link key={repo.id} to={`/app/repositories/${repo.id}`}>
            <Card className="hover:border-primary/50 transition-colors cursor-pointer h-full">
              <CardContent className="p-5 space-y-3">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-2">
                    <FolderGit2 className="h-5 w-5 text-primary" />
                    <h3 className="font-semibold">{repo.name}</h3>
                  </div>
                  <Badge variant={repo.status === 'ready' ? 'success' : 'warning'}>
                    {repo.status}
                  </Badge>
                </div>
                <p className="text-sm text-muted-foreground line-clamp-2">{repo.description}</p>
                <div className="flex items-center justify-between text-xs text-muted-foreground">
                  <div className="flex items-center gap-1">
                    {repo.source_type === 'github' ? <Github className="h-3 w-3" /> : <Upload className="h-3 w-3" />}
                    <span>{repo.source_type}</span>
                  </div>
                  <span>{repo.total_files} files</span>
                </div>
                <div className="flex gap-1 flex-wrap">
                  {Object.entries(repo.languages).map(([lang, pct]) => (
                    <span key={lang} className="text-xs bg-secondary px-2 py-0.5 rounded">
                      {lang} {pct}%
                    </span>
                  ))}
                </div>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
