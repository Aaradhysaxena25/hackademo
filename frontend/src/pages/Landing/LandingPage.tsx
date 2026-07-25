import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { MessageSquare, Search, FileText, Bug, GitBranch, BarChart3 } from 'lucide-react';

const features = [
  { icon: MessageSquare, title: 'AI Chat', desc: 'Ask questions about your codebase in natural language' },
  { icon: Search, title: 'Semantic Search', desc: 'Find code by meaning, not just keywords' },
  { icon: FileText, title: 'Auto Documentation', desc: 'Generate docs for functions, classes, and modules' },
  { icon: Bug, title: 'Bug Detection', desc: 'Identify potential bugs and security issues' },
  { icon: GitBranch, title: 'PR Review', desc: 'AI-powered code review for pull requests' },
  { icon: BarChart3, title: 'Analytics', desc: 'Visualize code complexity and repository health' },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Navbar */}
      <header className="border-b">
        <nav className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-2xl">🚀</span>
            <span className="text-xl font-bold">CodePilot AI</span>
          </div>
          <div className="flex items-center gap-3">
            <Link to="/login">
              <Button variant="ghost">Login</Button>
            </Link>
            <Link to="/register">
              <Button>Get Started</Button>
            </Link>
          </div>
        </nav>
      </header>

      {/* Hero */}
      <section className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-5xl font-bold tracking-tight mb-4 max-w-3xl mx-auto">
          Chat with your codebase.
          <span className="text-primary"> Understand any repository.</span>
        </h1>
        <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
          Import your repository, ask questions, search semantically, generate docs, and detect bugs — all powered by AI and RAG.
        </p>
        <div className="flex gap-4 justify-center">
          <Link to="/register">
            <Button size="lg">Get Started Free</Button>
          </Link>
          <Link to="/login">
            <Button variant="outline" size="lg">View Demo →</Button>
          </Link>
        </div>
      </section>

      {/* Features */}
      <section className="container mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-center mb-12">Everything you need to understand code</h2>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {features.map((f) => (
            <div key={f.title} className="rounded-lg border p-6 hover:border-primary/50 transition-colors">
              <f.icon className="h-8 w-8 text-primary mb-3" />
              <h3 className="font-semibold mb-1">{f.title}</h3>
              <p className="text-sm text-muted-foreground">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section className="container mx-auto px-4 py-16 text-center">
        <h2 className="text-3xl font-bold mb-12">How it works</h2>
        <div className="grid gap-8 md:grid-cols-3 max-w-3xl mx-auto">
          {[
            { step: '1', title: 'Import', desc: 'Connect GitHub or upload a ZIP' },
            { step: '2', title: 'Index', desc: 'AI parses and embeds your code' },
            { step: '3', title: 'Chat', desc: 'Ask anything about your codebase' },
          ].map((s) => (
            <div key={s.step}>
              <div className="w-10 h-10 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-bold mx-auto mb-3">
                {s.step}
              </div>
              <h3 className="font-semibold">{s.title}</h3>
              <p className="text-sm text-muted-foreground mt-1">{s.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-8">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          © 2024 CodePilot AI. Built for developers.
        </div>
      </footer>
    </div>
  );
}
