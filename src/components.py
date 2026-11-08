import pandas as pd
import plotly.express as px
import streamlit as st


class UIComponents:

    @staticmethod
    def render_kpis(df: pd.DataFrame) -> None:
        """Affiche la barre des métriques clés (KPIs)."""
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📌 Total CVs", f"{len(df):,}")
        col2.metric("🏷️ Métiers Uniques", df["category"].nunique())
        col3.metric(
            "⚠️ Doublons Exacts", df.duplicated(subset=["resume_text"]).sum()
        )
        col4.metric("📂 Sources Actives", df["source"].nunique())

    @staticmethod
    def render_charts(df: pd.DataFrame) -> None:
        """Affiche les graphiques de répartition."""
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("📊 Répartition par Source")
            fig_pie = px.pie(
                df,
                names="source",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel,
            )
            fig_pie.update_layout(margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig_pie, use_container_width=True)

        with c2:
            st.subheader("💼 Top 15 Métiers")
            top_cats = (
                df["category"]
                .value_counts()
                .head(15)
                .reset_index(name="count")
            )
            top_cats.columns = ["category", "count"]
            fig_bar = px.bar(
                top_cats,
                x="count",
                y="category",
                orientation="h",
                color="count",
                color_continuous_scale="Blues",
            )
            # Ajustements de dimensions et masquage de la barre de couleur inutile
            fig_bar.update_layout(
                height=380,
                yaxis={"categoryorder": "total ascending"},
                showlegend=False,
                margin=dict(t=20, b=20, l=20, r=20),
            )
           

            st.plotly_chart(fig_bar, use_container_width=True)