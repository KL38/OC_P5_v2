from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.sql import text
from sqlalchemy.orm import declarative_base
from datetime import datetime
import os
from dotenv import load_dotenv


Base = declarative_base()

# Connection string
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

class EmployeeSirh(Base):
    __tablename__ = 'employees_sirh'
    
    id_employee = Column(Integer, primary_key=True)
    age = Column(Integer)
    genre = Column(String)
    revenu_mensuel = Column(Integer)
    statut_marital = Column(String)
    departement = Column(String)
    poste = Column(String)
    nombre_experiences_precedentes = Column(Integer)
    nombre_heures_travaillees = Column(Integer)
    annee_experience_totale = Column(Integer)
    annees_dans_l_entreprise = Column(Integer)
    annees_dans_le_poste_actuel = Column(Integer)

class EmployeeEval(Base):
    __tablename__ = 'employees_eval'
    
    eval_number = Column(Integer, primary_key=True)
    satisfaction_employee_environnement = Column(Integer)
    note_evaluation_precedente = Column(Integer)
    niveau_hierarchique_poste = Column(Integer)
    satisfaction_employee_nature_travail = Column(Integer)
    satisfaction_employee_equipe = Column(Integer)
    satisfaction_employee_equilibre_pro_perso = Column(Integer)
    note_evaluation_actuelle = Column(Integer)
    heure_supplementaires = Column(String)
    augementation_salaire_precedente = Column(String)


class EmployeeSondage(Base):
    __tablename__ = 'employees_sondage'
    
    code_sondage = Column(Integer, primary_key=True)
    a_quitte_l_entreprise = Column(String)
    nombre_participation_pee = Column(Integer)
    nb_formations_suivies = Column(Integer)
    nombre_employee_sous_responsabilite = Column(Integer)
    distance_domicile_travail = Column(Integer)
    niveau_education = Column(Integer)
    domaine_etude = Column(String)
    ayant_enfants = Column(String)
    frequence_deplacement = Column(String)
    annees_depuis_la_derniere_promotion = Column(Integer)
    annes_sous_responsable_actuel = Column(Integer)


class PredictionLog(Base):
    __tablename__ = 'predictions_log'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_employee = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

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
   

