# ChronoCast AI

ChronoCast AI is a production-style machine learning platform that forecasts Bitcoin prices using historical market data.

The system demonstrates a complete **ML engineering workflow** including data pipelines, model training, experiment tracking, monitoring, and a live analytics dashboard.

---

## 🚀 Features

• BTC price forecasting using multiple models  
• MLflow experiment tracking  
• Model registry and versioning  
• Drift detection with Evidently AI  
• Django REST API for predictions  
• React fintech-style dashboard  
• A/B testing framework for models  
• ROI simulation for trading strategies  
• Docker deployment ready  
• CI/CD pipeline support  

---

## 🧠 Machine Learning Models

The system supports:

| Model | Purpose |
|------|------|
| Linear Regression | Baseline forecasting |
| ARIMA | Time-series statistical model |
| LSTM | Deep learning time-series model |

Metrics tracked:

- MAE
- RMSE

---

## 🏗 Architecture

```
Binance API
      ↓
Data Ingestion Pipeline
      ↓
Data Preprocessing
      ↓
Feature Engineering
      ↓
Model Training
      ↓
MLflow Experiment Tracking
      ↓
Model Registry
      ↓
Django REST API
      ↓
React Dashboard
      ↓
Monitoring & Drift Detection
```

---

## 📊 Dashboard

The React dashboard provides:

- BTC price overview
- Model prediction results
- Model leaderboard
- Experiment comparison
- Drift monitoring
- ROI simulation

---

## ⚙️ Tech Stack

### Backend
- Python
- Django
- Django REST Framework

### Machine Learning
- Scikit-learn
- Statsmodels
- TensorFlow / PyTorch
- MLflow

### Frontend
- React
- Vite
- TailwindCSS
- Chart.js

### Monitoring
- Evidently AI

### Infrastructure
- Docker
- GitHub Actions

---

## 📁 Project Structure

```
ChronoCast-AI
│
├── backend
│   └── django_api
│       ├── core
│       ├── predictions
│       ├── experiments
│       ├── monitoring
│       ├── ab_testing
│       └── roi
│
├── frontend
│   └── react_dashboard
│
├── ml_pipeline
│   ├── data_pipeline
│   ├── training
│   ├── inference
│   └── monitoring
│
├── mlops
│   └── mlflow
│
├── docker
├── docs
└── run_pipeline.py
```

---

## 🖥 Running the Project

### 1️⃣ Start Backend

```
cd backend/django_api
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

### 2️⃣ Start Frontend

```
cd frontend
npm install
npm run dev
```

---

### 3️⃣ Start MLflow

```
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --port 5000
```

---

## 🌐 Services

| Service | URL |
|------|------|
| React Dashboard | http://localhost:5173 |
| Django API | http://127.0.0.1:8000 |
| MLflow UI | http://localhost:5000 |

---

## 🔄 ML Pipeline

You can retrain the models using:

```
python run_pipeline.py
```

Pipeline steps:

1. Data ingestion from Binance
2. Data preprocessing
3. Feature engineering
4. Model training
5. Experiment logging to MLflow
6. Drift detection monitoring

---

## 📈 Future Improvements

- Real-time BTC price streaming
- Automated model retraining
- Advanced trading strategy simulation
- Kubernetes deployment
- Live experiment comparison dashboard

---

## 👨‍💻 Author

Anas

Machine Learning & Full Stack Development Project