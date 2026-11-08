from pathlib import Path
import pandas as pd
import streamlit as st

DATA_PATH = Path("data/dataset_resume_fusionne_final.csv")

class DataLoader:
    @staticmethod
    @st.cache_data(ttl=600, show_spinner="Chargement du dataset...")
    def load_data() -> pd.DataFrame:
        """Charge le dataset depuis le fichier CSV avec mise en cache."""
        if not DATA_PATH.exists():
            # Fallback si le fichier est à la racine
            fallback_path = Path("dataset_resume_fusionne_final.csv")
            if fallback_path.exists():
                return pd.read_csv(fallback_path)
            else:
                raise FileNotFoundError(f"Le fichier {DATA_PATH} n'existe pas.")
        return pd.read_csv(DATA_PATH)

    @staticmethod
    def save_data(df: pd.DataFrame) -> None:
        """Sauvegarde le DataFrame dans le fichier CSV et vide le cache."""
        target_path = (
            DATA_PATH
            if DATA_PATH.parent.exists()
            else Path("dataset_resume_fusionne_final_2.csv")
        )

        df.to_csv(target_path, index=False, encoding="utf-8")
        st.cache_data.clear()