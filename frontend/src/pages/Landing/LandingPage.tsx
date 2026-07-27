import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import {
  MessageSquare, Search, FileText, Bug, GitBranch, BarChart3,
  Code, Zap, Shield, ArrowRight
} from 'lucide-react';

const features = [
  { icon: MessageSquare, title: 'AI Chat', desc: 'Have natural conversations about your codebase. Ask how things work, find bugs, or understand complex logic.' },
  { icon: Search, title: 'Semantic Search', desc: 'Search by meaning, not keywords. Find "the function that sends emails" without knowing the exact name.' },
  { icon: FileText, title: 'Auto Documentation', desc: 'Generate comprehensive docs for functions, classes, and entire modules in seconds.' },
  { icon: Bug, title: 'Bug Detection', desc: 'AI-powered static analysis that finds potential bugs, security issues, and anti-patterns.' },
  { icon: GitBranch, title: 'PR Review', desc: 'Get AI code reviews on pull requests — catch issues before they reach production.' },
  { icon: BarChart3, title: 'Code Analytics', desc: 'Visualize language distribution, complexity metrics, and repository health at a glance.' },
];

const techStack = [
  { icon: Code, label: 'RAG Pipeline' },
  { icon: Zap, label: 'Vector Search' },
  { icon: Shield, label: 'JWT Auth' },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Navbar */}
      <header className="sticky top-0 z-50 border-b bg-background/80 backdrop-blur-sm">
        <nav className="container mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
              <Code className="h-4 w-4 text-primary-foreground" />
            </div>
            <span className="text-lg font-bold">CodePilot AI</span>
          </div>
          <div className="flex items-center gap-2">
            <Link to="/login">
              <Button variant="ghost" size="sm">Sign In</Button>
            </Link>
            <Link to="/register">
              <Button size="sm">Get Started</Button>
            </Link>
          </div>
        </nav>
      </header>

      {/* Hero */}
      <section className="container mx-auto px-4 pt-20 pb-16 text-center">
        <div className="inline-flex items-center gap-2 bg-primary/5 border border-primary/20 px-4 py-1.5 rounded-full text-sm text-primary mb-6">
          <Zap className="h-3.5 w-3.5" />
          Powered by RAG + Sentence Transformers
        </div>
        <h1 className="text-4xl md:text-6xl font-bold tracking-tight mb-5 max-w-4xl mx-auto leading-tight">
          Understand any codebase
          <br />
          <span className="text-primary">in seconds, not hours</span>
        </h1>
        <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto leading-relaxed">
          Import your repository, and start asking questions. CodePilot indexes your code,
          understands the architecture, and answers with precise file references.
        </p>
        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <Link to="/register">
            <Button size="lg" className="gap-2 px-8">
              Start Free <ArrowRight className="h-4 w-4" />
            </Button>
          </Link>
          <Link to="/login">
            <Button variant="outline" size="lg" className="px-8">
              Sign In
            </Button>
          </Link>
        </div>

        {/* Tech pills */}
        <div className="flex justify-center gap-3 mt-10">
          {techStack.map((t) => (
            <div key={t.label} className="flex items-center gap-1.5 text-xs text-muted-foreground bg-secondary px-3 py-1.5 rounded-full">
              <t.icon className="h-3 w-3" />
              {t.label}
            </div>
          ))}
        </div>
      </section>

      {/* Demo preview */}
      <section className="container mx-auto px-4 pb-16">
        <div className="max-w-4xl mx-auto rounded-xl border bg-card p-6 shadow-lg">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-3 h-3 rounded-full bg-red-400" />
            <div className="w-3 h-3 rounded-full bg-yellow-400" />
            <div className="w-3 h-3 rounded-full bg-green-400" />
            <span className="ml-3 text-xs text-muted-foreground font-mono">CodePilot AI Chat</span>
          </div>
          <div className="space-y-3">
            <div className="flex justify-end">
              <div className="bg-primary text-primary-foreground px-4 py-2 rounded-lg text-sm max-w-xs">
                How does user authentication work in this project?
              </div>
            </div>
            <div className="flex gap-2">
              <div className="w-6 h-6 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0 mt-1">
                <Code className="h-3 w-3 text-primary" />
              </div>
              <div className="bg-secondary px-4 py-3 rounded-lg text-sm max-w-md">
                <p className="mb-2">The auth system uses <strong>JWT tokens</strong> with rotation:</p>
                <code className="block bg-background p-2 rounded text-xs font-mono mb-2">
                  src/middleware/auth.py:15-35
                </code>
                <p className="text-muted-foreground text-xs">3 sources found • 94% relevance</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="container mx-auto px-4 py-16 border-t">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-3">Everything you need to understand code</h2>
          <p className="text-muted-foreground max-w-xl mx-auto">From quick answers to deep analysis — CodePilot gives you superpowers over any codebase.</p>
        </div>
        <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3 max-w-5xl mx-auto">
          {features.map((f) => (
            <div key={f.title} className="rounded-xl border p-5 hover:border-primary/30 hover:shadow-sm transition-all group">
              <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center mb-3 group-hover:bg-primary/20 transition-colors">
                <f.icon className="h-5 w-5 text-primary" />
              </div>
              <h3 className="font-semibold mb-1.5">{f.title}</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section className="container mx-auto px-4 py-16 border-t">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-3">Three steps to code clarity</h2>
        </div>
        <div className="grid gap-8 md:grid-cols-3 max-w-3xl mx-auto">
          {[
            { step: '1', title: 'Import', desc: 'Connect GitHub or upload a ZIP archive' },
            { step: '2', title: 'Index', desc: 'AI parses, chunks, and embeds your code' },
            { step: '3', title: 'Ask', desc: 'Chat, search, generate docs — all in one place' },
          ].map((s) => (
            <div key={s.step} className="text-center">
              <div className="w-12 h-12 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-bold text-lg mx-auto mb-4">
                {s.step}
              </div>
              <h3 className="font-semibold text-lg mb-1">{s.title}</h3>
              <p className="text-sm text-muted-foreground">{s.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="container mx-auto px-4 py-16 border-t">
        <div className="text-center max-w-xl mx-auto">
          <h2 className="text-2xl font-bold mb-3">Ready to understand your code better?</h2>
          <p className="text-muted-foreground mb-6">Free to start. No credit card required.</p>
          <Link to="/register">
            <Button size="lg" className="gap-2">
              Get Started Free <ArrowRight className="h-4 w-4" />
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-6">
        <div className="container mx-auto px-4 flex items-center justify-between text-sm text-muted-foreground">
          <div className="flex items-center gap-2">
            <Code className="h-4 w-4" />
            <span>CodePilot AI</span>
          </div>
          <span>© 2024. Built for developers.</span>
        </div>
      </footer>
    </div>
  );
}
