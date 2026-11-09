from pathlib import Path
import pandas as pd
import streamlit as st

DATA_PATH = Path("data/dataset_resume_fusionne_final.csv")
FALLBACK_PATH = Path("buckup/dataset_resume_fusionne_final.csv")

class DataLoader:
    @staticmethod
    #@st.cache_data(ttl=600, show_spinner="Chargement du dataset...")
    def load_data() -> pd.DataFrame:
        """Charge le dataset depuis le fichier CSV avec mise en cache."""
        if DATA_PATH.exists():
            return pd.read_csv(DATA_PATH)
        elif FALLBACK_PATH.exists():
            return pd.read_csv(FALLBACK_PATH)
        else:
            raise FileNotFoundError("Aucun fichier source trouvé pour l'ingestion.")

    @staticmethod
    def save_data(df: pd.DataFrame , target_path: Path = DATA_PATH) -> None:
        """Sauvegarde le DataFrame dans le fichier CSV et vide le cache."""
        target_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(target_path, index=False, encoding="utf-8")
        print(f"[DataOps Ingestion] Data sauvegardée avec succès dans : {target_path}")


def run_ingestion():
   
   """Étape d'ingestion pour le pipeline DataOps / DVC."""
    # 1. Verification fi data/ w fil-root
   if DATA_PATH.exists():
        print(f"[Ingestion] Lecture depuis : {DATA_PATH}")
        df = pd.read_csv(DATA_PATH)
   elif FALLBACK_PATH.exists():
        print(f"[Ingestion] Lecture depuis la copie de secours : {FALLBACK_PATH}")
        df = pd.read_csv(FALLBACK_PATH)
   else:
        # Fallback pour le futur API / Scraper
        print("[Ingestion Warning] Aucun fichier source local. Création d'un dataset vide de structure.")
        df = pd.DataFrame(columns=["resume_text", "experience_years", "education_level"])
    
    # 2. Re-création du fichier dans data/ pour valider le stage DVC
   DataLoader.save_data(df, DATA_PATH)

if __name__ == "__main__":
    run_ingestion()