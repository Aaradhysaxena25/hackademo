import { useParams, Link } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import {
  ArrowLeft, MessageSquare, RefreshCw, FileCode, Folder,
} from 'lucide-react';

export default function RepositoryDetailPage() {
  const { id } = useParams();

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Link to="/app/repositories">
          <Button variant="ghost" size="icon"><ArrowLeft className="h-4 w-4" /></Button>
        </Link>
        <div className="flex-1">
          <h1 className="text-2xl font-bold">my-project</h1>
          <p className="text-sm text-muted-foreground">A Python web application</p>
        </div>
        <div className="flex gap-2">
          <Link to={`/app/chat?repo=${id}`}>
            <Button variant="outline"><MessageSquare className="h-4 w-4" /> Chat</Button>
          </Link>
          <Button variant="outline"><RefreshCw className="h-4 w-4" /> Reindex</Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid gap-4 md:grid-cols-4">
        {[
          { label: 'Files', value: '342', icon: FileCode },
          { label: 'Chunks', value: '1,205', icon: Folder },
          { label: 'Lines', value: '28.5K', icon: FileCode },
          { label: 'Coverage', value: '98%', icon: FileCode },
        ].map((s) => (
          <Card key={s.label}>
            <CardContent className="p-4 flex items-center justify-between">
              <div>
                <p className="text-xs text-muted-foreground">{s.label}</p>
                <p className="text-xl font-bold">{s.value}</p>
              </div>
              <s.icon className="h-5 w-5 text-muted-foreground" />
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Languages */}
      <Card>
        <CardHeader><CardTitle>Languages</CardTitle></CardHeader>
        <CardContent className="space-y-2">
          {[
            { lang: 'Python', pct: 65, color: 'bg-blue-500' },
            { lang: 'JavaScript', pct: 25, color: 'bg-yellow-500' },
            { lang: 'HTML', pct: 10, color: 'bg-orange-500' },
          ].map((l) => (
            <div key={l.lang} className="flex items-center gap-3">
              <span className="text-sm w-24">{l.lang}</span>
              <div className="flex-1 h-2 bg-secondary rounded-full overflow-hidden">
                <div className={`h-full ${l.color} rounded-full`} style={{ width: `${l.pct}%` }} />
              </div>
              <span className="text-sm text-muted-foreground w-10">{l.pct}%</span>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* File Browser Preview */}
      <Card>
        <CardHeader><CardTitle>Files</CardTitle></CardHeader>
        <CardContent>
          <div className="space-y-1">
            {['src/', 'src/main.py', 'src/auth.py', 'src/utils.py', 'tests/', 'README.md'].map((f) => (
              <div key={f} className="flex items-center gap-2 px-2 py-1.5 rounded hover:bg-accent text-sm">
                {f.endsWith('/') ? <Folder className="h-4 w-4 text-blue-500" /> : <FileCode className="h-4 w-4 text-muted-foreground" />}
                <span>{f}</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
