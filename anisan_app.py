import streamlit as st
import pandas as pd
from datetime import date
import pydeck as pdk

# Configuration
st.set_page_config(page_title="ANISAN", layout="centered")

st.title("🍼 Application ANISAN - Suivi Nutritionnel des Enfants")

# Données des régions avec coordonnées géographiques
regions_coords = {
    "Niger": {
        "Agadez": (16.9666, 7.9911),
        "Dosso": (13.05, 3.2),
        "Maradi": (13.5, 7.1),
        "Niamey": (13.5, 2.1),
        "Tahoua": (14.9, 5.3),
        "Tillabéri": (14.2, 1.45),
        "Zinder": (13.8, 8.99)
    },
    "Burkina Faso": {
        "Centre": (12.3714, -1.5197),
        "Hauts-Bassins": (11.1, -4.3),
        "Est": (12.5, 0.4)
    },
    "Sénégal": {
        "Dakar": (14.6928, -17.4467),
        "Thiès": (14.7833, -16.9333),
        "Saint-Louis": (16.0179, -16.4896)
    },
    "Bénin": {
        "Alibori": (11.5, 3.5),
        "Borgou": (9.3, 2.6),
        "Collines": (8.6, 2.3),
        "Ouémé": (6.5, 2.6)
    }
}

# Initialisation de la session
if "enfants" not in st.session_state:
    st.session_state.enfants = []

# 📋 Formulaire
st.header("➕ Ajouter un enfant")
with st.form("ajout_enfant"):
    pays = st.selectbox("Pays", list(regions_coords.keys()))
    region = st.selectbox("Région", list(regions_coords[pays].keys()))
    nom = st.text_input("Nom de l’enfant")
    sexe = st.radio("Sexe", ["M", "F"], horizontal=True)
    age = st.number_input("Âge (en mois)", min_value=0, max_value=60)
    poids = st.number_input("Poids (kg)", min_value=0.0, step=0.1)
    taille = st.number_input("Taille (cm)", min_value=0.0, step=0.1)
    pb = st.number_input("Périmètre brachial (cm)", min_value=0.0, step=0.1)
    oedeme = st.radio("Œdème ?", ["Non", "Oui"], horizontal=True)
    date_mesure = st.date_input("Date de mesure", value=date.today())

    valider = st.form_submit_button("📨 Enregistrer")

# 🔎 Analyse nutritionnelle
def evaluer_statut(pb, oedeme):
    if oedeme == "Oui" or pb < 11.5:
        return "🔴 MAS (Malnutrition aiguë sévère)", "Fournir une alimentation thérapeutique d’urgence. Référer à un centre de santé immédiatement."
    elif pb < 12.5:
        return "🟠 MAM (Malnutrition aiguë modérée)", "Apporter un complément nutritionnel spécifique et surveiller l’état de santé."
    elif pb < 13.0:
        return "🟡 Stress nutritionnel", "Renforcer l’alimentation. Suivi mensuel recommandé."
    else:
        return "🟢 Bonne situation nutritionnelle", "Continuer une alimentation équilibrée. Contrôle régulier mensuel."

# ✅ Enregistrement
if valider:
    statut, conseil = evaluer_statut(pb, oedeme)
    lat, lon = regions_coords[pays][region]
    
    enfant = {
        "Nom": nom,
        "Sexe": sexe,
        "Âge (mois)": age,
        "Poids (kg)": poids,
        "Taille (cm)": taille,
        "PB (cm)": pb,
        "Œdème": oedeme,
        "Pays": pays,
        "Région": region,
        "Date": date_mesure.strftime("%d/%m/%Y"),
        "Statut": statut,
        "Conseil": conseil,
        "latitude": lat,
        "longitude": lon
    }

    st.session_state.enfants.append(enfant)
    st.success("✅ Données enregistrées avec succès !")

# 📊 Tableau
if st.session_state.enfants:
    df = pd.DataFrame(st.session_state.enfants)
    
    st.markdown("### 🗂️ Tableau de Suivi")
    st.dataframe(df.drop(columns=["latitude", "longitude"]), use_container_width=True)

    # 📥 Export CSV
    st.markdown("### 📥 Export des données")
    st.download_button(
        label="📄 Télécharger les données (CSV)",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name="anisan_data.csv",
        mime="text/csv"
    )

    # 📌 Conseils
    st.markdown("### 📌 Conseils nutritionnels")
    for e in st.session_state.enfants:
        st.markdown(f"**{e['Nom']} ({e['Statut']})** : ✅ {e['Conseil']}")

    # 🗺️ Carte de localisation
    st.markdown("### 🗺️ Carte de localisation des enfants")
    geo_df = df.rename(columns={"latitude": "lat", "longitude": "lon"})
    st.map(geo_df[['lat', 'lon']])
else:
    st.info("📋 Enregistrez des enfants pour visualiser les tableaux et cartes.")
