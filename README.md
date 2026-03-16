# 🏦 LoanSense — AI Powered Credit Decision Engine

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> A professional Machine Learning web application that predicts loan approval decisions using Logistic Regression — built with Python, Scikit-Learn, and Streamlit.

---

## 📸 Screenshots

### 🖥️ Main Dashboard
![LoanSense Dashboard](screenshots/dashboard.png)

### ✅ Loan Approved
![Loan Approved](screenshots/approved.png)

### ❌ Loan Rejected
![Loan Rejected](screenshots/rejected.png)

---

## 🚀 Features

- 🤖 **AI-Powered Predictions** — Logistic Regression model trained on 614 real loan applicants
- 🎨 **Beautiful UI** — Blue & Gold professional banking theme built with Streamlit
- 📊 **Data Visualizations** — Interactive charts showing loan approval trends and credit history analysis
- 📈 **Model Metrics** — Real-time display of model accuracy, features analyzed, and training records
- ⚡ **Instant Results** — Get loan approval decisions in seconds with confidence scores
- 🧹 **Clean Pipeline** — Full data preprocessing including missing value handling and feature encoding

---

## 🧠 How It Works

```
User fills in applicant details (Income, Credit History, Loan Amount, etc.)
                        ↓
Data is preprocessed and scaled using StandardScaler
                        ↓
Logistic Regression model analyzes 11 features
                        ↓
Prediction: ✅ LOAN APPROVED or ❌ LOAN REJECTED + Confidence Score
```

---

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| **Algorithm** | Logistic Regression |
| **Training Samples** | 491 |
| **Testing Samples** | 123 |
| **Accuracy** | 79% |
| **Precision (Approved)** | 76% |
| **Recall (Approved)** | 99% |

---

## 📁 Project Structure

```
loan_prediction/
│
├── app.py                  ← Streamlit frontend (main app)
├── loan_prediction.py      ← ML model training & evaluation
├── train.csv               ← Kaggle dataset
├── loan_analysis.png       ← Generated visualization
└── README.md               ← You are here!
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/loan-prediction.git
cd loan-prediction
```

### 2️⃣ Install Required Libraries

```bash
pip install pandas numpy scikit-learn matplotlib seaborn streamlit
```

### 3️⃣ Download the Dataset

Download `train.csv` from Kaggle:
👉 [Loan Prediction Problem Dataset](https://www.kaggle.com/datasets/altruistdelhite04/loan-prediction-problem-dataset)

Place `train.csv` in the project root folder.

### 4️⃣ Run the App

```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501` 🎉

---

## 🔧 Run the ML Model Only

If you just want to train and evaluate the model without the UI:

```bash
python loan_prediction.py
```

This will:
- Load and clean the dataset
- Train the Logistic Regression model
- Print accuracy, confusion matrix, and classification report
- Generate and save `loan_analysis.png`

---

## 📋 Input Features

| Feature | Description | Type |
|---------|-------------|------|
| Gender | Male / Female | Categorical |
| Married | Yes / No | Categorical |
| Dependents | 0 / 1 / 2 / 3+ | Categorical |
| Education | Graduate / Not Graduate | Categorical |
| Self Employed | Yes / No | Categorical |
| Applicant Income | Monthly income (₹) | Numerical |
| Coapplicant Income | Co-applicant monthly income (₹) | Numerical |
| Loan Amount | Requested loan amount (thousands) | Numerical |
| Loan Term | Repayment period (months) | Numerical |
| Credit History | Good (1.0) / Bad (0.0) | Binary |
| Property Area | Urban / Semiurban / Rural | Categorical |

---

## 💡 Key Insights from the Data

- **Credit History** is the most powerful factor — applicants with good credit history are approved at a much higher rate
- **Income alone** does not determine approval — credit history plays a bigger role
- **~68%** of applicants in the dataset were approved for loans

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python** | Core programming language |
| **Pandas** | Data loading and manipulation |
| **NumPy** | Numerical computations |
| **Scikit-Learn** | Machine learning model |
| **Matplotlib & Seaborn** | Data visualization |
| **Streamlit** | Web application frontend |

---

## 📌 Dataset

This project uses the **Loan Prediction Problem Dataset** from Kaggle.

- **Source:** [Kaggle — altruistdelhite04](https://www.kaggle.com/datasets/altruistdelhite04/loan-prediction-problem-dataset)
- **Records:** 614 loan applicants
- **Features:** 13 columns
- **Target:** Loan_Status (Y = Approved, N = Rejected)

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

Built with ❤️ as a Machine Learning portfolio project.

If you found this helpful, please ⭐ star the repository!

---

> **Note:** This project is for educational purposes. Real-world loan decisions involve many more factors and should not be based solely on ML model predictions.
