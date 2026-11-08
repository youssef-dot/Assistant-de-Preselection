import pandas as pd
import streamlit as st
from src.components import UIComponents
from src.data_loader import DataLoader
from src.data_processor import DataProcessor

# Configuration de la page
st.set_page_config(
    page_title="DataOps Resume Analytics Engine", page_icon="⚡", layout="wide"
)


def main():
    st.title("⚡ DataOps Pipeline — Resume Dataset Control Center")

    # 1. Chargement des données via DataLoader
    try:
        df = DataLoader.load_data()
    except Exception as e:
        st.error(f"Erreur critique lors du chargement des données : {e}")
        st.stop()

    # 2. Barre latérale de filtrage (Sidebar)
    st.sidebar.header("🎛️ Filtres Globaux")
    selected_sources = st.sidebar.multiselect(
        "Sources de données",
        options=df["source"].unique(),
        default=df["source"].unique(),
    )
    selected_categories = st.sidebar.multiselect(
        "Catégories de métiers",
        options=df["category"].unique(),
        default=df["category"].unique(),
    )

    # Filtrage dynamique
    filtered_df = df[
        (df["source"].isin(selected_sources))
        & (df["category"].isin(selected_categories))
    ]

    # 3. Métriques clés
    UIComponents.render_kpis(filtered_df)
    st.divider()

    # 4. Onglets de contrôle (Tabs)
    tab_analytics, tab_duplicates, tab_ingest, tab_raw = st.tabs(
        [
            "📊 Analytics & Distribution",
            "⚠️ Control Panel Doublons",
            "➕ Ingestion Nouveau CV",
            "📋 Data Explorer",
        ]
    )

    with tab_analytics:
        UIComponents.render_charts(filtered_df)

    with tab_duplicates:
        st.subheader("🔍 Inspection des Doublons Exacts")
        dups = DataProcessor.get_duplicates(filtered_df)
        if not dups.empty:
            st.warning(f"Attention : {len(dups)} enregistrements en doublon identifiés.")
            st.dataframe(
                dups[["source", "category", "resume_text"]],
                use_container_width=True,
                height=300,
            )
        else:
            st.success("Aucun doublon trouvé dans le sous-ensemble filtré.")

    with tab_ingest:
        st.subheader("📥 Ingestion Manuelle de Données")
        with st.form("ingest_form", clear_on_submit=True):
            col_cat, col_src = st.columns(2)
            with col_cat:
                cat_input = st.text_input("Catégorie Métier (ex: DATA-ENGINEER)")
            with col_src:
                src_input = st.selectbox(
                    "Source d'origine",
                    options=["MANUAL_INGESTION", "PARTNER_API", "OCR_BATCH"],
                )

            txt_input = st.text_area("Contenu textuel du CV", height=200)
            submitted = st.form_submit_button("Ingérer & Sauvegarder")

            if submitted:
                if txt_input.strip() and cat_input.strip():
                    # Appliquer l'anonymisation PII avant sauvegarde
                    clean_txt = DataProcessor.anonymize_text(txt_input)
                    updated_df = DataProcessor.add_new_resume(
                        df, clean_txt, cat_input, src_input
                    )
                    DataLoader.save_data(updated_df)
                    st.success("Nouveau CV intégré et sauvegardé dans le dataset !")
                    st.rerun()
                else:
                    st.error("Tous les champs requis doivent être remplis.")

    with tab_raw:
        st.subheader("📋 Dataset Brut Filtré")
        st.dataframe(filtered_df, use_container_width=True)


if __name__ == "__main__":
    main()