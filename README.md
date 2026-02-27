---
title: HR Attrition Prediction API - Futurisys
colorFrom: blue
colorTo: green
sdk: docker
pinned: false

---
<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

<br />
<div align="center">
  <h3 align="center">HR Attrition Prediction API — Futurisys</h3>
  <p align="center">
    A production-grade REST API that predicts employee attrition using a Gradient Boosting pipeline with SHAP explainability, deployed on Hugging Face Spaces.
    <br />
    <a href="https://github.com/KL38/OC_P5_v2"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://huggingface.co/spaces/KLEB38/OC_P5">View Live Demo</a>
    &middot;
    <a href="https://github.com/KL38/OC_P5_v2/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/KL38/OC_P5_v2/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#running-tests">Running Tests</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

---

## About The Project

**Futurisys** is a tech consulting firm used as the business context for this OpenClassrooms Data Science project (Project 5). The objective is to help HR departments proactively identify employees at risk of attrition before they leave.

This project delivers a complete, containerised ML system:

- A **Gradient Boosting classifier** trained on HR data and serialised into a Scikit-Learn pipeline with automated preprocessing
- **Custom feature engineering** — overall satisfaction score, expertise inconsistency (department vs. study domain mismatch), managerial stagnation, and development stagnation signals
- A **custom classification threshold of 0.37** (tuned for recall on the attrition class rather than the default 0.50)
- A **FastAPI REST API** with full input validation via Pydantic
- **SHAP-based explainability** — every prediction is accompanied by the top 5 most influential features and their direction of impact
- A complete **CI/CD pipeline** via GitHub Actions that automatically deploys to Hugging Face Spaces on every push to `main`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Python][Python-badge]][Python-url]
* [![FastAPI][FastAPI-badge]][FastAPI-url]
* [![scikit-learn][sklearn-badge]][sklearn-url]
* [![pandas][pandas-badge]][pandas-url]
* [![SHAP][SHAP-badge]][SHAP-url]
* [![Docker][Docker-badge]][Docker-url]
* [![GitHub Actions][GHActions-badge]][GHActions-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Getting Started

### Prerequisites

- Python 3.13+
- Docker (for containerised deployment)
- Git

### Installation

#### Option 1 — Run locally with Python

1. Clone the repository
   ```sh
   git clone https://github.com/KL38/OC_P5_v2.git
   cd OC_P5_v2
   ```
2. Install dependencies
   ```sh
   pip install -r requirements.txt
   ```
3. Start the API
   ```sh
   uvicorn app.main:app --reload
   ```
   The API is available at `http://127.0.0.1:8000`. The interactive Swagger UI is at `http://127.0.0.1:8000/docs`.

#### Option 2 — Run with Docker

1. Build the image
   ```sh
   docker build -t futurisys-api .
   ```
2. Run the container
   ```sh
   docker run -p 7860:7860 futurisys-api
   ```
   The API is available at `http://localhost:7860`.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Usage

### Endpoints

| Method | Endpoint   | Description                              |
|--------|------------|------------------------------------------|
| `GET`  | `/`        | Health check — returns a welcome message |
| `POST` | `/predict` | Predicts employee attrition risk         |

### `POST /predict` — Input Schema

All fields use their **French alias** as the JSON key.

| JSON key                                | Type   | Accepted values / notes                                             |
|-----------------------------------------|--------|---------------------------------------------------------------------|
| `Genre`                                 | string | `"M"` or `"F"`                                                      |
| `Statut Marital`                        | string | `"Marié(e)"`, `"Célibataire"`, `"Divorcé(e)"`                      |
| `Département`                           | string | `"Consulting"`, `"Commercial"`, `"Ressources Humaines"`             |
| `Poste`                                 | string | `"Consultant"`, `"Manager"`, `"Tech Lead"`, …                       |
| `Domaine d'étude`                       | string | `"Infra & Cloud"`, `"Marketing"`, `"Ressources Humaines"`, …        |
| `Fréquence de déplacement`              | string | `"Aucun"`, `"Occasionnel"`, `"Frequent"`                            |
| `Heures supplémentaires`                | string | `"Oui"` or `"Non"`                                                  |
| `Âge`                                   | int    |                                                                     |
| `Revenu mensuel`                        | int    |                                                                     |
| `Nombre d'expériences précédentes`      | int    |                                                                     |
| `Années d'expérience totale`            | int    |                                                                     |
| `Années dans l'entreprise`              | int    |                                                                     |
| `Années dans le poste actuel`           | int    |                                                                     |
| `Nombre de formations suivies`          | int    |                                                                     |
| `Distance domicile-travail`             | int    |                                                                     |
| `Niveau d'éducation`                    | int    |                                                                     |
| `Années depuis la dernière promotion`   | int    |                                                                     |
| `Années sous responsable actuel`        | int    |                                                                     |
| `Satisfaction environnement`            | int    | 1–4                                                                 |
| `Satisfaction nature du travail`        | int    | 1–4                                                                 |
| `Satisfaction équipe`                   | int    | 1–4                                                                 |
| `Satisfaction équilibre pro/perso`      | int    | 1–4                                                                 |
| `Note évaluation précédente`            | int    | 1–4                                                                 |
| `Note évaluation actuelle`              | int    | 1–4                                                                 |
| `Augmentation salaire précédente`       | string | Percentage as string, e.g. `"18%"`                                  |

### Example Request

```bash
curl -X POST "http://localhost:7860/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Genre": "M",
    "Statut Marital": "Marié(e)",
    "Département": "Consulting",
    "Poste": "Consultant",
    "Domaine d'\''étude": "Infra & Cloud",
    "Fréquence de déplacement": "Occasionnel",
    "Heures supplémentaires": "Non",
    "Âge": 32,
    "Revenu mensuel": 4883,
    "Nombre d'\''expériences précédentes": 1,
    "Années d'\''expérience totale": 10,
    "Années dans l'\''entreprise": 10,
    "Années dans le poste actuel": 4,
    "Nombre de formations suivies": 3,
    "Distance domicile-travail": 7,
    "Niveau d'\''éducation": 2,
    "Années depuis la dernière promotion": 1,
    "Années sous responsable actuel": 1,
    "Satisfaction environnement": 4,
    "Note évaluation précédente": 3,
    "Satisfaction nature du travail": 3,
    "Satisfaction équipe": 1,
    "Satisfaction équilibre pro/perso": 3,
    "Note évaluation actuelle": 3,
    "Augmentation salaire précédente": "18%"
  }'
```

### Example Response

```json
{
  "statut_employe": "The staff has a LOW probability of resigning",
  "probability_score": 0.28,
  "model_threshold": 0.37,
  "note": "Decision based on a strategic threshold of 0.37, not 0.50",
  "top_5_factors": {
    "revenu_mensuel": {
      "interpretation": "Primary driver — decreases resignation risk",
      "feature_value": 4883.0
    },
    "annees_dans_l_entreprise": {
      "interpretation": "Strong factor — decreases resignation risk",
      "feature_value": 10.0
    },
    "statut_marital_Célibataire": {
      "interpretation": "Moderate factor — decreases resignation risk",
      "feature_value": "encoded"
    },
    "distance_domicile_travail": {
      "interpretation": "Contributing factor — decreases resignation risk",
      "feature_value": 7.0
    },
    "overall_satisfaction": {
      "interpretation": "Notable factor — decreases resignation risk",
      "feature_value": 2.75
    }
  }
}
```

### Response Schema

| Field             | Type   | Description                                                                 |
|-------------------|--------|-----------------------------------------------------------------------------|
| `statut_employe`  | string | Human-readable verdict: `"LOW probability of resigning"` or `"HIGH probability of resigning"` |
| `probability_score` | float | Raw model probability of resignation (0–1), rounded to 2 decimal places   |
| `model_threshold` | float  | Decision threshold applied — `0.37` (prediction is `HIGH` if score ≥ 0.37) |
| `note`            | string | Reminder that the threshold is strategically set to 0.37, not the default 0.50 |
| `top_5_factors`   | object | Top 5 features ranked by absolute SHAP value (most influential first)      |

Each entry in `top_5_factors` is keyed by the **feature name** and contains:

| Sub-field         | Type           | Description                                                                 |
|-------------------|----------------|-----------------------------------------------------------------------------|
| `interpretation`  | string         | Rank label (`Primary driver`, `Strong factor`, `Moderate factor`, `Contributing factor`, `Notable factor`) followed by the direction of impact (`increases` or `decreases resignation risk`) |
| `feature_value`   | float \| string | The actual value of that feature for this employee. Returns `"encoded"` for one-hot encoded categorical features (e.g. `statut_marital_Célibataire`) whose original value is lost after encoding |

> The interactive Swagger UI (auto-generated by FastAPI) is available at `/docs` on any running instance.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Running Tests

The test suite covers unit tests for feature engineering helpers and functional tests for all API endpoints, including valid predictions, input validation (HTTP 422), and warning logging.

```sh
pytest tests/ --cov=app
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Contact

Kevin Lebayle — [GitHub @KL38](https://github.com/KL38)

Project Link: [https://github.com/KL38/OC_P5_v2](https://github.com/KL38/OC_P5_v2)
Live Demo: [https://huggingface.co/spaces/KLEB38/OC_P5](https://huggingface.co/spaces/KLEB38/OC_P5)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Acknowledgments

* [FastAPI](https://fastapi.tiangolo.com/) — high-performance async web framework
* [SHAP](https://shap.readthedocs.io/) — model explainability
* [scikit-learn](https://scikit-learn.org/) — ML pipeline and Gradient Boosting classifier
* [Hugging Face Spaces](https://huggingface.co/spaces) — Docker-based free deployment
* [othneildrew/Best-README-Template](https://github.com/othneildrew/Best-README-Template) — README structure

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/KL38/OC_P5_v2.svg?style=for-the-badge
[contributors-url]: https://github.com/KL38/OC_P5_v2/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/KL38/OC_P5_v2.svg?style=for-the-badge
[forks-url]: https://github.com/KL38/OC_P5_v2/network/members
[stars-shield]: https://img.shields.io/github/stars/KL38/OC_P5_v2.svg?style=for-the-badge
[stars-url]: https://github.com/KL38/OC_P5_v2/stargazers
[issues-shield]: https://img.shields.io/github/issues/KL38/OC_P5_v2.svg?style=for-the-badge
[issues-url]: https://github.com/KL38/OC_P5_v2/issues
[Python-badge]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[FastAPI-badge]: https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white
[FastAPI-url]: https://fastapi.tiangolo.com/
[sklearn-badge]: https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white
[sklearn-url]: https://scikit-learn.org/
[pandas-badge]: https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white
[pandas-url]: https://pandas.pydata.org/
[SHAP-badge]: https://img.shields.io/badge/SHAP-FF6B6B?style=for-the-badge&logoColor=white
[SHAP-url]: https://shap.readthedocs.io/
[Docker-badge]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
[GHActions-badge]: https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white
[GHActions-url]: https://github.com/features/actions
