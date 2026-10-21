# PlacementPilot — AI-Powered Student Skill Mapping & Placement System

PlacementPilot is a production-ready, enterprise-grade placement and internship management platform. Built with React 18, TypeScript, Vite, Flask, SQLAlchemy, and OpenAI/Gemini integration with a deterministic fallback engine.

---

## 🌟 Key Features

1. **Three Distinct Scoped Login Pages**:
   - `/login/student` → Student Portal
   - `/login/admin` → College Admin Portal
   - `/login/industry` → Recruiter Portal
2. **AI Resume & ATS Verification**:
   - PDF/DOCX parsing with section-by-section feedback (Formatting, Keywords, Impact, Readability, ATS-friendliness).
3. **Webcam Proctored Exam Engine**:
   - Real-time `MediaDevices` webcam preview, tab switch listener, and auto-termination on proctoring violations.
   - Monaco code editor integration (`@monaco-editor/react`) for LeetCode-style coding rounds.
4. **11-Stage Recruitment Pipeline State Machine**:
   - `POSTED` → `APPLIED` → `ELIGIBILITY_FAILED` → `ELIGIBLE` → `SHORTLISTED` → `INTERVIEW_SCHEDULED` → `INTERVIEWED` → `SELECTED` → `REJECTED` → `OFFERED` → `PLACED`.
   - Real-time audit history & notifications on stage transitions.
5. **Interactive 11-Column Kanban Board & Skills Matrix**:
   - Admin oversight with override capability and heatmaps comparing student scores against benchmarks.

---

## 🚀 Quick Start (Local Setup)

### Prerequisites
- Python 3.11+
- Node.js 20+
- (Optional) MySQL 8.0 or Docker

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env

# Initialize database and populate seed data
python run.py seed
python run.py
```
Backend API will start at: `http://localhost:5000`

### 2. Frontend Setup (development only)
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
Frontend Web Application will start at: `http://localhost:5173`

For a single host URL, use the Docker deployment below. It builds the frontend into
the backend image and serves both the web application and API at `http://localhost:5000`.

---

## 🔑 Demo Credentials (Generated via `python run.py seed`)

| Role | Email | Password |
|---|---|---|
| **Student** | `student@demo.com` | `Demo@1234` |
| **College Admin** | `admin@demo.com` | `Demo@1234` |
| **Industry Recruiter** | `recruiter@demo.com` | `Demo@1234` |

---

## 🐳 Docker Deployment

To run full stack with MySQL 8:
```bash
docker compose up --build
```

Open `http://localhost:5000` after the containers start. The API health check is
available at `http://localhost:5000/api/v1/health`.
