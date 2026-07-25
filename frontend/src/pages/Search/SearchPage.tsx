import { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Search, FileCode, Code } from 'lucide-react';

interface SearchResult {
  file_path: string;
  symbol_name: string | null;
  chunk_type: string;
  content: string;
  language: string;
  start_line: number;
  end_line: number;
  relevance_score: number;
}

const mockResults: SearchResult[] = [
  {
    file_path: 'src/auth/middleware.py',
    symbol_name: 'authenticate_request',
    chunk_type: 'function',
    content: 'def authenticate_request(request):\n    token = request.headers.get("Authorization")\n    if not token:\n        raise Unauthorized()',
    language: 'python',
    start_line: 15,
    end_line: 25,
    relevance_score: 0.94,
  },
  {
    file_path: 'src/utils/jwt.py',
    symbol_name: 'verify_token',
    chunk_type: 'function',
    content: 'def verify_token(token: str) -> dict:\n    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])\n    return payload',
    language: 'python',
    start_line: 8,
    end_line: 15,
    relevance_score: 0.87,
  },
];

export default function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [searched, setSearched] = useState(false);

  const handleSearch = () => {
    if (!query.trim()) return;
    // Mock search
    setResults(mockResults);
    setSearched(true);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Semantic Search</h1>
        <p className="text-muted-foreground">Search your code by meaning, not just keywords</p>
      </div>

      {/* Search Bar */}
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
        <Button onClick={handleSearch}>Search</Button>
      </div>

      {/* Results */}
      {searched && (
        <div className="space-y-3">
          <p className="text-sm text-muted-foreground">{results.length} results found</p>
          {results.map((result, i) => (
            <Card key={i} className="hover:border-primary/50 transition-colors">
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
                      {Math.round(result.relevance_score * 100)}% match
                    </span>
                  </div>
                </div>
                {result.symbol_name && (
                  <div className="flex items-center gap-1 text-sm">
                    <Code className="h-3 w-3" />
                    <span className="font-mono text-primary">{result.symbol_name}</span>
                  </div>
                )}
                <pre className="bg-secondary/50 p-3 rounded text-xs overflow-x-auto font-mono">
                  {result.content}
                </pre>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {!searched && (
        <div className="text-center py-16 text-muted-foreground">
          <Search className="h-12 w-12 mx-auto mb-4 opacity-20" />
          <p>Search for code using natural language</p>
          <p className="text-sm mt-1">Try: "function that validates email" or "database connection setup"</p>
        </div>
      )}
    </div>
  );
}
