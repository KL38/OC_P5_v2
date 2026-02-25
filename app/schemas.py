from pydantic import BaseModel, Field
from typing import Literal


class EmployeeInput(BaseModel):
    genre: Literal["M", "F"] = Field(..., alias="Genre")
    statut_marital: str = Field(..., alias="Statut Marital")
    departement: str = Field(..., alias="Département")
    poste: str = Field(..., alias="Poste")
    domaine_etude: str = Field(..., alias="Domaine d'étude")
    frequence_deplacement: str = Field(..., alias="Fréquence de déplacement")
    heure_supplementaires: Literal["Oui", "Non"] = Field(..., alias="Heures supplémentaires")
    age: int = Field(..., alias="Âge")
    revenu_mensuel: int = Field(..., alias="Revenu mensuel")
    nombre_experiences_precedentes: int = Field(..., alias="Nombre d'expériences précédentes")
    annee_experience_totale: int = Field(..., alias="Années d'expérience totale")
    annees_dans_l_entreprise: int = Field(..., alias="Années dans l'entreprise")
    annees_dans_le_poste_actuel: int = Field(..., alias="Années dans le poste actuel")
    nb_formations_suivies: int = Field(..., alias="Nombre de formations suivies")
    distance_domicile_travail: int = Field(..., alias="Distance domicile-travail")
    niveau_education: int = Field(..., alias="Niveau d'éducation")
    annees_depuis_la_derniere_promotion: int = Field(..., alias="Années depuis la dernière promotion")
    annes_sous_responsable_actuel: int = Field(..., alias="Années sous responsable actuel")
    satisfaction_employee_environnement: int = Field(..., alias="Satisfaction environnement")
    note_evaluation_precedente: int = Field(..., alias="Note évaluation précédente")
    satisfaction_employee_nature_travail: int = Field(..., alias="Satisfaction nature du travail")
    satisfaction_employee_equipe: int = Field(..., alias="Satisfaction équipe")
    satisfaction_employee_equilibre_pro_perso: int = Field(..., alias="Satisfaction équilibre pro/perso")
    note_evaluation_actuelle: int = Field(..., alias="Note évaluation actuelle")
    augementation_salaire_precedente: str = Field(..., alias="Augmentation salaire précédente")

    model_config = {"populate_by_name": True}