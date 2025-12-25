import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Upload, Play, CheckCircle, XCircle, RefreshCcw, Video } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [jobs, setJobs] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  const fetchJobs = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/jobs`);
      setJobs(response.data);
    } catch (err) {
      console.error('Failed to fetch jobs:', err);
    }
  };

  useEffect(() => {
    fetchJobs();
    const interval = setInterval(fetchJobs, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    
    setUploading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      await axios.post(`${API_BASE_URL}/upload`, formData);
      setSelectedFile(null);
      fetchJobs();
    } catch (err) {
      alert('Upload failed: ' + err.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="dashboard-container">
      <header>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <Video size={40} color="#bb86fc" />
          <h1>VideoFlow Live</h1>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <RefreshCcw size={16} className="spin" />
          <span style={{ fontSize: '0.9rem', opacity: 0.7 }}>Live Polling Active</span>
        </div>
      </header>

      <section className="upload-card">
        <div className="drop-zone" onClick={() => document.getElementById('fileInput').click()}>
          <Upload size={48} style={{ marginBottom: '1rem', opacity: 0.5 }} />
          <h3>{selectedFile ? selectedFile.name : 'Drop video or click to upload'}</h3>
          <p style={{ opacity: 0.5 }}>MP4, MKV, AVI (Max 50MB)</p>
          <input 
            id="fileInput" 
            type="file" 
            hidden 
            onChange={handleFileChange} 
            accept="video/*"
          />
        </div>
        {selectedFile && (
          <div style={{ marginTop: '1.5rem', display: 'flex', justifyContent: 'center' }}>
            <button onClick={handleUpload} disabled={uploading}>
              {uploading ? 'Processing...' : 'Start Job'}
            </button>
          </div>
        )}
      </section>

      <section className="job-list-container">
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
          <h2>Background Jobs</h2>
          <span>{jobs.length} total</span>
        </div>
        
        <div className="job-list">
          {jobs.map((job) => (
            <div key={job.id} className="job-item">
              <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                <div style={{ background: 'rgba(255,255,255,0.05)', padding: '0.5rem', borderRadius: '8px' }}>
                  {job.status === 'Completed' ? <CheckCircle color="#bb86fc" /> : 
                   job.status === 'Failed' ? <XCircle color="#cf6679" /> : 
                   <RefreshCcw className="spin" color="#03dac6" />}
                </div>
                <div>
                  <div style={{ fontWeight: 600 }}>{job.filename}</div>
                  <div style={{ fontSize: '0.8rem', opacity: 0.4 }}>ID: {job.id.slice(0, 8)}...</div>
                </div>
              </div>
              
              <div className="status-badge-container">
                <span className={`status-badge status-${job.status.toLowerCase()}`}>
                  {job.status}
                </span>
              </div>

              <div style={{ fontSize: '0.9rem', opacity: 0.6 }}>
                {new Date(job.created_at).toLocaleTimeString()}
              </div>

              <div style={{ textAlign: 'right' }}>
                {job.status === 'Completed' && (
                  <a href={`#`} style={{ color: '#03dac6', textDecoration: 'none', fontWeight: 600 }}>
                    Download 
                  </a>
                )}
              </div>
            </div>
          ))}
          {jobs.length === 0 && (
            <div style={{ textAlign: 'center', padding: '3rem', opacity: 0.3 }}>
              No jobs yet. Upload a video to get started.
            </div>
          )}
        </div>
      </section>

      <style>{`
        .spin { animation: spin 2s linear infinite; }
        @keyframes spin { 100% { transform: rotate(360deg); } }
      `}</style>
    </div>
  );
}

export default App;
