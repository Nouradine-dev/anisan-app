
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Application ANISAN", layout="centered")

# Définition des pays et régions
countries_regions = {
    "Niger": ["Agadez", "Diffa", "Dosso", "Maradi", "Niamey", "Tahoua", "Tillabéri", "Zinder"],
    "Burkina Faso": ["Boucle du Mouhoun", "Cascades", "Centre", "Centre-Est", "Centre-Nord", "Centre-Ouest", "Centre-Sud",
                     "Est", "Hauts-Bassins", "Nord", "Plateau-Central", "Sahel", "Sud-Ouest"]
}

# Initialisation session_state
if 'country' not in st.session_state:
    st.session_state.country = "Niger"
if 'region' not in st.session_state:
    st.session_state.region = countries_regions[st.session_state.country][0]

# Sélection du pays
st.session_state.country = st.selectbox("Sélectionnez le pays", list(countries_regions.keys()), index=list(countries_regions.keys()).index(st.session_state.country))

# Sélection de la région en fonction du pays
regions = countries_regions[st.session_state.country]
st.session_state.region = st.selectbox("Sélectionnez la région", regions, index=regions.index(st.session_state.region) if st.session_state.region in regions else 0)

# Fonction de calcul automatique de la phase nutritionnelle
def get_phase_nutritionnelle(poids, taille_cm):
    taille_m = taille_cm / 100
    imc = poids / (taille_m ** 2)
    if imc >= 15:
        return "Phase minimale", "🟢"
    elif 13 <= imc < 15:
        return "MAM", "🟡"
    else:
        return "MAS", "🔴"

st.title("Suivi nutritionnel des enfants")

# Formulaire de saisie
with st.form("form_enfant"):
    nom = st.text_input("Nom de l'enfant")
    age = st.number_input("Âge (en mois)", min_value=0, max_value=59, step=1)
    poids = st.number_input("Poids (en kg)", min_value=0.0, format="%.2f")
    taille = st.number_input("Taille (en cm)", min_value=30.0, format="%.1f")
    pb = st.number_input("Périmètre brachial (en cm)", min_value=5.0, format="%.1f")

    submitted = st.form_submit_button("Enregistrer")

    if submitted:
        phase, couleur = get_phase_nutritionnelle(poids, taille)
        enfant = {
            "Nom": nom,
            "Âge (mois)": age,
            "Poids (kg)": poids,
            "Taille (cm)": taille,
            "PB (cm)": pb,
            "Phase nutritionnelle": phase,
            "Symbole": couleur,
            "Région": st.session_state.region,
            "Pays": st.session_state.country
        }

        # Chargement et mise à jour du fichier
        fichier = "enfants.csv"
        if os.path.exists(fichier):
            df = pd.read_csv(fichier)
            df = pd.concat([df, pd.DataFrame([enfant])], ignore_index=True)
        else:
            df = pd.DataFrame([enfant])

        df.to_csv(fichier, index=False)
        st.success(f"✅ {nom} a été enregistré avec succès ({couleur} {phase})")

        # Alerte en cas de MAS
        if phase == "MAS":
            st.error("🚨 Alerte nutritionnelle : cet enfant présente une malnutrition aiguë sévère (MAS) !")

# Affichage des données enregistrées
if os.path.exists("enfants.csv"):
    st.subheader("Liste des enfants enregistrés")
    df = pd.read_csv("enfants.csv")
    st.dataframe(df)
