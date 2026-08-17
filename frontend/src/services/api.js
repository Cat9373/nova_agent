const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

class ApiClient {
  constructor() {
    this.token = localStorage.getItem('nova_auth_token');
  }

  setToken(token) {
    this.token = token;
    localStorage.setItem('nova_auth_token', token);
  }

  clearToken() {
    this.token = null;
    localStorage.removeItem('nova_auth_token');
  }

  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const config = {
      ...options,
      headers,
    };

    const response = await fetch(url, config);
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Request failed with status ${response.status}`);
    }

    if (response.status === 204) {
      return null;
    }

    return response.json();
  }

  // Auth Operations
  async login(email, password) {
    const data = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    if (data.access_token) {
      this.setToken(data.access_token);
    }
    return data;
  }

  async signup(email, password) {
    return this.request('/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  // User Profile Operations
  async getProfile() {
    return this.request('/user/profile');
  }

  async updateProfile(profileData) {
    return this.request('/user/profile', {
      method: 'PATCH',
      body: JSON.stringify(profileData),
    });
  }

  // Chat Operations
  async sendChatMessage(content, sessionId) {
    return this.request('/chat/message', {
      method: 'POST',
      body: JSON.stringify({ content, session_id: sessionId }),
    });
  }

  // Notes Operations
  async getNotes() {
    return this.request('/notes');
  }

  async createNote(noteData) {
    return this.request('/notes', {
      method: 'POST',
      body: JSON.stringify(noteData),
    });
  }

  async updateNote(noteId, noteData) {
    return this.request(`/notes/${noteId}`, {
      method: 'PATCH',
      body: JSON.stringify(noteData),
    });
  }

  async deleteNote(noteId) {
    return this.request(`/notes/${noteId}`, {
      method: 'DELETE',
    });
  }

  // Tasks Operations
  async getTasks() {
    return this.request('/tasks');
  }

  async createTask(taskData) {
    return this.request('/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  async updateTask(taskId, taskData) {
    return this.request(`/tasks/${taskId}`, {
      method: 'PATCH',
      body: JSON.stringify(taskData),
    });
  }

  async deleteTask(taskId) {
    return this.request(`/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }

  // Document Operations (Requires FormData)
  async uploadDocument(file) {
    const formData = new FormData();
    formData.append('file', file);

    const headers = {};
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(`${API_BASE_URL}/documents/upload`, {
      method: 'POST',
      headers,
      body: formData,
    });

    if (!response.ok) {
      throw new Error('File upload failed');
    }

    return response.json();
  }

  async getDocuments() {
    return this.request('/documents');
  }

  async deleteDocument(docId) {
    return this.request(`/documents/${docId}`, {
      method: 'DELETE',
    });
  }

  // Long-term Memory Operations
  async searchMemory(query, category = null) {
    return this.request('/memory/search', {
      method: 'POST',
      body: JSON.stringify({ query, category }),
    });
  }

  // Voice Directives
  async transcribeVoice(audioBlob) {
    const formData = new FormData();
    formData.append('file', audioBlob, 'audio_directive.wav');

    const headers = {};
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(`${API_BASE_URL}/voice/transcribe`, {
      method: 'POST',
      headers,
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Voice transcription failed');
    }

    return response.json();
  }
}

export const api = new ApiClient();
