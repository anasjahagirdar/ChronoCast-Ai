# ChronoCast AI Project Report

## 1. Updated Folder Structure

```text
ChronoCast AI/
├── .github/workflows/ci.yml
├── .dockerignore
├── .env.example
├── backend/
│   ├── Dockerfile
│   └── django_api/
│       ├── ab_testing/
│       ├── core/
│       ├── experiments/
│       ├── model_registry_api/
│       ├── monitoring/
│       ├── predictions/
│       ├── requirements.txt
│       └── roi/
├── docker/
│   ├── mlflow.Dockerfile
│   └── postgres-init/
│       └── 01-create-mlflow-db.sql
├── docker-compose.yml
├── docs/
│   └── PROJECT_REPORT.md
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   ├── src/
│   │   ├── api.js
│   │   ├── App.jsx
│   │   ├── hooks/
│   │   │   └── useDashboardData.js
│   │   └── index.css
│   └── vite.config.js
├── ml_pipeline/
│   ├── config.py
│   ├── inference/
│   │   └── predict.py
│   ├── mlflow_pyfunc.py
│   ├── monitoring/
│   │   └── drift_detection/
│   │       ├── drift_detector.py
│   │       └── generate_report.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── data_service.py
│   │   ├── forecast_service.py
│   │   ├── mlflow_service.py
│   │   ├── monitoring_service.py
│   │   └── product_analytics.py
│   └── training/
│       ├── train_arima.py
│       ├── train_linear.py
│       └── train_lstm.py
├── mlops/
│   └── mlflow/
│       ├── mlflow_config.py
│       └── model_registry.py
└── run_pipeline.py
```

## 2. Files Created or Modified

### Backend and API

- `backend/django_api/core/settings.py`
- `backend/django_api/core/urls.py`
- `backend/django_api/core/asgi.py`
- `backend/django_api/core/wsgi.py`
- `backend/django_api/manage.py`
- `backend/django_api/requirements.txt`
- `backend/django_api/predictions/views.py`
- `backend/django_api/predictions/urls.py`
- `backend/django_api/predictions/tests.py`
- `backend/django_api/experiments/views.py`
- `backend/django_api/experiments/urls.py`
- `backend/django_api/monitoring/views.py`
- `backend/django_api/monitoring/urls.py`
- `backend/django_api/roi/views.py`
- `backend/django_api/roi/urls.py`
- `backend/django_api/ab_testing/views.py`
- `backend/django_api/ab_testing/urls.py`
- `backend/django_api/model_registry_api/__init__.py`
- `backend/django_api/model_registry_api/apps.py`
- `backend/django_api/model_registry_api/views.py`
- `backend/django_api/model_registry_api/urls.py`

### ML Pipeline and MLOps

- `ml_pipeline/config.py`
- `ml_pipeline/mlflow_pyfunc.py`
- `ml_pipeline/services/__init__.py`
- `ml_pipeline/services/data_service.py`
- `ml_pipeline/services/forecast_service.py`
- `ml_pipeline/services/mlflow_service.py`
- `ml_pipeline/services/monitoring_service.py`
- `ml_pipeline/services/product_analytics.py`
- `ml_pipeline/training/train_linear.py`
- `ml_pipeline/training/train_arima.py`
- `ml_pipeline/training/train_lstm.py`
- `ml_pipeline/inference/predict.py`
- `ml_pipeline/monitoring/drift_detection/drift_detector.py`
- `ml_pipeline/monitoring/drift_detection/generate_report.py`
- `mlops/mlflow/mlflow_config.py`
- `mlops/mlflow/model_registry.py`
- `run_pipeline.py`

### Frontend

- `frontend/src/api.js`
- `frontend/src/hooks/useDashboardData.js`
- `frontend/src/App.jsx`
- `frontend/src/index.css`
- `frontend/vite.config.js`
- `frontend/Dockerfile`
- `frontend/nginx.conf`

### DevOps and Docs

- `.dockerignore`
- `.env.example`
- `backend/Dockerfile`
- `docker/mlflow.Dockerfile`
- `docker/postgres-init/01-create-mlflow-db.sql`
- `docker-compose.yml`
- `.github/workflows/ci.yml`
- `docs/PROJECT_REPORT.md`

## 3. Major Features Implemented

### ML pipeline

- Centralized configuration for datasets, model paths, MLflow URIs, registry names, and forecast constants.
- Shared services for dataset loading, forecasting, MLflow querying, monitoring summaries, ROI simulation, and A/B test analytics.
- PyFunc wrappers for Linear Regression, ARIMA, and LSTM models so production inference can load registered MLflow artifacts consistently.
- `run_pipeline.py` updated to run ingestion, preprocessing, feature engineering, all three training jobs, and drift reporting.

### LSTM fix

- `ml_pipeline/training/train_lstm.py` now detects unsupported interpreters and re-launches itself with Python 3.10 when needed.
- Added a sliding-window dataset, MinMax scaling, stacked LSTM network, MAE/RMSE evaluation, MLflow logging, and MLflow model registry registration.
- The script supports `--epochs`, `--batch-size`, and `--window-size`.

### Django API

