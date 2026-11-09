from pathlib import Path
import re
import pandas as pd
import numpy as np
import yaml


class DataProcessor:

    @staticmethod
    def get_duplicates(
        df: pd.DataFrame, subset_col: str = "resume_text"
    ) -> pd.DataFrame:
        """Retourne toutes les lignes identifiées comme doublons exacts."""
        return df[df.duplicated(subset=[subset_col], keep=False)].sort_values(
            by=subset_col
        )

    #nahiha
    @staticmethod
    def anonymize_text(text: str) -> str:
        """Masque les données personnelles sensibles (PII)."""
        if not isinstance(text, str):
            return ""

        # Masquage Email, Téléphone, SSN
        text = re.sub(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "[EMAIL_MASKED]",
            text,
        )
        text = re.sub(
            r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
            "[PHONE_MASKED]",
            text,
        )
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[SSN_MASKED]", text)

        # Nettoyage bruit OCR fréquent
        text = re.sub(r"Clairenes", "lines", text)
        text = re.sub(r"guideClairenes", "guidelines", text)
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def add_new_resume(
        df: pd.DataFrame, text: str, category: str, source: str
    ) -> pd.DataFrame:
        """Ajoute un nouveau CV validé au DataFrame."""
        new_entry = pd.DataFrame(
            [
                {
                    "resume_text": text.strip(),
                    "category": category.upper().strip(),
                    "source": source,
                }
            ]
        )
        return pd.concat([df, new_entry], ignore_index=True)

def load_params():
    """Charge la configuration depuis configs/params.yaml."""
    with open("configs/params.yaml", "r") as f:
        return yaml.safe_load(f)

def run_preprocessing():
    """Exécution du pipeline de prétraitement pour DVC."""
    params = load_params()
    raw_path = Path(params["data"]["raw_path"])
    processed_dir = Path(params["data"]["processed_dir"])

    # Création automatique du dossier data/processed/
    processed_dir.mkdir(parents=True, exist_ok=True)

    if not raw_path.exists():
        raise FileNotFoundError(f"Le fichier raw est introuvable : {raw_path}")

    print(f"[Preprocessing] Lecture des données brutes depuis : {raw_path}")
    df = pd.read_csv(raw_path)

    # Nettoyage et anonymisation si la colonne resume_text existe
    if "resume_text" in df.columns:
        df["resume_text"] = df["resume_text"].apply(DataProcessor.anonymize_text)

    # Suppression des doublons exacts
    df = df.drop_duplicates()

    # Split train / test avec Pure Pandas / Numpy (Pour éviter le blocage DLL de sklearn)
    test_size = params["data"].get("test_size", 0.2)
    random_state = params["base"].get("random_state", 42)

    np.random.seed(random_state)
    shuffled_indices = np.random.permutation(len(df))
    test_set_size = int(len(df) * test_size)

    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]

    train_df = df.iloc[train_indices]
    test_df = df.iloc[test_indices]

    """# Split train / test
    test_size = params["data"].get("test_size", 0.2)
    random_state = params["base"].get("random_state", 42)

    train_df, test_df = train_test_split(
        df, test_size=test_size, random_state=random_state
    )
"""
    # Sauvegarde des fichiers prétraités
    train_path = Path(params["data"]["train_path"])
    test_path = Path(params["data"]["test_path"])

    train_df.to_csv(train_path, index=False, encoding="utf-8")
    test_df.to_csv(test_path, index=False, encoding="utf-8")

    print(f"[Preprocessing] Dataset Train sauvegardé dans : {train_path}")
    print(f"[Preprocessing] Dataset Test sauvegardé dans : {test_path}")


if __name__ == "__main__":
    run_preprocessing()