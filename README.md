# VideoFlow Live - Async Video Processing Backend

A high-performance, asynchronous video processing system built with **FastAPI**, **Celery**, **Redis**, and **FFmpeg**. Features a premium **React** dashboard for real-time monitoring.

## 🚀 Concept
Heavy video processing (resizing, transcoding) blocks the main thread. This project implements a **Queue Architecture**:
1. **API**: Accepts the upload and returns a Job ID immediately.
2. **Redis**: Acts as the message broker.
3. **Celery Worker**: Picks up the job, runs FFmpeg in a separate process, and updates the DB.
4. **Dashboard**: Live updates on job status (Processing, Completed, Failed).

## 🛠️ Tech Stack
- **Backend**: FastAPI, Celery, SQLAlchemy (SQLite)
- **Frontend**: React (Vite), Lucide Icons, Axios
- **Worker**: FFmpeg
- **Infrastructure**: Docker, Docker Compose, Redis

## 📋 Features
- **Asynchronous Processing**: Immediate response on upload.
- **Premium Live View**: Modern dark-themed dashboard with real-time polling.
- **FFmpeg Integration**: Automatic video resizing to 640px width (maintaining aspect ratio).
- **Persistence**: SQLite database to track job history and metadata.

## 🚦 Getting Started

### Prerequisites
- Docker & Docker Compose
- (Optional) Python 3.11+ if running locally

### Installation & Run

1. **Clone the repository**:
   ```bash
   git clone git@github.com:ommishra0/Async-Video-Processing-Backend.git
   cd Async-Video-Processing-Backend
   ```

2. **Start the services**:
   ```bash
   docker compose up --build
   ```

3. **Access the Application**:
   - **Dashboard**: [http://localhost:5173](http://localhost:5173)
   - **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

## 📁 Project Structure
- `/backend`: FastAPI application and Celery tasks.
- `/frontend`: React dashboard (Vite).
- `/uploads`: Temporary storage for uploaded videos.
- `/processed`: Storage for resized output videos.
- `docker-compose.yml`: Orchestration for API, Worker, Redis, and Frontend.

## 🧪 Verification
You can use the provided script to test the backend flow without the UI:
```bash
python verify_flow.py
```

## 📄 License
MIT
