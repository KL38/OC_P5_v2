from fastapi import FastAPI
import pandas as pd
import joblib
from app.schemas import EmployeeInput
import shap

app = FastAPI() # On crée l'outil (le guichet)

# Au démarrage, on charge ton pipeline
model = joblib.load('app/pipeline_rh.joblib')

def inconsistency(df):
    if df["departement"] == "Commercial":
        if (
            df["domaine_etude"]
            == "Marketing"
            # or df["domaine_etude"] == "Transformation Digitale"
            # or df["domaine_etude"] == "Infra & Cloud"
            # or df["domaine_etude"] == "Entrepreunariat"
        ):
            return 0
        else:
            return 1

    elif df["departement"] == "Consulting":
        if (
            df["domaine_etude"] == "Infra & Cloud"
            or df["domaine_etude"] == "Transformation Digitale"
            # or df["domaine_etude"] == "Entrepreunariat"
        ):
            return 0
        else:
            return 1

    elif df["departement"] == "Ressources Humaines":
        if (
            df["domaine_etude"] == "Ressources Humaines"
            or df["domaine_etude"] == "Entrepreunariat"
        ):
            return 0
        else:
            return 1

def promotion(df):
    if (
        df["annes_sous_responsable_actuel"] > 4
        and df["annees_depuis_la_derniere_promotion"] > 4
    ):
        return 1
    else:
        return 0

def developpement(df):
    if df["annees_dans_l_entreprise"] == 0:
        return 0
    elif df["annees_dans_l_entreprise"] >= 2 and df["nb_formations_suivies"] <= 1:
        return 1
    else:
        return 0

def depart(x):
    if x == 0:
        return "The staff has a LOW probability of resigning"
    if x==1:
        return "The staff has a HIGH probability of resigning"


@app.get("/") # La page d'accueil de ton API
def read_root():
    return {"message": "Welcome to the FUTURISYS HR predictor API"}

@app.post("/predict")
def predict(data: EmployeeInput):
    # 1. On transforme le dictionnaire reçu en DataFrame pandas
    df = pd.DataFrame([data.model_dump()])

    # Encodage binaire non inclus dans le pipeline: 
    df['genre']= df["genre"].map({"M": 1, "F": 0})
    df['heure_supplementaires']= df["heure_supplementaires"].map({"Oui": 1, "Non": 0})
    
    # Changement de type pour augmentation salaire precedente (non inclus dans pipeline)
    df["augementation_salaire_precedente"] = df["augementation_salaire_precedente"].apply(lambda x: float(x[:-1]) / 100)
    dft = df[[item for item in df.columns if item.startswith("satisfaction")]].copy()
    dft.loc[:, "overall_satisfaction"] = dft.mean(
        axis=1
    )
    df["overall_satisfaction"] = dft["overall_satisfaction"].copy()
    df["expertise_inconcistency"] = df.apply(inconsistency, axis=1)
    df["managarial_stagnation"] = df.apply(promotion, axis=1)
    df["developpement_stagnation"] = df.apply(developpement, axis=1)
    
    # 2. On utilise le pipeline pour faire la prédiction
    proba = model.predict_proba(df)[0][1]
    prediction = 1 if proba >= 0.37 else 0

    # 3. SHAP explanation
    preprocessor_step = model[:-1]
    gb_step = model[-1]

    X_preprocessed = preprocessor_step.transform(df)
    explainer = shap.TreeExplainer(gb_step)
    shap_values_obj = explainer(X_preprocessed)

    feature_names = [name.split("__")[-1] for name in preprocessor_step.get_feature_names_out()]
    shap_series = pd.Series(shap_values_obj.values[0], index=feature_names)
    top_factors = shap_series.abs().nlargest(5)

    def interpret_shap(rank: int, value: float) -> str:
        intensity = {
            0: "Primary driver",
            1: "Strong factor",
            2: "Moderate factor",
            3: "Contributing factor",
            4: "Notable factor"
        }
        direction = "increases resignation risk" if value > 0 else "decreases resignation risk"
        return f"{intensity[rank]} — {direction}"

        # 3. On renvoie le résultat au format JSON
    return {
        "statut_employe": depart(prediction),
        "probability_score": round(proba, 2),
        "model_threshold": 0.37,
        "note": "Decision based on a strategic threshold of 0.37, not 0.50",
        "top_5_factors": {
            factor: {
                "interpretation": interpret_shap(rank, shap_series[factor]),
                "feature_value": float(df[factor].values[0]) if factor in df.columns else "encoded"
            }
            for rank, factor in enumerate(top_factors.index)
        }
    }
