import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="ANISAN - Application Nutritionnelle", layout="centered")

st.title("🍼 Application ANISAN - Suivi Nutritionnel des Enfants")

# Initialisation
if "enfants" not in st.session_state:
    st.session_state["enfants"] = []

# Formulaire
st.markdown("### ➕ Ajouter un nouvel enfant")
with st.form("formulaire_enfant"):
    nom = st.text_input("Nom de l’enfant")
    sexe = st.selectbox("Sexe", ["M", "F"])
    age = st.number_input("Âge (en mois)", min_value=0, max_value=120, step=1)
    poids = st.number_input("Poids (kg)", min_value=0.0, step=0.1)
    taille = st.number_input("Taille (cm)", min_value=0.0, step=0.1)
    pb = st.number_input("Périmètre brachial (cm)", min_value=0.0, step=0.1)
    oedeme = st.radio("Œdème nutritionnel ?", ["Non", "Oui"])
    date_mesure = st.date_input("Date de la mesure", value=date.today())
    submitted = st.form_submit_button("📨 Enregistrer")

if submitted:
    if oedeme == "Oui" or pb <= 11.0:
        phase = "Famine nutritionnelle"
        couleur = "🔴"
    elif pb <= 11.5:
        phase = "Urgence nutritionnelle"
        couleur = "🟥"
    elif pb <= 12.5:
        phase = "Crise nutritionnelle (MAM)"
        couleur = "🟧"
    elif pb <= 12.9:
        phase = "Stress nutritionnel"
        couleur = "🟨"
    else:
        phase = "Phase minimale"
        couleur = "🟢"

    enfant = {
        "Nom": nom,
        "Sexe": sexe,
        "Âge (mois)": age,
        "Poids (kg)": poids,
        "Taille (cm)": taille,
        "PB (cm)": pb,
        "Œdème": oedeme,
        "Date de mesure": date_mesure.strftime("%d/%m/%Y"),
        "Statut nutritionnel": f"{couleur} {phase}"
    }
    st.session_state["enfants"].append(enfant)
    st.success("✅ Données enregistrées avec succès !")

# Tableau
st.markdown("### 📊 Tableau des enfants enregistrés")
if st.session_state["enfants"]:
    df = pd.DataFrame(st.session_state["enfants"])
    st.dataframe(df, use_container_width=True)

    # Export
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📄 Télécharger les données (CSV)", data=csv, file_name="donnees_anisan.csv", mime="text/csv")

    excel_path = "donnees_anisan.xlsx"
    df.to_excel(excel_path, index=False)
    with open(excel_path, "rb") as f:
        st.download_button("📊 Télécharger les données (Excel)", data=f, file_name="donnees_anisan.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
else:
    st.info("Aucune donnée enregistrée pour le moment.")

# Graphiques
st.markdown("## 📈 Visualisation des données nutritionnelles")
if st.session_state["enfants"]:
    df = pd.DataFrame(st.session_state["enfants"])
    df["Phase simplifiée"] = df["Statut nutritionnel"].str.extract(r"[🔴🟥🟧🟨🟢] (.*)")

    st.markdown("### 📌 Nombre d’enfants par phase nutritionnelle")
    phase_count = df["Phase simplifiée"].value_counts().sort_index()
    st.bar_chart(phase_count)

    st.markdown("### 👦👧 Répartition par sexe")
    sexe_count = df["Sexe"].value_counts()
    st.bar_chart(sexe_count)

    st.markdown("### ⏳ Répartition par tranche d’âge (mois)")
    bins = [0, 5, 11, 23, 59, 120]
    labels = ["0–5", "6–11", "12–23", "24–59", "60+"]
    df["Tranche d’âge"] = pd.cut(df["Âge (mois)"], bins=bins, labels=labels, include_lowest=True)
    age_group_count = df["Tranche d’âge"].value_counts().sort_index()
    st.bar_chart(age_group_count)
else:
    st.info("➡️ Enregistrez des enfants pour visualiser les graphiques.")
