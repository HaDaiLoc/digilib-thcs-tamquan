I. Chay local
1. Backend
- cd "C:\Users\NHA LINH\Documents\MY WORKSPACE\digilib_v2\digilib-thcs-tamquan\backend"
- pip install -r requirements.txt
- alembic upgrade head
- python run_backend.py
- API: http://127.0.0.1:8001
- Swagger: http://127.0.0.1:8001/docs

2. Frontend
- Mo terminal moi
- cd "C:\Users\NHA LINH\Documents\MY WORKSPACE\digilib_v2\digilib-thcs-tamquan\frontend"
- npm install
- npm run dev
- Frontend: http://127.0.0.1:5173

II. Deploy
1. Backend tren Render
- Push code len nhanh `main`.
- Tren Render, tao Blueprint tu `render.yaml` (chi tao 1 web service backend).
- Set env var backend:
  - DATABASE_URL
  - SECRET_KEY
  - NVIDIA_API_KEY
  - CORS_ORIGINS (them domain Vercel cua frontend)

2. Frontend tren Vercel
- Import repo vao Vercel, root directory: `frontend`.
- Build command: `npm run build`.
- Output directory: `dist`.
- Env var:
  - VITE_API_BASE_URL=https://<backend-render-domain>/api
- Da co file `frontend/vercel.json` de rewrite SPA route ve `index.html`.
