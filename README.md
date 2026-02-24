---
title: HR Attrition Prediction API - Futurisys
colorFrom: blue
colorTo: green
sdk: docker
pinned: false

---
# HR Attrition Prediction API - Futurisys

This project provides a professional-grade REST API designed to predict employee attrition for **Futurisys**. 
It uses a Machine Learning pipeline to analyze employee data and provide actionable insights for HR departments.

## Project Overview
The objective is to identify employees at risk of leaving the company by analyzing HR features.

**Key Features:**
- **Machine Learning Pipeline:** A robust model (Gradient Boosting/Random Forest) integrated with automated preprocessing.
- **FastAPI Framework:** High-performance API with built-in validation and asynchronous support.

---

## Project Structure

```text
.
├── app/
│   ├── main.py              # Core API logic and Pydantic schemas
│   └── pipeline_rh.joblib    # Serialized Scikit-Learn pipeline (Model + Scalers)
├── notebooks/               # Research, EDA, and model training notebooks
├── .gitignore               # Ensures clean version control by ignoring temp files
├── requirements.txt         # List of Python dependencies
└── README.md                # Project documentation

```
## Installation & Setup

1. Prerequisites

  Python 3.8+
  Git

3. Clone the Repository

  git clone <your-repository-url>
  cd <your-project-folder>

3. Install dependencies

  pip install -r requirements.txt

## Usage

### Running the API

## API Endpoints

GET / 

POST /predict

## Author
Kevin L. - Data Science & Machine Learning Student