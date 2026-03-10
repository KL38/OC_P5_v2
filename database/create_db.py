from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.sql import text
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone
import os
from dotenv import load_dotenv


Base = declarative_base()

# Connection string
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

class PredictionLog(Base):
    __tablename__ = 'predictions_log'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_employee = Column(Integer)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Inputs
    genre = Column(String)
    statut_marital = Column(String)
    departement = Column(String)
    poste = Column(String)
    domaine_etude = Column(String)
    frequence_deplacement = Column(String)
    heure_supplementaires = Column(String)
    age = Column(Integer)
    revenu_mensuel = Column(Integer)
    nombre_experiences_precedentes = Column(Integer)
    annee_experience_totale = Column(Integer)
    annees_dans_l_entreprise = Column(Integer)
    annees_dans_le_poste_actuel = Column(Integer)
    nb_formations_suivies = Column(Integer)
    distance_domicile_travail = Column(Integer)
    niveau_education = Column(Integer)
    annees_depuis_la_derniere_promotion = Column(Integer)
    annes_sous_responsable_actuel = Column(Integer)
    satisfaction_employee_environnement = Column(Integer)
    note_evaluation_precedente = Column(Float)
    satisfaction_employee_nature_travail = Column(Integer)
    satisfaction_employee_equipe = Column(Integer)
    satisfaction_employee_equilibre_pro_perso = Column(Integer)
    note_evaluation_actuelle = Column(Float)
    augementation_salaire_precedente = Column(String)

    # Outputs
    prediction = Column(String)
    probability_score = Column(Float)
    primary_driver = Column(String)
    strong_factor = Column(String)
    moderate_factor = Column(String)
    contributing_factor = Column(String)
    notable_factor = Column(String)
    unknown_category_warning = Column(String, nullable=True)
    ground_truth = Column(Integer, nullable=True)


class PredictionLogTest(Base):
    __tablename__ = 'predictions_log_test'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_employee = Column(Integer)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Inputs
    genre = Column(String)
    statut_marital = Column(String)
    departement = Column(String)
    poste = Column(String)
    domaine_etude = Column(String)
    frequence_deplacement = Column(String)
    heure_supplementaires = Column(String)
    age = Column(Integer)
    revenu_mensuel = Column(Integer)
    nombre_experiences_precedentes = Column(Integer)
    annee_experience_totale = Column(Integer)
    annees_dans_l_entreprise = Column(Integer)
    annees_dans_le_poste_actuel = Column(Integer)
    nb_formations_suivies = Column(Integer)
    distance_domicile_travail = Column(Integer)
    niveau_education = Column(Integer)
    annees_depuis_la_derniere_promotion = Column(Integer)
    annes_sous_responsable_actuel = Column(Integer)
    satisfaction_employee_environnement = Column(Integer)
    note_evaluation_precedente = Column(Float)
    satisfaction_employee_nature_travail = Column(Integer)
    satisfaction_employee_equipe = Column(Integer)
    satisfaction_employee_equilibre_pro_perso = Column(Integer)
    note_evaluation_actuelle = Column(Float)
    augementation_salaire_precedente = Column(String)

    # Outputs
    prediction = Column(String)
    probability_score = Column(Float)
    primary_driver = Column(String)
    strong_factor = Column(String)
    moderate_factor = Column(String)
    contributing_factor = Column(String)
    notable_factor = Column(String)
    unknown_category_warning = Column(String, nullable=True)
    ground_truth = Column(Integer, nullable=True)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Tables created successfully!")
   

