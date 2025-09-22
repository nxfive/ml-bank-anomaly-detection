# Bank Anomaly Detection 

Detect suspicious bank transactions using Isolation Forest and Local Outlier Factor models.<br> 
Includes a **FastAPI backend** for prediction and a **Streamlit frontend** for interactive UI.

[![Kaggle Dataset](https://img.shields.io/badge/Kaggle-Dataset-blue?logo=kaggle)](https://www.kaggle.com/code/nxfiv3/anomaly-detection-bank-transactions-nxfiv3)

---
## Features

- View available models and transactions via API
- Predict transactions using a single model or both models simultaneously
- Interactive Streamlit interface for entering transaction data and checking for fraud
- Data preprocessing and feature engineering steps included
- Tested with Pytest (API endpoints + core /src modules)

---

## Monitoring

- Metrics collection with Prometheus
- Dashboards and visualizations with Grafana
- Alerts and notifications with Alertmanager

---

## Tech Stack

- **Backend:** FastAPI, Numpy, Pandas, Scikit-learn
- **Frontend:** Streamlit
- **Testing:** Pytest
- **Deployment:** Docker, Azure DevOps
- **Monitoring:** Prometheus, Grafana, Alertmanager

---
## Quick Start
#### 1. Clone the repository
```bash
git clone https://github.com/nxfive/ml-bank-anomaly-detection.git
cd ml-bank-anomaly-detection
```
#### 2. Create a virtual environment and install dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # [Linux/Mac]
.venv\Scripts\activate     # [Windows]

pip install -r requirements.txt
```

#### 3. Build
```bash
python -m src.main
```

#### 4. Test
```bash
export ENV=dev
pytest -v
```

#### 5. Start FastAPI backend
```bash
python -m server.run
```

* Swagger UI: http://127.0.0.1:8000/docs
* Redoc UI: http://127.0.0.1:8000/redoc

#### 6. Start Streamlit frontend
```bash
streamlit run client/main.py  
```
---
### Run with Docker
```bash
docker-compose -f docker-compose.yml up --build
```
