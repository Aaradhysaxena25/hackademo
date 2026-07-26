import { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Search, FileCode, Code } from 'lucide-react';
import { searchService } from '@/services/search';
import { useRepositories } from '@/hooks/useRepositories';

interface SearchResult {
  chunk_id: string;
  file_path: string;
  symbol_name: string | null;
  chunk_type: string;
  content: string;
  language: string;
  start_line: number;
  end_line: number;
  relevance_score: number;
}

export default function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [queryTime, setQueryTime] = useState(0);
  const [error, setError] = useState('');

  const { data: reposData } = useRepositories();
  const repos = reposData?.results || [];

  const handleSearch = async () => {
    if (!query.trim()) return;
    if (repos.length === 0) {
      setError('No repositories available. Import a repository first.');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const res = await searchService.search({
        query: query.trim(),
        repository_ids: repos.map((r: any) => r.id),
        limit: 10,
      });
      setResults(res.data.data.results);
      setQueryTime(res.data.data.query_time_ms);
      setSearched(true);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Search failed.');
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Semantic Search</h1>
        <p className="text-muted-foreground">Search your code by meaning, not just keywords</p>
      </div>

      <div className="flex gap-2">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Describe what you're looking for... (e.g., 'function that validates email')"
            className="pl-9"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          />
        </div>
        <Button onClick={handleSearch} disabled={loading}>
          {loading ? 'Searching...' : 'Search'}
        </Button>
      </div>

      {error && <p className="text-sm text-destructive">{error}</p>}

      {loading && (
        <div className="space-y-3">
          <Skeleton className="h-24 w-full" />
          <Skeleton className="h-24 w-full" />
        </div>
      )}

      {searched && !loading && (
        <div className="space-y-3">
          <p className="text-sm text-muted-foreground">
            {results.length} results found in {queryTime}ms
          </p>
          {results.map((result) => (
            <Card key={result.chunk_id} className="hover:border-primary/50 transition-colors">
              <CardContent className="p-4 space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <FileCode className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm font-medium">{result.file_path}</span>
                    <span className="text-xs text-muted-foreground">
                      :{result.start_line}-{result.end_line}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge variant="secondary">{result.chunk_type}</Badge>
                    <span className="text-xs text-muted-foreground">
                      {Math.round(result.relevance_score * 100)}%
                    </span>
                  </div>
                </div>
                {result.symbol_name && (
                  <div className="flex items-center gap-1 text-sm">
                    <Code className="h-3 w-3" />
                    <span className="font-mono text-primary">{result.symbol_name}</span>
                  </div>
                )}
                <pre className="bg-secondary/50 p-3 rounded text-xs overflow-x-auto font-mono max-h-40">
                  {result.content}
                </pre>
              </CardContent>
            </Card>
          ))}
          {results.length === 0 && (
            <p className="text-center py-8 text-muted-foreground">No results found. Try a different query.</p>
          )}
        </div>
      )}

      {!searched && !loading && (
        <div className="text-center py-16 text-muted-foreground">
          <Search className="h-12 w-12 mx-auto mb-4 opacity-20" />
          <p>Search for code using natural language</p>
          <p className="text-sm mt-1">Try: "function that validates email" or "database connection setup"</p>
        </div>
      )}
    </div>
  );
}
