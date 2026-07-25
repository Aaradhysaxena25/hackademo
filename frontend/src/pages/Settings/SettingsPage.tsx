import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { User, Key, Github, Brain } from 'lucide-react';

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState('profile');

  const tabs = [
    { id: 'profile', label: 'Profile', icon: User },
    { id: 'ai', label: 'AI Config', icon: Brain },
    { id: 'github', label: 'GitHub', icon: Github },
    { id: 'api', label: 'API Keys', icon: Key },
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Settings</h1>

      <div className="flex gap-6">
        {/* Tabs */}
        <div className="w-48 space-y-1">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm transition-colors ${
                activeTab === tab.id ? 'bg-primary/10 text-primary font-medium' : 'text-muted-foreground hover:bg-accent'
              }`}
            >
              <tab.icon className="h-4 w-4" />
              {tab.label}
            </button>
          ))}
        </div>

        {/* Content */}
        <div className="flex-1 max-w-2xl">
          {activeTab === 'profile' && (
            <Card>
              <CardHeader><CardTitle>Profile</CardTitle></CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium">First Name</label>
                    <Input defaultValue="John" className="mt-1" />
                  </div>
                  <div>
                    <label className="text-sm font-medium">Last Name</label>
                    <Input defaultValue="Doe" className="mt-1" />
                  </div>
                </div>
                <div>
                  <label className="text-sm font-medium">Email</label>
                  <Input defaultValue="john@example.com" className="mt-1" disabled />
                </div>
                <Button>Save Changes</Button>
              </CardContent>
            </Card>
          )}

          {activeTab === 'ai' && (
            <Card>
              <CardHeader><CardTitle>AI Configuration</CardTitle></CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm font-medium">LLM Provider</label>
                  <select className="mt-1 w-full rounded-md border border-input bg-background px-3 py-2 text-sm">
                    <option>OpenAI</option>
                    <option>Ollama (Local)</option>
                  </select>
                </div>
                <div>
                  <label className="text-sm font-medium">Model</label>
                  <select className="mt-1 w-full rounded-md border border-input bg-background px-3 py-2 text-sm">
                    <option>gpt-4o-mini</option>
                    <option>gpt-4o</option>
                    <option>gpt-3.5-turbo</option>
                  </select>
                </div>
                <div>
                  <label className="text-sm font-medium">API Key</label>
                  <Input type="password" placeholder="sk-..." className="mt-1" />
                </div>
                <Button>Save Configuration</Button>
              </CardContent>
            </Card>
          )}

          {activeTab === 'github' && (
            <Card>
              <CardHeader><CardTitle>GitHub Connection</CardTitle></CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center gap-3 p-3 rounded-md border">
                  <Github className="h-5 w-5" />
                  <div className="flex-1">
                    <p className="text-sm font-medium">Not connected</p>
                    <p className="text-xs text-muted-foreground">Connect GitHub to import repositories</p>
                  </div>
                  <Button variant="outline">Connect GitHub</Button>
                </div>
              </CardContent>
            </Card>
          )}

          {activeTab === 'api' && (
            <Card>
              <CardHeader><CardTitle>API Keys</CardTitle></CardHeader>
              <CardContent className="space-y-4">
                <p className="text-sm text-muted-foreground">
                  API keys allow external tools to access your CodePilot data.
                </p>
                <Button variant="outline">Generate New Key</Button>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