- `/api/predictions/` returns production forecast details, market overview, history, and forecast points.
- `/api/experiments/` exposes recent MLflow runs and summary metrics.
- `/api/monitoring/drift/` returns drift status, feature-level statistics, and report metadata.
- `/api/models/` exposes model leaderboard and registered versions.
- `/api/roi/` returns scenario-based ROI simulation and equity curves.
- `/api/ab-testing/` returns challenger analysis, confidence, lift, and simulated reward history.
- Added CORS support through `django-cors-headers`.

### Frontend dashboard

- Rebuilt the dashboard into a responsive fintech-style dark UI with glass panels, gradient lighting, and polling.
- Added charts for BTC forecast trajectory, model performance, A/B testing history, and ROI equity curves.
- Added model leaderboard, MLflow experiments table, drift feature cards, market overview metrics, and ROI scenario tiles.

### Monitoring

- Added a reusable drift summary service based on KS tests and mean-shift detection over recent windows.
- Drift reports now persist both JSON summary and HTML report output.

### DevOps

- Added Dockerfiles for backend and frontend plus an MLflow image for compose usage.
- Added `docker-compose.yml` for `django_api`, `react_dashboard`, `mlflow`, and `postgres`.
- Added GitHub Actions pipeline for tests, lint, model training, drift report generation, and Docker image builds.

## 4. Instructions to Run the System

### Local backend

1. Install Python 3.10 and create a working virtual environment.
2. Install dependencies:

```bash
pip install -r backend/django_api/requirements.txt -r ml_pipeline/requirements.txt
```

3. Export environment variables from `.env.example` as needed.
4. From `backend/django_api`, run:

```bash
python manage.py migrate
python manage.py runserver
```

### Local frontend

1. From `frontend`, install dependencies:

```bash
npm ci
```

2. Start the Vite dashboard:

```bash
npm run dev
```

### Local ML pipeline

1. Run preprocessing and feature generation if needed:

```bash
python -m ml_pipeline.data_pipeline.preprocess
python -m ml_pipeline.data_pipeline.feature_engineering
```

2. Train individual models:

```bash
python -m ml_pipeline.training.train_linear
python -m ml_pipeline.training.train_arima
python -m ml_pipeline.training.train_lstm
```

3. Or run the full orchestration:

```bash
python run_pipeline.py
```

### Docker Compose

```bash
docker compose up --build
```

Services:

- Django API: `http://localhost:8000`
- Frontend dashboard: `http://localhost:3000`
- MLflow: `http://localhost:5000`
- Postgres: `localhost:5432`

## 5. API Documentation

### `GET /api/predictions/`

Returns:

- latest BTC price
- predicted next close
- production model metadata
- MAE/RMSE
- drift status
- market snapshot
- price history
- forecast trajectory

### `GET /api/experiments/`

Returns:

- MLflow experiment name
- run summary
- recent experiment runs with params, metrics, and status

### `GET /api/monitoring/drift/`

Returns:

- drift status
- drift score
- reference/current windows
- drifted features
- feature-level p-values and mean shifts
- HTML report path

Query params:

- `refresh=true` forces drift recomputation

### `GET /api/models/`

Returns:

- production model snapshot
- leaderboard across registered model families
- model version list from MLflow registry

### `GET /api/roi/`

Returns:

- expected return
- signal
- fee and volatility assumptions
- bullish/base/defensive scenarios
- strategy vs buy-and-hold equity curves

Query params:

- `investment`
- `days`

### `GET /api/ab-testing/`

Returns:

- winner
- confidence
- lift percentage
- control/challenger variants
- simulated reward history

## 6. UI Features Overview

- Dark fintech visual system with glassmorphism and animated gradient atmosphere.
- Auto-refreshing dashboard polling every 30 seconds.
- Forecast line chart with projected BTC trajectory.
- Model performance bar chart for MAE/RMSE comparisons.
- Drift monitoring score bar and feature breakdown cards.
- MLflow experiment table with best-run summary.
- Model leaderboard cards with rank, stage, version, and error metrics.
- A/B testing section with traffic split doughnut and reward history chart.
- ROI simulation section with scenario cards and comparative equity curves.

## 7. ML Models Implemented

- Linear Regression using engineered technical features.
- ARIMA `(5, 1, 0)` on BTC close prices.
- LSTM with sliding windows, MinMax scaling, sequential train/test split, MAE/RMSE evaluation, and MLflow registration.

## 8. DevOps Infrastructure

- Backend container on Python 3.10 with Django, MLflow client support, and Gunicorn.
- Frontend container built with Vite and served by Nginx.
- Dedicated MLflow container with Postgres-backed metadata store and persisted artifacts volume.
- Postgres database for Django and MLflow compose deployment.
- GitHub Actions pipeline for backend tests, frontend lint/build, model training, drift report generation, and Docker builds.

## 9. Known Limitations

- The current environment used for this implementation does not have a working local Python interpreter, so runtime validation could not be completed here.
- Live exchange ingestion still depends on external Binance availability and network access.
- A/B testing analytics are simulation-based rather than traffic collected from real production users.
- The dashboard currently uses polling instead of WebSocket streaming.

## 10. Suggested Future Improvements

- Add real scheduler support for periodic ingestion, retraining, and drift refresh jobs.
- Add WebSocket streaming for live price and inference updates.
- Introduce authentication and role-based access control for MLflow and dashboard endpoints.
- Add richer unit and integration tests for ML services and frontend rendering.
- Add champion/challenger promotion automation based on offline validation thresholds.
- Add feature store style dataset versioning and backfill jobs.
