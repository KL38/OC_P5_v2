from fastapi.testclient import TestClient
from app.main import app
import logging

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message":"Welcome to the FUTURISYS HR predictor API"}

def test_predict_valid():
    payload = {
        "Genre": "M",
        "Statut Marital": "Marié(e)",
        "Département": "Consulting",
        "Poste": "Consultant",
        "Domaine d'étude": "Infra & Cloud",
        "Fréquence de déplacement": "Occasionnel",
        "Heures supplémentaires": "Non",
        "Âge": 32,
        "Revenu mensuel": 4883,
        "Nombre d'expériences précédentes": 1,
        "Années d'expérience totale": 10,
        "Années dans l'entreprise": 10,
        "Années dans le poste actuel": 4,
        "Nombre de formations suivies": 3,
        "Distance domicile-travail": 7,
        "Niveau d'éducation": 2,
        "Années depuis la dernière promotion": 1,
        "Années sous responsable actuel": 1,
        "Satisfaction environnement": 4,
        "Note évaluation précédente": 3,
        "Satisfaction nature du travail": 3,
        "Satisfaction équipe": 1,
        "Satisfaction équilibre pro/perso": 3,
        "Note évaluation actuelle": 3,
        "Augmentation salaire précédente": "18%"
    }

    response = client.post("/predict", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["statut_employe"] == "The staff has a LOW probability of resigning"
    assert data["probability_score"] == 0.28
    assert data["model_threshold"] == 0.37

    # Top 5 SHAP factors
    factors = data["top_5_factors"]
    assert list(factors.keys()) == [
        "revenu_mensuel",
        "annees_dans_l_entreprise",
        "statut_marital_Célibataire",
        "distance_domicile_travail",
        "overall_satisfaction"
    ]

    # Interpretations
    assert factors["revenu_mensuel"]["interpretation"] == "Primary driver — decreases resignation risk"
    assert factors["annees_dans_l_entreprise"]["interpretation"] == "Strong factor — decreases resignation risk"
    assert factors["statut_marital_Célibataire"]["interpretation"] == "Moderate factor — decreases resignation risk"
    assert factors["distance_domicile_travail"]["interpretation"] == "Contributing factor — decreases resignation risk"
    assert factors["overall_satisfaction"]["interpretation"] == "Notable factor — decreases resignation risk"

    # Feature values
    assert factors["revenu_mensuel"]["feature_value"] == 4883.0
    assert factors["annees_dans_l_entreprise"]["feature_value"] == 10.0
    assert factors["statut_marital_Célibataire"]["feature_value"] == "encoded"

    assert factors["distance_domicile_travail"]["feature_value"] == 7.0
    assert factors["overall_satisfaction"]["feature_value"] == 2.75 


class Test_Predict_422:

    def test_predict_422_wrong_input(self):
        payload = {
            "Genre": "X", # INSERTION OF WRONG INPUT F OR M 
            "Statut Marital": "Marié(e)",
            "Département": "Consulting",
            "Poste": "Consultant",
            "Domaine d'étude": "Infra & Cloud",
            "Fréquence de déplacement": "Occasionnel",
            "Heures supplémentaires": "Non",
            "Âge": 32,
            "Revenu mensuel": 4883,
            "Nombre d'expériences précédentes": 1,
            "Années d'expérience totale": 10,
            "Années dans l'entreprise": 10,
            "Années dans le poste actuel": 4,
            "Nombre de formations suivies": 3,
            "Distance domicile-travail": 7,
            "Niveau d'éducation": 2,
            "Années depuis la dernière promotion": 1,
            "Années sous responsable actuel": 1,
            "Satisfaction environnement": 4,
            "Note évaluation précédente": 3,
            "Satisfaction nature du travail": 3,
            "Satisfaction équipe": 1,
            "Satisfaction équilibre pro/perso": 3,
            "Note évaluation actuelle": 3,
            "Augmentation salaire précédente": "18%"
        }
        response = client.post("/predict", json=payload)
        assert response.status_code == 422


    def test_predict_422_wrong_type_str(self):
        payload = {
            "Genre": "M",  
            "Statut Marital": "Marié(e)",
            "Département": "Consulting",
            "Poste": "Consultant",
            "Domaine d'étude": "Infra & Cloud",
            "Fréquence de déplacement": "Occasionnel",
            "Heures supplémentaires": "Non",
            "Âge": "trente", #EXPECTED INT
            "Revenu mensuel": 4883,
            "Nombre d'expériences précédentes": 1,
            "Années d'expérience totale": 10,
            "Années dans l'entreprise": 10,
            "Années dans le poste actuel": 4,
            "Nombre de formations suivies": 3,
            "Distance domicile-travail": 7,
            "Niveau d'éducation": 2,
            "Années depuis la dernière promotion": 1,
            "Années sous responsable actuel": 1,
            "Satisfaction environnement": 4,
            "Note évaluation précédente": 3,
            "Satisfaction nature du travail": 3,
            "Satisfaction équipe": 1,
            "Satisfaction équilibre pro/perso": 3,
            "Note évaluation actuelle": 3,
            "Augmentation salaire précédente": "18%"
        }
        response = client.post("/predict", json=payload)
        assert response.status_code == 422

    def test_predict_422_wrong_type_int(self):
        payload = {
            "Genre": "M",  
            "Statut Marital": "Marié(e)", 
            "Département": "Consulting",
            "Poste": "Consultant",
            "Domaine d'étude": "Infra & Cloud",
            "Fréquence de déplacement": "Occasionnel",
            "Heures supplémentaires": "Non",
            "Âge": 32,
            "Revenu mensuel": 4883.12,#WRONG TYPE, should be int 
            "Nombre d'expériences précédentes": 1,
            "Années d'expérience totale": 10,
            "Années dans l'entreprise": 10,
            "Années dans le poste actuel": 4,
            "Nombre de formations suivies": 3,
            "Distance domicile-travail": 7,
            "Niveau d'éducation": 2,
            "Années depuis la dernière promotion": 1,
            "Années sous responsable actuel": 1,
            "Satisfaction environnement": 4,
            "Note évaluation précédente": 3,
            "Satisfaction nature du travail": 3,
            "Satisfaction équipe": 1,
            "Satisfaction équilibre pro/perso": 3,
            "Note évaluation actuelle": 3,
            "Augmentation salaire précédente": "18%"
        }
        response = client.post("/predict", json=payload)
        assert response.status_code == 422

    def test_predict_422_incomplete_json(self):
        payload = {
            "Genre": "M",  
            "Statut Marital": "Marié(e)", 
            "Département": "Consulting",
            "Poste": "Consultant",
            "Domaine d'étude": "Infra & Cloud",
            "Fréquence de déplacement": "Occasionnel",
            "Heures supplémentaires": "Non",
            "Âge": 32,
            "Revenu mensuel": 4883, 
            "Nombre d'expériences précédentes": 1,
            "Années d'expérience totale": 10,
            "Années dans l'entreprise": 10,
            "Années dans le poste actuel": 4,
            "Nombre de formations suivies": 3,
            "Niveau d'éducation": 2, #MISSING "Distance domicile-travail"
            "Années depuis la dernière promotion": 1,
            "Années sous responsable actuel": 1,
            "Satisfaction environnement": 4,
            "Note évaluation précédente": 3,
            "Satisfaction nature du travail": 3,
            "Satisfaction équipe": 1,
            "Satisfaction équilibre pro/perso": 3,
            "Note évaluation actuelle": 3,
            "Augmentation salaire précédente": "18%"
        }
        response = client.post("/predict", json=payload)
        assert response.status_code == 422

def test_logging(caplog):
    payload = {
        "Genre": "M",  
        "Statut Marital": "Marié(e)", 
        "Département": "Logistique", #check wrong department
        "Poste": "Consultant",
        "Domaine d'étude": "Infra & Cloud",
        "Fréquence de déplacement": "Occasionnel",
        "Heures supplémentaires": "Non",
        "Âge": 32,
        "Revenu mensuel": 4883, 
        "Nombre d'expériences précédentes": 1,
        "Années d'expérience totale": 10,
        "Années dans l'entreprise": 10,
        "Années dans le poste actuel": 4,
        "Nombre de formations suivies": 3,
        "Distance domicile-travail": 7,
        "Niveau d'éducation": 2, 
        "Années depuis la dernière promotion": 1,
        "Années sous responsable actuel": 1,
        "Satisfaction environnement": 4,
        "Note évaluation précédente": 3,
        "Satisfaction nature du travail": 3,
        "Satisfaction équipe": 1,
        "Satisfaction équilibre pro/perso": 3,
        "Note évaluation actuelle": 3,
        "Augmentation salaire précédente": "18%"
    }

    with caplog.at_level(logging.WARNING):
        response = client.post("/predict", json=payload)

    assert response.status_code == 200  # l'API répond quand même
    assert "Unknown value 'Logistique' for column 'departement'" in caplog.text

