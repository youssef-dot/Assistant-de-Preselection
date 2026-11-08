import re
import pandas as pd


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