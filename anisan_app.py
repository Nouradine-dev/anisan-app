import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="ANISAN - Application Nutritionnelle", layout="centered")

st.title("🍼 Application ANISAN - Suivi Nutritionnel des Enfants")

st.markdown("Remplissez le formulaire pour chaque enfant évalué.")

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
    phase = ""
    couleur = ""

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

    st.success("✅ Données enregistrées avec succès !")
    st.markdown(f"**Statut nutritionnel : {couleur} {phase}**")
