from fastapi import FastAPI
import joblib

app = FastAPI() # On crée l'outil (le guichet)

# Au démarrage, on charge ton pipeline
model = joblib.load('app/pipeline_rh.joblib')

@app.get("/") # La page d'accueil de ton API
def read_root():
    return {"message": "Bienvenue sur l'API RH de Futurisys"}

@app.post("/predict")
def predict(data: dict):
    # 1. On transforme le dictionnaire reçu en DataFrame pandas
    df = pd.DataFrame([data])
    
    # 2. On utilise le pipeline pour faire la prédiction
    prediction = model.predict(df)
    
    # 3. On renvoie le résultat au format JSON
    return {
        "statut_employe": int(prediction[0])
    }