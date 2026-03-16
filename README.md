# ⚡ ChronoCast AI — BTC Forecasting ML Platform

<div align="center">

![ChronoCast AI](https://img.shields.io/badge/ChronoCast-AI-00d4ff?style=for-the-badge&logo=bitcoin&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-REST-092E20?style=for-the-badge&logo=django&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![MLflow](https://img.shields.io/badge/MLflow-2.13-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-VM-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)

**A production-grade, end-to-end MLOps platform for Bitcoin price forecasting.**  
Live market intelligence · Model registry governance · Drift surveillance · ROI simulation

🌐 **Live Demo**: [http://chrono-cast.duckdns.org](http://chrono-cast.duckdns.org)

</div>

---

## 📸 Dashboard Preview

> **BTC Forecasting Dashboard** — Real-time predictions powered by MLflow production registry

![Dashboard Overview](docs/screenshots/Screenshot_2026-03-16_113922.png)

> **Prediction Charts** — BTC close history with forecast trajectory & market regime analysis

![Prediction Charts](docs/screenshots/Screenshot_2026-03-16_113930.png)

> **Model Performance & Drift Monitoring** — Champion-vs-challenger comparison + feature-level drift surveillance

![Model Performance](docs/screenshots/Screenshot_2026-03-16_113941.png)

> **MLflow Experiments & Model Leaderboard** — Full experiment tracking with ranked model registry

![Experiments Leaderboard](docs/screenshots/Screenshot_2026-03-16_113948.png)

> **A/B Testing & ROI Simulation** — Offline challenger evaluation + projected strategy PnL vs buy-and-hold

![AB Testing ROI](docs/screenshots/Screenshot_2026-03-16_113956.png)

---

## 🧠 What is ChronoCast AI?

ChronoCast AI is a **full-stack MLOps platform** that forecasts Bitcoin (BTC) closing prices using historical market data. It demonstrates a complete, production-grade ML engineering workflow:

- 📥 **Data Ingestion** — Live BTC OHLCV data from Binance public API
- ⚙️ **Feature Engineering** — Rolling MAs, volatility, lag features
- 🤖 **Model Training** — Linear Regression, ARIMA, LSTM (TensorFlow)
- 📊 **Experiment Tracking** — MLflow with full hyperparameter + metrics logging
- 🏆 **Model Registry** — Automatic champion promotion to Production stage
- 📡 **Drift Detection** — Evidently AI feature-level drift reports
- 🌐 **REST API** — Django REST Framework serving live inference
- 🎨 **React Dashboard** — Glassmorphism fintech UI with Chart.js visualizations

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    React 19 Frontend                     │
│         (Vite + TailwindCSS + Chart.js)                 │
│   Promise.all → /api/predictions, /experiments,         │
│   /monitoring/drift, /models, /roi, /ab-testing         │
└───────────────────┬─────────────────────────────────────┘
                    │ HTTP REST
┌───────────────────▼─────────────────────────────────────┐
│              Django REST Framework API                   │
│    Facade over MLflow SDK → clean JSON endpoints        │
│    Gunicorn WSGI · 3 workers · port 8000                │
└──────┬────────────────────────────┬─────────────────────┘
       │                            │
┌──────▼──────┐           ┌─────────▼──────────┐
│  PostgreSQL  │           │    MLflow Server    │
│  (App DB +  │◄──────────│  (Tracking +        │
│  MLflow DB) │           │   Model Registry)   │
└─────────────┘           └─────────┬───────────┘
                                    │ artifact store
                          ┌─────────▼───────────┐
                          │   ML Pipeline        │
                          │  (Offline Batch)     │
                          │  Linear · ARIMA ·   │
                          │  LSTM Models         │
                          └─────────────────────┘
```

**Deployment:** Docker Compose · Nginx reverse proxy · Azure VM (East Asia) · GitHub Actions CI/CD

---

## 🗂️ Project Structure

```
ChronoCast-Ai/
├── backend/                    # Django REST API
│   └── django_api/
│       ├── core/               # Settings & root URLs
│       ├── predictions/        # Live BTC inference endpoint
│       ├── experiments/        # MLflow run metrics
│       ├── monitoring/         # Evidently AI drift reports
│       ├── ab_testing/         # Champion-challenger evaluation
│       ├── roi/                # PnL & strategy simulation
│       └── model_registry_api/ # MLflow Model Registry wrapper
├── frontend/                   # Vite + React 19 SPA
│   ├── src/
│   │   ├── api.js              # Axios aggregator (Promise.all)
│   │   ├── App.jsx             # Main dashboard view
│   │   └── hooks/              # useDashboardData hook
│   ├── nginx.conf              # Container nginx config
│   └── Dockerfile              # Multi-stage build
├── ml_pipeline/                # Offline ML workload
│   ├── data_pipeline/          # Binance ingestion & cleaning
│   ├── training/               # Linear, ARIMA, LSTM trainers
│   ├── inference/              # Offline prediction wrappers
│   ├── monitoring/             # Drift detection execution
│   └── config.py               # Global pipeline config
├── docker/                     # Dockerfiles & init scripts
│   ├── mlflow.Dockerfile
│   └── postgres-init/          # DB initialization SQL
├── docker-compose.yml          # Full stack orchestration
├── run_pipeline.py             # Master ML pipeline orchestrator
└── .github/workflows/          # GitHub Actions CI/CD
    └── deploy.yml
```

---

## 🚀 Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | React 19, Vite, TailwindCSS, Chart.js | Interactive fintech dashboard |
| **Backend** | Python 3.10, Django 4, DRF | REST API & MLflow facade |
| **ML Core** | Scikit-learn, Statsmodels, TensorFlow | Linear, ARIMA, LSTM models |
| **MLOps** | MLflow 2.13 | Experiment tracking & model registry |
| **Monitoring** | Evidently AI | Data & target drift detection |
| **Database** | PostgreSQL 16 | App state + MLflow backend store |
| **DevOps** | Docker, Docker Compose, Nginx | Containerized deployment |
| **Cloud** | Azure VM (Standard B2als v2) | Production hosting |
| **CI/CD** | GitHub Actions | Auto-deploy on push to `main` |

---

## 📡 API Endpoints

| Endpoint | Description |
|---|---|
| `GET /api/predictions/` | Live BTC inference from production model |
| `GET /api/experiments/` | Latest 5 MLflow training runs + metrics |
| `GET /api/monitoring/drift/` | Evidently AI drift report (p-values per feature) |
| `GET /api/models/` | Model leaderboard + registry stages |
| `GET /api/ab-testing/` | Champion vs challenger traffic splits + confidence |
| `GET /api/roi/` | Equity curve: ChronoCast strategy vs buy-and-hold |

---

## ⚙️ Local Development Setup

### Prerequisites
- Docker & Docker Compose
- Python 3.10+
- Node.js 20+

### 1. Clone the repository
```bash
git clone https://github.com/anasjahagirdar/ChronoCast-Ai.git
cd ChronoCast-Ai
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env with your values
```

### 3. Start all services
```bash
docker-compose up -d --build
```

### 4. Run the ML pipeline
```bash
docker exec -it chronocast-ai_django_api_1 bash -c "cd /app && python run_pipeline.py"
```

### 5. Access the app
| Service | URL |
|---|---|
| React Dashboard | http://localhost:3000 |
| Django API | http://localhost:8000/api/ |
| MLflow UI | http://localhost:5000 |

---

## 🤖 ML Pipeline

The pipeline runs as an offline batch process orchestrated by `run_pipeline.py`:

```
Data Ingestion (Binance API)
        ↓
Preprocessing (imputation, normalization)
        ↓
Feature Engineering (MA7, MA30, volatility, lag_1, lag_7, return)
        ↓
┌───────────────────────────────┐
│  Train Linear Regression      │  → MLflow run + artifact
│  Train ARIMA (p=5, d=1, q=0) │  → MLflow run + artifact
│  Train LSTM (20 epochs)       │  → MLflow run + artifact
└───────────────────────────────┘
        ↓
Drift Detection (Evidently AI)
        ↓
Auto-promote best model → Production stage
```

**Model Performance (latest run):**
| Model | MAE | RMSE | Stage |
|---|---|---|---|
| Linear Regression | **407.36** | 629.74 | ✅ Production |
| LSTM | 3,821.31 | 4,967.75 | Production |
| ARIMA | 20,125.53 | 25,154.40 | Archived |

---

## 🔄 CI/CD Pipeline

Every push to `main` automatically deploys to the Azure VM via GitHub Actions:

```yaml
Push to main
    ↓
GitHub Actions (ubuntu-latest)
    ↓
SSH into Azure VM
    ↓
git pull origin main
    ↓
docker-compose down && docker-compose up -d --build
    ↓
Live at http://chrono-cast.duckdns.org
```

---

## 🔒 Security

- `DJANGO_DEBUG=false` in production
- Secrets managed via `.env` (never committed)
- UFW firewall: only ports 22, 80, 443 open
- Internal ports 8000, 5000, 5432 blocked from internet
- CORS locked to allowed origins only
- MLflow contained within Docker network

---

## 🌐 Production Deployment

**Live URL**: [http://chrono-cast.duckdns.org](http://chrono-cast.duckdns.org)

| Component | Details |
|---|---|
| Cloud | Azure VM — Standard B2als v2 (2 vCPU, 4GB RAM) |
| Region | East Asia |
| OS | Ubuntu 24.04 LTS |
| Reverse Proxy | Nginx |
| Process Manager | Docker Compose + crontab auto-restart |
| Domain | DuckDNS free subdomain |

---

## 📁 Environment Variables

```env
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS=your-domain.duckdns.org,your-ip
CORS_ALLOWED_ORIGINS=http://your-domain.duckdns.org
POSTGRES_DB=chronocast
POSTGRES_USER=chronocast
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
MLFLOW_TRACKING_URI=http://mlflow:5000
MLFLOW_EXPERIMENT_NAME=chronocast_btc_forecasting
CHRONOCAST_REFRESH_SECONDS=30
PORT=3000
NODE_ENV=production
```

---

## 👨‍💻 Author

**Anas Jahagirdar**  
Full Stack Developer & Generative AI Engineer

[![GitHub](https://img.shields.io/badge/GitHub-anasjahagirdar-181717?style=for-the-badge&logo=github)](https://github.com/anasjahagirdar)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/anasjahagirdar)

---

---

<div align="center">

**⭐ Star this repo if you found it useful!**

*Built with Python, Django, React, MLflow, Docker & deployed on Azure*

</div>
