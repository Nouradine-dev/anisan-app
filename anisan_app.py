import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="ANISAN - Suivi Nutritionnel", layout="centered")

# Dictionnaire des régions par pays
countries_regions = {
    "Niger": ["Agadez", "Diffa", "Dosso", "Maradi", "Tahoua", "Tillabéri", "Zinder", "Niamey"]
}

# Initialisation des variables de session
if "country" not in st.session_state:
    st.session_state.country = "Niger"

if "region" not in st.session_state:
    st.session_state.region = "Niamey"

# Titre principal
st.title("🧒 Application ANISAN - Suivi Nutritionnel des Enfants")

# Sélection du pays
st.session_state.country = st.selectbox("Sélectionnez le pays", list(countries_regions.keys()))

# Sélection de la région
st.session_state.region = st.selectbox("Sélectionnez la région", countries_regions[st.session_state.country])

# Fonction pour calculer automatiquement la phase nutritionnelle
def get_phase_nutritionnelle(poids, taille_cm):
    taille_m = taille_cm / 100
    imc = poids / (taille_m ** 2)

    if imc >= 15:
        return "Phase minimale", "🟢"
    elif 13 <= imc < 15:
        return "MAM", "🟡"
    else:
        return "MAS", "🔴"

# Formulaire de saisie
st.subheader("➕ Ajouter un nouvel enfant")
with st.form("formulaire_enfant"):
    nom = st.text_input("Nom complet de l’enfant")
    age = st.number_input("Âge (en mois)", min_value=0, max_value=60, step=1)
    poids = st.number_input("Poids (en kg)", min_value=0.0, step=0.1)
    taille = st.number_input("Taille (en cm)", min_value=30.0, step=0.1)
    pb = st.number_input("Périmètre brachial (en cm)", min_value=5.0, step=0.1)

    submit = st.form_submit_button("Enregistrer")

    if submit:
        if not nom or age == 0 or poids == 0 or taille == 0 or pb == 0:
            st.error("🚨 Veuillez remplir tous les champs correctement.")
        else:
            # Calcul automatique de la phase
            phase, symbole = get_phase_nutritionnelle(poids, taille)

            enfant = {
                "Nom": nom,
                "Âge (mois)": age,
                "Poids (kg)": poids,
                "Taille (cm)": taille,
                "Périmètre brachial (cm)": pb,
                "Phase nutritionnelle": phase,
                "Symbole": symbole,
                "Région": st.session_state.region
            }

            if "enfants" not in st.session_state:
                st.session_state.enfants = []

            st.session_state.enfants.append(enfant)
            st.success(f"✅ Enfant enregistré avec succès. Phase : {symbole} {phase}")

            # Alerte nutritionnelle automatique
            if phase == "MAS":
                st.error("🚨 URGENCE : Cas de malnutrition aiguë sévère détecté !")
            elif phase == "MAM":
                st.warning("⚠️ Attention : Cas de malnutrition aiguë modérée.")

# Affichage de la liste des enfants
st.subheader("📋 Liste des enfants enregistrés")

if "enfants" in st.session_state and len(st.session_state.enfants) > 0:
    df = pd.DataFrame(st.session_state.enfants)
    st.dataframe(df)

    # Export CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Télécharger en CSV", data=csv, file_name="enfants_anisan.csv", mime="text/csv")
else:
    st.info("Aucun enfant enregistré pour le moment.")
