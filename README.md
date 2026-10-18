# AI Resume Analyzer

AI Resume Analyzer is a full-stack application that evaluates a resume against a job description. It extracts resume text, compares skills, calculates an ATS-style score, and generates targeted improvement suggestions.

## Features

- PDF and DOCX resume upload
- Job description matching
- ATS compatibility scoring
- Matched and missing skill detection
- Resume strengths and improvement suggestions
- Bullet-point rewrite suggestions
- React frontend with a FastAPI backend
- Optional local Ollama integration for AI-generated suggestions

## Project structure

```text
ai-resume-analyzer/
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   ├── schemas/
│   │   └── services/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   └── package.json
└── requirements.txt
```

## Run locally

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

The backend runs at `http://127.0.0.1:8001`.

### Frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at the URL shown by Vite, usually `http://localhost:5173`.

For a custom backend URL, create `frontend/.env.local`:

```env
VITE_API_BASE_URL=http://localhost:8001
```

## Production deployment

### Backend on Render

Use the repository with these Render settings:

```text
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

If the Root Directory is left blank, use:

```text
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port $PORT
```

Set the backend CORS variable to your deployed frontend origin:

```env
CORS_ORIGINS=https://your-frontend-domain.vercel.app
```

### Frontend on Vercel

Set the Vercel project root directory to `frontend` and add:

```env
VITE_API_BASE_URL=https://your-backend-domain.onrender.com
```

Redeploy after changing environment variables.

## API

### `GET /`

Returns the backend health status.

### `POST /api/analyze`

Accepts multipart form data:

- `resume`: PDF or DOCX file
- `job_description`: job description text

Returns the ATS score, category scores, skill matches, strengths, improvements, and bullet rewrites.

## Notes

- Resume files must be PDF or DOCX.
- The application uses a curated skills dictionary for matching.
- Ollama is optional. If the configured local model is unavailable, the backend returns fallback suggestions.
- Do not commit `.env` files, API keys, virtual environments, or generated build output.
