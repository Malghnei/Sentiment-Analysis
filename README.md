# Sentiment Analysis System
This project provides a full-stack application for analyzing the sentiment of Amazon reviews using machine learning models. It consists of a robust Python backend and a modern SvelteKit frontend.

## Architecture

The project is structured as a monorepo containing two main components:

### Backend (Python/FastAPI)
The backend is a REST API packaged as a Docker container, self-hosted on an Oracle Cloud Always Free VM behind Caddy (automatic HTTPS).
*   **Framework**: FastAPI for high-performance API routing and validation.
*   **Machine Learning**:
    *   **RoBERTa**: Deep learning model for advanced sentiment classification (via Hugging Face Transformers).
    *   **VADER**: Rule-based sentiment analysis (via NLTK).
*   **Infrastructure**: Docker image with CPU-only PyTorch and both models baked in, served by Uvicorn on port 7860.

Run locally:
```bash
docker build -t sentiment backend && docker run -p 7860:7860 sentiment
```

Deploy on the VM (needs Docker, ports 80/443 open, and a domain such as a free DuckDNS name pointing at the VM):
```bash
git clone https://github.com/Malghnei/Sentiment-Analysis.git && cd Sentiment-Analysis
cp .env.example .env   # set DOMAIN
docker compose up -d --build
```
Update: `git pull && docker compose up -d --build`.

Oracle Cloud specifics (one-time, on the VM):
- **Open 80/443 in two places.** OCI Console → your instance's subnet → Security List → add Ingress rules for TCP 80 and 443 from `0.0.0.0/0`. The Ubuntu images also ship host iptables rules that reject everything but SSH:
  `sudo iptables -I INPUT 6 -p tcp -m multiport --dports 80,443 -j ACCEPT && sudo netfilter-persistent save`
  (Oracle Linux instead: `sudo firewall-cmd --permanent --add-service={http,https} && sudo firewall-cmd --reload`.)
- **Docker:** `curl -fsSL https://get.docker.com | sudo sh && sudo usermod -aG docker $USER` (log out/in after).
- **Shape:** the Ampere A1 (ARM) shape works as-is (PyTorch ships ARM CPU wheels). The 1 GB `E2.1.Micro` shape will run out of memory building/loading RoBERTa; add swap first:
  `sudo fallocate -l 4G /swapfile && sudo chmod 600 /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile && echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab`
- **Frontend:** set `PUBLIC_API_URL=https://<DOMAIN>` in the Netlify site's environment variables and redeploy.

### Frontend (SvelteKit)
The frontend provides a fast, responsive user interface to interact with the sentiment API.
*   **Framework**: SvelteKit for modern, SSR-capable web application development.
*   **Styling**: Tailwind CSS for a utility-first, responsive design.
*   **Data Processing**: PapaParse for robust client-side CSV parsing.
*   **Deployment**: Netlify (`@sveltejs/adapter-netlify`). Set `PUBLIC_API_URL` to the backend URL (see `frontend/.env.example`).