import React, { useState, useEffect, useRef } from "react";
import {
  MessageSquare,
  FileText,
  CheckSquare,
  Brain,
  Mic,
  Upload,
  Calendar,
  Mail,
  TrendingUp,
  ArrowRight,
  User,
  Plus,
} from "lucide-react";

export default function App() {
  const [activeTab, setActiveTab] = useState("dashboard");
  const [chatMessages, setChatMessages] = useState([
    { sender: "assistant", text: "Hello! I am NovaAgent. How can I assist you with your productivity today?" },
  ]);
  const [inputText, setInputText] = useState("");
  const [notes, setNotes] = useState([
    { id: 1, title: "Strategic Roadmap", content: "Explore integration parameters with Outlook OAuth models.", important: true },
    { id: 2, title: "Ideas", content: "Setup local LLM models using Llama 3 via Ollama gateways.", important: false },
  ]);
  const [tasks, setTasks] = useState([
    { id: 1, title: "Implement JWT credentials authentication", status: "completed", priority: "high" },
    { id: 2, title: "Design LangGraph orchestrator routing", status: "in_progress", priority: "high" },
    { id: 3, title: "Configure pgvector migrations", status: "pending", priority: "medium" },
  ]);
  const [memories, setMemories] = useState([
    { category: "Task", content: "Database migration due tomorrow at 9 AM" },
    { category: "Note", content: "Vite app setup using dark modes and glassmorphism" },
  ]);
  const [noteTitle, setNoteTitle] = useState("");
  const [noteContent, setNoteContent] = useState("");
  const [taskTitle, setTaskTitle] = useState("");
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatMessages]);

  const handleSendMessage = () => {
    if (!inputText.trim()) return;
    setChatMessages((prev) => [...prev, { sender: "user", text: inputText }]);
    const sent = inputText;
    setInputText("");
    setTimeout(() => {
      setChatMessages((prev) => [
        ...prev,
        {
          sender: "assistant",
          text: `I received: "${sent}". The Master Orchestrator routed this to the appropriate service handler. [Simulated Response]`,
        },
      ]);
    }, 800);
  };

  const handleCreateNote = (e) => {
    e.preventDefault();
    if (!noteTitle.trim()) return;
    const newNote = { id: Date.now(), title: noteTitle, content: noteContent, important: true };
    setNotes([newNote, ...notes]);
    setMemories([{ category: "Note", content: `${noteTitle}: ${noteContent}` }, ...memories]);
    setNoteTitle("");
    setNoteContent("");
  };

  const handleCreateTask = (e) => {
    e.preventDefault();
    if (!taskTitle.trim()) return;
    setTasks([...tasks, { id: Date.now(), title: taskTitle, status: "pending", priority: "medium" }]);
    setTaskTitle("");
  };

  const tabLabel = { dashboard: "Dashboard", chat: "AI Chat", notes: "Notes Agent", tasks: "Tasks Agent" };

  return (
    <div className="app-shell">
      {/* -- Sidebar -- */}
      <aside className="sidebar">
        <div>
          <div className="sidebar-logo">
            <div className="logo-icon">
              <Brain />
            </div>
            <div className="logo-text">
              <h1>NovaAgent</h1>
              <span>Assistant</span>
            </div>
          </div>
          <nav className="sidebar-nav">
            {[
              { id: "dashboard", label: "Dashboard",   Icon: TrendingUp   },
              { id: "chat",      label: "AI Chat",     Icon: MessageSquare },
              { id: "notes",     label: "Notes Agent", Icon: FileText     },
              { id: "tasks",     label: "Tasks Agent", Icon: CheckSquare  },
            ].map(({ id, label, Icon }) => (
              <button
                key={id}
                onClick={() => setActiveTab(id)}
                className={"nav-btn" + (activeTab === id ? " active" : "")}
              >
                <Icon />
                {label}
              </button>
            ))}
          </nav>
        </div>
        <div className="sidebar-user">
          <div className="user-avatar">
            <User />
          </div>
          <div className="user-info">
            <p>Executive User</p>
            <span>exec@novaagent.ai</span>
          </div>
        </div>
      </aside>

      {/* -- Main -- */}
      <main className="main-area">
        <header className="topbar">
          <h2>{tabLabel[activeTab]}</h2>
          <div className="status-pill">
            <div className="ping-wrapper">
              <span className="ping-dot" />
              <span className="solid-dot" />
            </div>
            Local LLM Connected
          </div>
        </header>

        <div className="scroll-panel">

          {/* Dashboard */}
          {activeTab === "dashboard" && (
            <div className="dashboard-grid">
              <div className="card col-span-2">
                <div className="card-header">
                  <div className="card-header-left">
                    <Brain className="text-purple animate-pulse" style={{ width: 20, height: 20 }} />
                    <h3>Long Term Memory Vault</h3>
                  </div>
                  <span className="badge badge-purple">Vector Database Linked</span>
                </div>
                {memories.map((m, i) => (
                  <div key={i} className="memory-row">
                    <p>{m.content}</p>
                    <span className="badge badge-blue">{m.category}</span>
                  </div>
                ))}
              </div>

              <div className="card" style={{ display: "flex", flexDirection: "column", justifyContent: "space-between" }}>
                <div>
                  <div className="card-header">
                    <div className="card-header-left">
                      <Upload style={{ width: 20, height: 20, color: "#3b82f6" }} />
                      <h3>RAG File Ingestion</h3>
                    </div>
                  </div>
                  <p className="card-subtext">Upload PDFs, txt or docs to enrich your AI RAG Knowledge pool.</p>
                  <div className="drop-zone">
                    <Upload />
                    <span className="drop-title">Drag file here or click</span>
                    <span className="drop-sub">PDF or Plaintext files (up to 10MB)</span>
                  </div>
                </div>
                <button className="btn btn-primary mt-4">
                  Launch Document Chat <ArrowRight style={{ width: 16, height: 16 }} />
                </button>
              </div>

              <div className="card col-span-3">
                <div className="card-header">
                  <h3>Phase 2: Agent Orchestration Roadmap</h3>
                </div>
                <div className="roadmap-grid">
                  {[
                    { Icon: Mail,     color: "#3b82f6", title: "Email Agent",       desc: "Automatic parsing of Gmail/Outlook schedules and template drafting." },
                    { Icon: Calendar, color: "#a855f7", title: "Calendar Sync",     desc: "Double booking conflict checking and scheduling suggestions." },
                    { Icon: Mic,      color: "#10b981", title: "Meeting Summaries", desc: "Auto-summary extractors from transcripts and sync action lists." },
                  ].map(({ Icon, color, title, desc }) => (
                    <div key={title} className="roadmap-item">
                      <Icon style={{ color, width: 18, height: 18, marginTop: 2, flexShrink: 0 }} />
                      <div><h4>{title}</h4><p>{desc}</p></div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* AI Chat */}
          {activeTab === "chat" && (
            <div className="chat-wrap">
              <div className="chat-messages">
                {chatMessages.map((msg, i) => (
                  <div key={i} className={"chat-row " + msg.sender}>
                    <div className={"chat-bubble " + msg.sender}>{msg.text}</div>
                  </div>
                ))}
                <div ref={chatEndRef} />
              </div>
              <div className="chat-input-bar">
                <input
                  type="text"
                  className="form-input"
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
                  placeholder="Ask NovaAgent anything..."
                />
                <button className="btn-icon" onClick={handleSendMessage}>
                  <ArrowRight />
                </button>
              </div>
            </div>
          )}

          {/* Notes */}
          {activeTab === "notes" && (
            <div className="side-panel-grid">
              <div className="card">
                <h3 style={{ fontFamily: "Outfit,sans-serif", fontSize: 15, fontWeight: 600, color: "#fff", marginBottom: 18 }}>Add Note</h3>
                <form onSubmit={handleCreateNote}>
                  <div className="form-group">
                    <label className="form-label">Title</label>
                    <input type="text" className="form-input" value={noteTitle} onChange={(e) => setNoteTitle(e.target.value)} placeholder="Roadmap parameters" />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Content</label>
                    <textarea className="form-textarea" value={noteContent} onChange={(e) => setNoteContent(e.target.value)} placeholder="Write your note here..." rows={5} />
                  </div>
                  <button type="submit" className="btn btn-primary">
                    <Plus style={{ width: 16, height: 16 }} /> Save and Index
                  </button>
                </form>
              </div>
              <div className="notes-list">
                {notes.map((note) => (
                  <div key={note.id} className="note-card">
                    {note.important && <span className="note-badge">Saved to Long Term Memory</span>}
                    <h4>{note.title}</h4>
                    <p>{note.content}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Tasks */}
          {activeTab === "tasks" && (
            <div className="side-panel-grid">
              <div className="card">
                <h3 style={{ fontFamily: "Outfit,sans-serif", fontSize: 15, fontWeight: 600, color: "#fff", marginBottom: 18 }}>Add Task</h3>
                <form onSubmit={handleCreateTask}>
                  <div className="form-group">
                    <label className="form-label">Task Title</label>
                    <input type="text" className="form-input" value={taskTitle} onChange={(e) => setTaskTitle(e.target.value)} placeholder="Integrate vector store" />
                  </div>
                  <button type="submit" className="btn btn-primary">
                    <Plus style={{ width: 16, height: 16 }} /> Create Todo
                  </button>
                </form>
              </div>
              <div className="card">
                <h3 style={{ fontFamily: "Outfit,sans-serif", fontSize: 15, fontWeight: 600, color: "#fff", marginBottom: 18 }}>Tasks Checklist</h3>
                <div className="tasks-list">
                  {tasks.map((task) => (
                    <div key={task.id} className="task-row">
                      <div className="task-left">
                        <input
                          type="checkbox"
                          checked={task.status === "completed"}
                          onChange={() =>
                            setTasks(tasks.map((t) =>
                              t.id === task.id ? { ...t, status: t.status === "completed" ? "pending" : "completed" } : t
                            ))
                          }
                        />
                        <span className={"task-label" + (task.status === "completed" ? " done" : "")}>{task.title}</span>
                      </div>
                      <span className={"badge " + (task.priority === "high" ? "badge-red" : "badge-blue")}>{task.priority}</span>
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
