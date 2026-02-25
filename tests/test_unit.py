import pandas as pd
import pytest
from app.main import depart, inconsistency, promotion, developpement, interpret_shap
import os


# ---------------------------------------------------------------------------
# depart
# ---------------------------------------------------------------------------

def test_depart():
    assert depart(0) == "The staff has a LOW probability of resigning"
    assert depart(1) == "The staff has a HIGH probability of resigning"

# ---------------------------------------------------------------------------
# inconsistency
# The function is called via df.apply(inconsistency, axis=1), so each input
# is a pandas Series representing a single row.
# ---------------------------------------------------------------------------

class TestInconsistency:
    # --- Commercial ---
    def test_commercial_marketing_is_consistent(self):
        row = pd.Series({"departement": "Commercial", "domaine_etude": "Marketing"})
        assert inconsistency(row) == 0

    def test_commercial_infra_is_inconsistent(self):
        row = pd.Series({"departement": "Commercial", "domaine_etude": "Infra & Cloud"})
        assert inconsistency(row) == 1

    def test_commercial_rh_is_inconsistent(self):
        row = pd.Series({"departement": "Commercial", "domaine_etude": "Ressources Humaines"})
        assert inconsistency(row) == 1

    def test_commercial_transformation_is_inconsistent(self):
        row = pd.Series({"departement": "Commercial", "domaine_etude": "Transformation Digitale"})
        assert inconsistency(row) == 1

    # --- Consulting ---
    def test_consulting_infra_is_consistent(self):
        row = pd.Series({"departement": "Consulting", "domaine_etude": "Infra & Cloud"})
        assert inconsistency(row) == 0

    def test_consulting_transformation_is_consistent(self):
        row = pd.Series({"departement": "Consulting", "domaine_etude": "Transformation Digitale"})
        assert inconsistency(row) == 0

    def test_consulting_marketing_is_inconsistent(self):
        row = pd.Series({"departement": "Consulting", "domaine_etude": "Marketing"})
        assert inconsistency(row) == 1

    def test_consulting_rh_is_inconsistent(self):
        row = pd.Series({"departement": "Consulting", "domaine_etude": "Ressources Humaines"})
        assert inconsistency(row) == 1

    # --- Ressources Humaines ---
    def test_rh_rh_is_consistent(self):
        row = pd.Series({"departement": "Ressources Humaines", "domaine_etude": "Ressources Humaines"})
        assert inconsistency(row) == 0

    def test_rh_entrepreneuriat_is_consistent(self):
        row = pd.Series({"departement": "Ressources Humaines", "domaine_etude": "Entrepreunariat"})
        assert inconsistency(row) == 0

    def test_rh_marketing_is_inconsistent(self):
        row = pd.Series({"departement": "Ressources Humaines", "domaine_etude": "Marketing"})
        assert inconsistency(row) == 1

    def test_rh_infra_is_inconsistent(self):
        row = pd.Series({"departement": "Ressources Humaines", "domaine_etude": "Infra & Cloud"})
        assert inconsistency(row) == 1


# ---------------------------------------------------------------------------
# promotion
# Returns 1 (stagnant) only when BOTH values are strictly greater than 4.
# ---------------------------------------------------------------------------

class TestPromotion:
    def test_both_above_4_is_stagnant(self):
        row = pd.Series({"annes_sous_responsable_actuel": 5, "annees_depuis_la_derniere_promotion": 5})
        assert promotion(row) == 1

    def test_large_values_are_stagnant(self):
        row = pd.Series({"annes_sous_responsable_actuel": 10, "annees_depuis_la_derniere_promotion": 10})
        assert promotion(row) == 1

    def test_manager_years_exactly_4_not_stagnant(self):
        row = pd.Series({"annes_sous_responsable_actuel": 4, "annees_depuis_la_derniere_promotion": 5})
        assert promotion(row) == 0

    def test_promotion_years_exactly_4_not_stagnant(self):
        row = pd.Series({"annes_sous_responsable_actuel": 5, "annees_depuis_la_derniere_promotion": 4})
        assert promotion(row) == 0

    def test_both_below_threshold_not_stagnant(self):
        row = pd.Series({"annes_sous_responsable_actuel": 2, "annees_depuis_la_derniere_promotion": 2})
        assert promotion(row) == 0

    def test_only_manager_years_high_not_stagnant(self):
        row = pd.Series({"annes_sous_responsable_actuel": 6, "annees_depuis_la_derniere_promotion": 1})
        assert promotion(row) == 0

    def test_only_promotion_years_high_not_stagnant(self):
        row = pd.Series({"annes_sous_responsable_actuel": 1, "annees_depuis_la_derniere_promotion": 6})
        assert promotion(row) == 0


# ---------------------------------------------------------------------------
# developpement
# Returns 0 for new employees (tenure == 0), 1 when tenure >= 2 with <= 1
# training, 0 otherwise (sufficient training, or tenure == 1 year).
# ---------------------------------------------------------------------------

class TestDeveloppement:
    def test_new_employee_returns_0(self):
        row = pd.Series({"annees_dans_l_entreprise": 0, "nb_formations_suivies": 0})
        assert developpement(row) == 0

    def test_one_year_tenure_returns_0(self):
        # tenure == 1 meets neither condition → 0
        row = pd.Series({"annees_dans_l_entreprise": 1, "nb_formations_suivies": 0})
        assert developpement(row) == 0

    def test_two_years_no_training_is_stagnant(self):
        row = pd.Series({"annees_dans_l_entreprise": 2, "nb_formations_suivies": 0})
        assert developpement(row) == 1

    def test_two_years_one_training_is_stagnant(self):
        row = pd.Series({"annees_dans_l_entreprise": 2, "nb_formations_suivies": 1})
        assert developpement(row) == 1

    def test_two_years_two_trainings_not_stagnant(self):
        row = pd.Series({"annees_dans_l_entreprise": 2, "nb_formations_suivies": 2})
        assert developpement(row) == 0

    def test_long_tenure_no_training_is_stagnant(self):
        row = pd.Series({"annees_dans_l_entreprise": 10, "nb_formations_suivies": 0})
        assert developpement(row) == 1

    def test_long_tenure_sufficient_training_not_stagnant(self):
        row = pd.Series({"annees_dans_l_entreprise": 10, "nb_formations_suivies": 5})
        assert developpement(row) == 0


def test_interpret_shap():
    assert interpret_shap(0, 0.5) == "Primary driver — increases resignation risk"
    assert interpret_shap(0, -0.5) == "Primary driver — decreases resignation risk"
    assert interpret_shap(1, 0.5) == "Strong factor — increases resignation risk"
    assert interpret_shap(1, -0.5) == "Strong factor — decreases resignation risk"
    assert interpret_shap(2, 0.5) == "Moderate factor — increases resignation risk"
    assert interpret_shap(2, -0.5) == "Moderate factor — decreases resignation risk"
    assert interpret_shap(3, 0.5) == "Contributing factor — increases resignation risk"
    assert interpret_shap(3, -0.5) == "Contributing factor — decreases resignation risk"
    assert interpret_shap(4, 0.5) == "Notable factor — increases resignation risk"
    assert interpret_shap(4, -0.5) == "Notable factor — decreases resignation risk"
    