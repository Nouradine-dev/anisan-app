
import streamlit as st
import pandas as pd
from datetime import date
import pydeck as pdk

st.set_page_config(page_title="ANISAN - Application Nutritionnelle", layout="centered")
st.title("🍼 ANISAN - Suivi Nutritionnel des Enfants en Afrique de l’Ouest")

# Données des pays et régions (extrait simplifié)
regions_par_pays = {
    "Bénin": ["Alibori", "Atacora", "Atlantique", "Borgou", "Collines", "Donga", "Kouffo", "Littoral", "Mono", "Ouémé", "Plateau", "Zou"],
    "Niger": ["Agadez", "Diffa", "Dosso", "Maradi", "Niamey", "Tahoua", "Tillabéry", "Zinder"],
    "Burkina Faso": ["Boucle du Mouhoun", "Cascades", "Centre", "Centre-Est", "Centre-Nord", "Centre-Ouest", "Centre-Sud", "Est", "Hauts-Bassins", "Nord", "Plateau-Central", "Sahel", "Sud-Ouest"],
    "Sénégal": ["Dakar", "Diourbel", "Fatick", "Kaffrine", "Kaolack", "Kédougou", "Kolda", "Louga", "Matam", "Saint-Louis", "Sédhiou", "Tambacounda", "Thiès", "Ziguinchor"]
    # Tu peux ajouter les autres pays ici
}

# Initialiser l'état
if "enfants" not in st.session_state:
    st.session_state["enfants"] = []

# Formulaire
st.markdown("### ➕ Ajouter un nouvel enfant")
with st.form("formulaire_enfant"):
    pays = st.selectbox("Pays", list(regions_par_pays.keys()))
    region = st.selectbox("Région", regions_par_pays[pays])
    nom = st.text_input("Nom de l’enfant")
    sexe = st.selectbox("Sexe", ["M", "F"])
    age = st.number_input("Âge (en mois)", min_value=0, max_value=120, step=1)
    poids = st.number_input("Poids (kg)", min_value=0.0, step=0.1)
    taille = st.number_input("Taille (cm)", min_value=0.0, step=0.1)
    pb = st.number_input("Périmètre brachial (cm)", min_value=0.0, step=0.1)
    oedeme = st.radio("Œdème nutritionnel ?", ["Non", "Oui"])
    lat = st.number_input("Latitude (ex: 13.5)")
    lon = st.number_input("Longitude (ex: 2.1)")
    date_mesure = st.date_input("Date de la mesure", value=date.today())

    submitted = st.form_submit_button("📨 Enregistrer")

# Traitement
if submitted:
    phase = ""
    couleur = ""
    recommandation = ""

    if oedeme == "Oui" or pb <= 11.0:
        phase = "Famine nutritionnelle"
        couleur = "🔴"
        recommandation = "⚠️ Consultation urgente et prise en charge immédiate."
    elif pb <= 11.5:
        phase = "Urgence nutritionnelle (MAS)"
        couleur = "🟥"
        recommandation = "⚠️ Surveillance médicale urgente et supplémentation thérapeutique."
    elif pb <= 12.5:
        phase = "Crise nutritionnelle (MAM)"
        couleur = "🟧"
        recommandation = "🟠 Apport alimentaire enrichi + suivi hebdomadaire."
    elif pb <= 12.9:
        phase = "Stress nutritionnel"
        couleur = "🟨"
        recommandation = "🟡 Renforcer la diversité alimentaire à domicile."
    else:
        phase = "Phase minimale (normale)"
        couleur = "🟢"
        recommandation = "🟢 Surveillance mensuelle et maintien des bonnes pratiques."

    enfant = {
        "Pays": pays,
        "Région": region,
        "Nom": nom,
        "Sexe": sexe,
        "Âge (mois)": age,
        "Poids (kg)": poids,
        "Taille (cm)": taille,
        "PB (cm)": pb,
        "Œdème": oedeme,
        "Latitude": lat,
        "Longitude": lon,
        "Date de mesure": date_mesure.strftime("%d/%m/%Y"),
        "Phase nutritionnelle": f"{couleur} {phase}",
        "Recommandation": recommandation
    }

    st.session_state["enfants"].append(enfant)
    st.success("✅ Données enregistrées avec succès !")

# Affichage du tableau
if st.session_state["enfants"]:
    df = pd.DataFrame(st.session_state["enfants"])
    st.markdown("### 📋 Données enregistrées")
    st.dataframe(df, use_container_width=True)

    st.markdown("### 📌 Recommandations nutritionnelles")
    for enfant in st.session_state["enfants"]:
        st.write(f"👶 {enfant['Nom']} ({enfant['Région']}, {enfant['Pays']}) : {enfant['Recommandation']}")

    st.markdown("### 🗺️ Carte des localisations")
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=12.5,
            longitude=-1.5,
            zoom=4,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=df,
                get_position='[Longitude, Latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius=20000,
            ),
        ],
    ))

else:
    st.info("Aucune donnée enregistrée pour l’instant.")
