import pytest
import os
import pandas as pd
import yaml

@pytest.fixture
def params():
    with open("configs/params.yaml", "r") as f:
        return yaml.safe_load(f)

def test_data_files_exist(params):
    """Vérifier l'existence des fichiers de données."""
    raw_path = params["data"]["raw_path"]
    assert os.path.exists(raw_path), f"Le fichier {raw_path} n'existe pas."

def test_missing_values_threshold(params):
    """Vérifier que le taux de valeurs manquantes est sous le seuil défini."""
    raw_path = params["data"]["raw_path"]
    if os.path.exists(raw_path):
        df = pd.read_csv(raw_path)
        missing_rate = df.isnull().mean().max()
        threshold = params["quality_checks"]["max_missing_threshold"]
        assert missing_rate <= threshold, f"Taux de missing values ({missing_rate}) > seuil ({threshold})"