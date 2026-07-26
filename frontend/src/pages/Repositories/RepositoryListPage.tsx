import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { FolderGit2, Plus, Search, Upload, Github } from 'lucide-react';
import { useRepositories, useCreateRepository } from '@/hooks/useRepositories';

export default function RepositoryListPage() {
  const [search, setSearch] = useState('');
  const [showCreate, setShowCreate] = useState(false);
  const [newRepoName, setNewRepoName] = useState('');

  const { data, isLoading } = useRepositories({ search: search || undefined });
  const createMutation = useCreateRepository();

  const repos = data?.results || [];

  const handleCreate = async () => {
    if (!newRepoName.trim()) return;
    try {
      await createMutation.mutateAsync({
        name: newRepoName.trim(),
        source_type: 'upload',
      });
      setNewRepoName('');
      setShowCreate(false);
    } catch {
      // Error handled by React Query
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Repositories</h1>
        <Button onClick={() => setShowCreate(!showCreate)}>
          <Plus className="h-4 w-4" /> Import
        </Button>
      </div>

      {/* Quick Create */}
      {showCreate && (
        <Card>
          <CardContent className="p-4">
            <p className="text-sm font-medium mb-3">Create a new repository</p>
            <div className="flex gap-2">
              <Input
                placeholder="Repository name"
                value={newRepoName}
                onChange={(e) => setNewRepoName(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleCreate()}
              />
              <Button onClick={handleCreate} disabled={createMutation.isPending}>
                {createMutation.isPending ? 'Creating...' : 'Create'}
              </Button>
            </div>
            {createMutation.isError && (
              <p className="text-sm text-destructive mt-2">Failed to create repository.</p>
            )}
          </CardContent>
        </Card>
      )}

      {/* Search */}
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
      {isLoading ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <Card key={i}><CardContent className="p-5"><Skeleton className="h-24 w-full" /></CardContent></Card>
          ))}
        </div>
      ) : repos.length > 0 ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {repos.map((repo: any) => (
            <Link key={repo.id} to={`/app/repositories/${repo.id}`}>
              <Card className="hover:border-primary/50 transition-colors cursor-pointer h-full">
                <CardContent className="p-5 space-y-3">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-2">
                      <FolderGit2 className="h-5 w-5 text-primary" />
                      <h3 className="font-semibold">{repo.name}</h3>
                    </div>
                    <Badge variant={repo.status === 'ready' ? 'success' : repo.status === 'indexing' ? 'warning' : 'secondary'}>
                      {repo.status}
                    </Badge>
                  </div>
                  {repo.description && (
                    <p className="text-sm text-muted-foreground line-clamp-2">{repo.description}</p>
                  )}
                  <div className="flex items-center justify-between text-xs text-muted-foreground">
                    <div className="flex items-center gap-1">
                      {repo.source_type === 'github' ? <Github className="h-3 w-3" /> : <Upload className="h-3 w-3" />}
                      <span>{repo.source_type}</span>
                    </div>
                    <span>{repo.total_files} files</span>
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      ) : (
        <div className="text-center py-16 text-muted-foreground">
          <FolderGit2 className="h-12 w-12 mx-auto mb-4 opacity-20" />
          <p>No repositories found</p>
          <p className="text-sm mt-1">Import a repository to get started</p>
        </div>
      )}
    </div>
  );
}
