# Sentiment Analysis System
This project provides a full-stack application for analyzing the sentiment of Amazon reviews using machine learning models. It consists of a robust Python backend and a modern SvelteKit frontend.

## Architecture

The project is structured as a monorepo containing two main components:

### Backend (Python/FastAPI)
The backend is a REST API packaged as a Docker container and hosted for free on Hugging Face Spaces.
*   **Framework**: FastAPI for high-performance API routing and validation.
*   **Machine Learning**:
    *   **RoBERTa**: Deep learning model for advanced sentiment classification (via Hugging Face Transformers).
    *   **VADER**: Rule-based sentiment analysis (via NLTK).
*   **Infrastructure**: Docker image with CPU-only PyTorch and both models baked in, served by Uvicorn on port 7860.

Run locally:
```bash
docker build -t sentiment backend && docker run -p 7860:7860 sentiment
```

Deploy (pushes only `backend/` to the Space; use a Hugging Face write token as the password):
```bash
git remote add space https://huggingface.co/spaces/<user>/<space>
git subtree push --prefix backend space main
```

### Frontend (SvelteKit)
The frontend provides a fast, responsive user interface to interact with the sentiment API.
*   **Framework**: SvelteKit for modern, SSR-capable web application development.
*   **Styling**: Tailwind CSS for a utility-first, responsive design.
*   **Data Processing**: PapaParse for robust client-side CSV parsing.
*   **Deployment**: Netlify (`@sveltejs/adapter-netlify`). Set `PUBLIC_API_URL` to the backend URL (see `frontend/.env.example`).