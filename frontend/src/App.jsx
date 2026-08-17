import React, { useState, useEffect, useRef } from 'react';
import { 
  MessageSquare, 
  FileText, 
  CheckSquare, 
  Settings, 
  Brain, 
  Mic, 
  Upload, 
  Calendar, 
  Mail, 
  TrendingUp, 
  ArrowRight,
  User,
  Plus
} from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [chatMessages, setChatMessages] = useState([
    { sender: 'assistant', text: "Hello! I am NovaAgent. How can I assist you with your productivity today?" }
  ]);
  const [inputText, setInputText] = useState('');
  const [notes, setNotes] = useState([
    { id: 1, title: 'Strategic Roadmap', content: 'Explore integration parameters with Outlook OAuth models.', important: true },
    { id: 2, title: 'Ideas', content: 'Setup local LLM models using Llama 3 via Ollama gateways.', important: false }
  ]);
  const [tasks, setTasks] = useState([
    { id: 1, title: 'Implement JWT credentials authentication', status: 'completed', priority: 'high' },
    { id: 2, title: 'Design LangGraph orchestrator routing', status: 'in_progress', priority: 'high' },
    { id: 3, title: 'Configure pgvector migrations', status: 'pending', priority: 'medium' }
  ]);
  const [memories, setMemories] = useState([
    { category: 'Task', content: 'Database migration due tomorrow at 9 AM' },
    { category: 'Note', content: 'Vite app setup using dark modes and glassmorphism' }
  ]);

  const [noteTitle, setNoteTitle] = useState('');
  const [noteContent, setNoteContent] = useState('');
  const [taskTitle, setTaskTitle] = useState('');

  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages]);

  const handleSendMessage = () => {
    if (!inputText.trim()) return;
    const newMsg = { sender: 'user', text: inputText };
    setChatMessages(prev => [...prev, newMsg]);
    setInputText('');

    // Simulate AI thinking and streaming response
    setTimeout(() => {
      setChatMessages(prev => [...prev, {
        sender: 'assistant',
        text: `I received: "${inputText}". Since you mentioned notes or tasks, the Master Orchestrator routed this to the appropriate service handler. [Simulated Response]`
      }]);
    }, 800);
  };

  const handleCreateNote = (e) => {
    e.preventDefault();
    if (!noteTitle.trim()) return;
    const newNote = {
      id: Date.now(),
      title: noteTitle,
      content: noteContent,
      important: true
    };
    setNotes([newNote, ...notes]);
    setMemories([
      { category: 'Note', content: `Important Note: ${noteTitle} - ${noteContent}` },
      ...memories
    ]);
    setNoteTitle('');
    setNoteContent('');
  };

  const handleCreateTask = (e) => {
    e.preventDefault();
    if (!taskTitle.trim()) return;
    const newT = {
      id: Date.now(),
      title: taskTitle,
      status: 'pending',
      priority: 'medium'
    };
    setTasks([...tasks, newT]);
    setTaskTitle('');
  };

  return (
    <div className="flex h-screen bg-[#070b14] text-gray-100 overflow-hidden font-sans">
      
      {/* Sidebar Navigation */}
      <aside className="w-64 bg-[#0c1222] border-r border-[#1a253e] flex flex-col justify-between">
        <div>
          <div className="p-6 flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
              <Brain className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="font-bold text-lg leading-tight tracking-wider text-transparent bg-clip-text bg-gradient-to-r from-white via-blue-100 to-blue-300">NovaAgent</h1>
              <span className="text-xs text-blue-400 font-medium tracking-widest">ASSISTANT</span>
            </div>
          </div>

          <nav className="px-4 py-2 space-y-1">
            <button 
              onClick={() => setActiveTab('dashboard')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 ${activeTab === 'dashboard' ? 'bg-gradient-to-r from-blue-600/25 to-purple-600/10 text-blue-400 border-l-4 border-blue-500' : 'text-gray-400 hover:bg-[#131b31] hover:text-white'}`}
            >
              <TrendingUp className="w-4 h-4" /> Dashboard
            </button>
            <button 
              onClick={() => setActiveTab('chat')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 ${activeTab === 'chat' ? 'bg-gradient-to-r from-blue-600/25 to-purple-600/10 text-blue-400 border-l-4 border-blue-500' : 'text-gray-400 hover:bg-[#131b31] hover:text-white'}`}
            >
              <MessageSquare className="w-4 h-4" /> AI Chat
            </button>
            <button 
              onClick={() => setActiveTab('notes')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 ${activeTab === 'notes' ? 'bg-gradient-to-r from-blue-600/25 to-purple-600/10 text-blue-400 border-l-4 border-blue-500' : 'text-gray-400 hover:bg-[#131b31] hover:text-white'}`}
            >
              <FileText className="w-4 h-4" /> Notes Agent
            </button>
            <button 
              onClick={() => setActiveTab('tasks')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 ${activeTab === 'tasks' ? 'bg-gradient-to-r from-blue-600/25 to-purple-600/10 text-blue-400 border-l-4 border-blue-500' : 'text-gray-400 hover:bg-[#131b31] hover:text-white'}`}
            >
              <CheckSquare className="w-4 h-4" /> Tasks Agent
            </button>
          </nav>
        </div>

        {/* User profile footer */}
        <div className="p-4 border-t border-[#1a253e] flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-[#16223f] flex items-center justify-center text-blue-400 font-bold border border-blue-500/20">
            <User className="w-4 h-4" />
          </div>
          <div>
            <p className="text-sm font-semibold text-white">Executive User</p>
            <p className="text-xs text-gray-500">exec@novaagent.ai</p>
          </div>
        </div>
      </aside>

      {/* Main Panel Area */}
      <main className="flex-1 flex flex-col overflow-hidden bg-[#070b14] relative">
        <header className="h-16 border-b border-[#1a253e] flex items-center justify-between px-8 bg-[#0c1222]/50 backdrop-blur-md z-10">
          <h2 className="text-xl font-bold capitalize tracking-wide">{activeTab} View</h2>
          <div className="flex items-center gap-3">
            <span className="flex h-2.5 w-2.5 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
            </span>
            <span className="text-xs text-gray-400 font-semibold uppercase">Local LLM Connected</span>
          </div>
        </header>

        {/* Dynamic Panels */}
        <div className="flex-1 overflow-y-auto p-8">
          
          {/* Dashboard Tab */}
          {activeTab === 'dashboard' && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              
              {/* Long term memory widget */}
              <div className="lg:col-span-2 glass-container p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <Brain className="w-5 h-5 text-purple-400 animate-pulse" />
                    <h3 className="font-semibold text-lg text-white">Long Term Memory Vault</h3>
                  </div>
                  <span className="text-xs text-purple-400 bg-purple-500/10 px-2 py-1 rounded-md">Vector Database Linked</span>
                </div>
                <div className="space-y-3">
                  {memories.map((m, i) => (
                    <div key={i} className="p-3 bg-[#131b31]/40 border border-[#1d2b4f]/30 rounded-xl flex justify-between items-center">
                      <p className="text-sm text-gray-300">{m.content}</p>
                      <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-blue-500/15 text-blue-400 border border-blue-500/20">{m.category}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* RAG widget */}
              <div className="glass-container p-6 flex flex-col justify-between">
                <div>
                  <div className="flex items-center gap-2 mb-4">
                    <Upload className="w-5 h-5 text-blue-400" />
                    <h3 className="font-semibold text-lg text-white">RAG File Ingestion</h3>
                  </div>
                  <p className="text-sm text-gray-400 mb-4">Upload PDFs, txt or docs to enrich your AI RAG Knowledge pool.</p>
                  
                  <div className="border border-dashed border-[#23355d] hover:border-blue-500 rounded-xl p-6 text-center cursor-pointer transition-all duration-300 bg-[#0d1428]/45">
                    <Upload className="w-8 h-8 text-gray-500 mx-auto mb-2" />
                    <p className="text-sm font-medium text-gray-300">Drag file here or click</p>
                    <p className="text-xs text-gray-500 mt-1">PDF or Plaintext files (up to 10MB)</p>
                  </div>
                </div>
                <button className="mt-4 w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white rounded-xl py-3 text-sm font-semibold shadow-lg shadow-blue-500/10 flex items-center justify-center gap-2">
                  Launch Document Chat <ArrowRight className="w-4 h-4" />
                </button>
              </div>

              {/* Future Roadmaps Placeholder (Email, Calendar, Meeting integrations) */}
              <div className="lg:col-span-3 glass-container p-6">
                <h3 className="font-semibold text-lg text-white mb-4">Phase 2: Agent Orchestration Roadmap</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="p-4 bg-[#11192f]/50 border border-[#1e2c4f]/40 rounded-xl flex items-start gap-3">
                    <Mail className="w-5 h-5 text-blue-400 mt-1" />
                    <div>
                      <h4 className="font-semibold text-sm text-gray-200">Email Agent</h4>
                      <p className="text-xs text-gray-500 mt-1">Automatic parsing of Gmail/Outlook schedules and template drafting.</p>
                    </div>
                  </div>
                  <div className="p-4 bg-[#11192f]/50 border border-[#1e2c4f]/40 rounded-xl flex items-start gap-3">
                    <Calendar className="w-5 h-5 text-purple-400 mt-1" />
                    <div>
                      <h4 className="font-semibold text-sm text-gray-200">Calendar Sync</h4>
                      <p className="text-xs text-gray-500 mt-1">Double booking conflicts checking and scheduling suggestions.</p>
                    </div>
                  </div>
                  <div className="p-4 bg-[#11192f]/50 border border-[#1e2c4f]/40 rounded-xl flex items-start gap-3">
                    <Mic className="w-5 h-5 text-emerald-400 mt-1" />
                    <div>
                      <h4 className="font-semibold text-sm text-gray-200">Meeting Summaries</h4>
                      <p className="text-xs text-gray-500 mt-1">Auto-summaries extractors from transcripts and sync action lists.</p>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          )}

          {/* AI Chat Tab */}
          {activeTab === 'chat' && (
            <div className="glass-container h-[70vh] flex flex-col overflow-hidden">
              <div className="flex-1 overflow-y-auto p-6 space-y-4">
                {chatMessages.map((msg, i) => (
                  <div key={i} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[70%] p-4 rounded-2xl text-sm leading-relaxed ${msg.sender === 'user' ? 'bg-blue-600 text-white rounded-br-none shadow-md shadow-blue-600/10' : 'bg-[#15203b] text-gray-200 rounded-bl-none border border-[#23335b]/30'}`}>
                      {msg.text}
                    </div>
                  </div>
                ))}
                <div ref={chatEndRef} />
              </div>
              <div className="p-4 border-t border-[#1a253e] bg-[#0c1222]/30 flex items-center gap-3">
                <input 
                  type="text" 
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                  placeholder="Ask NovaAgent anything..."
                  className="flex-1 bg-[#0c1222] border border-[#203159] focus:border-blue-500 rounded-xl px-4 py-3 text-sm text-white focus:outline-none placeholder-gray-500"
                />
                <button 
                  onClick={handleSendMessage}
                  className="bg-blue-600 hover:bg-blue-500 text-white p-3 rounded-xl shadow-lg transition-all duration-200"
                >
                  <ArrowRight className="w-5 h-5" />
                </button>
              </div>
            </div>
          )}

          {/* Notes Tab */}
          {activeTab === 'notes' && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-1 glass-container p-6">
                <h3 className="font-semibold text-lg text-white mb-4">Add Note</h3>
                <form onSubmit={handleCreateNote} className="space-y-4">
                  <div>
                    <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Title</label>
                    <input 
                      type="text" 
                      value={noteTitle}
                      onChange={(e) => setNoteTitle(e.target.value)}
                      placeholder="Roadmap parameters"
                      className="w-full bg-[#0c1222] border border-[#203159] focus:border-blue-500 rounded-xl px-4 py-3 text-sm focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Content</label>
                    <textarea 
                      value={noteContent}
                      onChange={(e) => setNoteContent(e.target.value)}
                      placeholder="Write your note here..."
                      rows="4"
                      className="w-full bg-[#0c1222] border border-[#203159] focus:border-blue-500 rounded-xl px-4 py-3 text-sm focus:outline-none"
                    />
                  </div>
                  <button type="submit" className="w-full bg-blue-600 hover:bg-blue-500 text-white py-3 rounded-xl text-sm font-semibold flex items-center justify-center gap-2">
                    <Plus className="w-4 h-4" /> Save and Index
                  </button>
                </form>
              </div>

              <div className="lg:col-span-2 space-y-4">
                {notes.map(note => (
                  <div key={note.id} className="glass-container p-6 relative">
                    {note.important && (
                      <span className="absolute top-4 right-4 text-xs font-semibold px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 border border-purple-500/20">Saved to Long Term Memory</span>
                    )}
                    <h4 className="font-bold text-lg text-white mb-2">{note.title}</h4>
                    <p className="text-sm text-gray-400">{note.content}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Tasks Tab */}
          {activeTab === 'tasks' && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-1 glass-container p-6">
                <h3 className="font-semibold text-lg text-white mb-4">Add Task</h3>
                <form onSubmit={handleCreateTask} className="space-y-4">
                  <div>
                    <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Task Title</label>
                    <input 
                      type="text" 
                      value={taskTitle}
                      onChange={(e) => setTaskTitle(e.target.value)}
                      placeholder="Integrate vector store"
                      className="w-full bg-[#0c1222] border border-[#203159] focus:border-blue-500 rounded-xl px-4 py-3 text-sm focus:outline-none"
                    />
                  </div>
                  <button type="submit" className="w-full bg-blue-600 hover:bg-blue-500 text-white py-3 rounded-xl text-sm font-semibold flex items-center justify-center gap-2">
                    <Plus className="w-4 h-4" /> Create Todo
                  </button>
                </form>
              </div>

              <div className="lg:col-span-2 glass-container p-6">
                <h3 className="font-semibold text-lg text-white mb-4">Tasks Checklist</h3>
                <div className="space-y-3">
                  {tasks.map(task => (
                    <div key={task.id} className="flex items-center justify-between p-3 bg-[#131b31]/40 border border-[#1e2a4a]/40 rounded-xl">
                      <div className="flex items-center gap-3">
                        <input 
                          type="checkbox" 
                          checked={task.status === 'completed'}
                          onChange={() => {
                            setTasks(tasks.map(t => t.id === task.id ? { ...t, status: t.status === 'completed' ? 'pending' : 'completed' } : t));
                          }}
                          className="w-4 h-4 rounded text-blue-500 focus:ring-blue-500 bg-[#0c1222] border-[#22335c]" 
                        />
                        <span className={`text-sm ${task.status === 'completed' ? 'line-through text-gray-500' : 'text-gray-200'}`}>{task.title}</span>
                      </div>
                      <span className={`text-xs px-2.5 py-0.5 rounded-full uppercase font-bold ${task.priority === 'high' ? 'bg-red-500/10 text-red-400 border border-red-500/20' : 'bg-blue-500/10 text-blue-400 border border-blue-500/20'}`}>
                        {task.priority}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

        </div>
      </main>

    </div>
  );
}
