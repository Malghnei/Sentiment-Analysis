# Sentiment Analysis System
This project provides a full-stack serverless application for analyzing the sentiment of Amazon reviews using machine learning models. It consists of a robust Python backend and a modern SvelteKit frontend.

## Architecture

The project is structured as a monorepo containing two main components:

### Backend (Python/FastAPI)
The backend is a serverless REST API designed to run on AWS Lambda via AWS SAM.
*   **Framework**: FastAPI for high-performance API routing and validation.
*   **Machine Learning**:
    *   **RoBERTa**: Deep learning model for advanced sentiment classification (via Hugging Face Transformers).
    *   **VADER**: Rule-based sentiment analysis (via NLTK).
*   **Serverless Adapter**: Mangum seamlessly converts AWS API Gateway events into ASGI requests.
*   **Infrastructure**: AWS SAM with a Container Image (Dockerfile) to bypass Lambda deployment size limits and package ML models efficiently.

### Frontend (SvelteKit)
The frontend provides a fast, responsive user interface to interact with the sentiment API.
*   **Framework**: SvelteKit for modern, SSR-capable web application development.
*   **Styling**: Tailwind CSS for a utility-first, responsive design.
*   **Data Processing**: PapaParse for robust client-side CSV parsing.
*   **Deployment**: Configured with `@sveltejs/adapter-auto`, compatible with Vercel, Netlify, and Cloudflare Pages.