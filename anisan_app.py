import streamlit as st
import streamlit as st
import streamlit as st

# Dictionnaire des pays et régions
countries_regions = {
    "Niger": [
        "Agadez", "Diffa", "Dosso", "Maradi", "Niamey",
        "Tahoua", "Tillabéri", "Zinder"
    ],
    "Sénégal": [
        "Dakar", "Diourbel", "Fatick", "Kaffrine", "Kaolack", "Kédougou",
        "Kolda", "Louga", "Matam", "Saint-Louis", "Sédhiou",
        "Tambacounda", "Thiès", "Ziguinchor"
    ]
}

# Fonction déclenchée quand le pays change
def on_country_change():
    st.session_state.region = countries_regions[st.session_state.country][0]

# Initialisation
if "country" not in st.session_state:
    st.session_state.country = "Niger"
if "region" not in st.session_state:
    st.session_state.region = countries_regions[st.session_state.country][0]

# Choix du pays
st.selectbox(
    "Sélectionnez le pays",
    list(countries_regions.keys()),
    key="country",
    on_change=on_country_change
)

# Choix de la région en fonction du pays sélectionné
st.selectbox(
    "Sélectionnez la région",
    countries_regions[st.session_state.country],
    key="region"
)

# Dictionnaire des pays et régions
countries_regions = {
    "Niger": ["Agadez", "Diffa", "Dosso", "Maradi", "Niamey",
              "Tahoua", "Tillabéri", "Zinder"],
    "Sénégal": ["Dakar", "Diourbel", "Fatick", "Kaffrine", "Kaolack", "Kédougou",
                "Kolda", "Louga", "Matam", "Saint‑Louis", "Sédhiou",
                "Tambacounda", "Thiès", "Ziguinchor"]
}

# Initialisation session state
if 'country' not in st.session_state:
    st.session_state.country = 'Niger'
if 'region' not in st.session_state:
    st.session_state.region = countries_regions[st.session_state.country][0]

def on_country_change():
    # Met à jour la région dès que le pays change
    st.session_state.region = countries_regions[st.session_state.country][0]

# Sélecteur de pays
st.selectbox(
    "Sélectionnez le pays",
    options=list(countries_regions.keys()),
    key='country',
    on_change=on_country_change
)

# Sélecteur de région dynamique
st.selectbox(
    "Sélectionnez la région",
    options=countries_regions[st.session_state.country],
    key='region'
)

# Dictionnaire des pays avec leurs régions
countries_regions = {
    "Niger": [
        "Agadez", "Diffa", "Dosso", "Maradi", "Niamey",
        "Tahoua", "Tillabéri", "Zinder"
    ],
    "Sénégal": [
        "Dakar", "Diourbel", "Fatick", "Kaffrine", "Kaolack", "Kédougou",
        "Kolda", "Louga", "Matam", "Saint-Louis", "Sédhiou",
        "Tambacounda", "Thiès", "Ziguinchor"
    ]
}

# Sélection du pays
# Sélection de la région en fonction du pays
st.session_state.region = st.selectbox("Sélectionnez la région", countries_regions[st.session_state.country])

import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
from datetime import date

st.set_page_config(page_title="ANISAN - Suivi Nutritionnel", layout="wide")

st.title("🍼 ANISAN - Suivi Nutritionnel des Enfants au Sahel et en Afrique de l'Ouest")

# Initialisation
if "enfants" not in st.session_state:
    st.session_state["enfants"] = []

regions = ["Ziguinchor", "Dakar", "Thiès", "Kolda", "Saint-Louis", "Tambacounda", "Matam", "Kaolack"]

st.markdown("## ➕ Ajouter un nouvel enfant")

with st.form("formulaire_enfant"):
    col1, col2 = st.columns(2)
    with col1:
        nom = st.text_input("Nom de l’enfant")
        sexe = st.selectbox("Sexe", ["M", "F"])
        age = st.number_input("Âge (en mois)", min_value=0, max_value=120, step=1)
        region = st.selectbox("Région", regions)
    with col2:
        poids = st.number_input("Poids (kg)", min_value=0.0, step=0.1)
        taille = st.number_input("Taille (cm)", min_value=0.0, step=0.1)
        pb = st.number_input("Périmètre brachial (cm)", min_value=0.0, step=0.1)
        oedeme = st.radio("Œdème nutritionnel ?", ["Non", "Oui"])
        date_mesure = st.date_input("Date de la mesure", value=date.today())

    submitted = st.form_submit_button("📨 Enregistrer")

if submitted:
    if oedeme == "Oui" or pb < 11.5:
        phase = "MAS (Aiguë sévère)"
        couleur = "🔴🔴"
    elif 11.5 <= pb < 12.5:
        phase = "MAM (Aiguë modérée)"
        couleur = "🟠"
    elif 12.5 <= pb < 12.9:
        phase = "Stress nutritionnel"
        couleur = "🟡"
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
        "Région": region,
        "Date de mesure": date_mesure.strftime("%d/%m/%Y"),
        "Phase nutritionnelle": f"{couleur} {phase}"
    }
    st.session_state["enfants"].append(enfant)
    st.success("✅ Données enregistrées avec succès !")

# Analyse et visualisation
st.markdown("## 📊 Statistiques Nutritionnelles")

if st.session_state["enfants"]:
    df = pd.DataFrame(st.session_state["enfants"])
    total = len(df)
    mam = df["Phase nutritionnelle"].str.contains("MAM").sum()
    mas = df["Phase nutritionnelle"].str.contains("MAS").sum()
    pb_moy = df["PB (cm)"].mean()
    poids_moy = df["Poids (kg)"].mean()
    taille_moy = df["Taille (cm)"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("👶 Total enfants", total)
    col2.metric("🟠 % MAM", f"{(mam/total)*100:.1f}%")
    col3.metric("🔴 % MAS", f"{(mas/total)*100:.1f}%")

    col4, col5, col6 = st.columns(3)
    col4.metric("📏 PB moyen", f"{pb_moy:.1f} cm")
    col5.metric("⚖️ Poids moyen", f"{poids_moy:.1f} kg")
    col6.metric("📐 Taille moyenne", f"{taille_moy:.1f} cm")

    st.markdown("## 🗺️ Répartition géographique")
    region_counts = df["Région"].value_counts().reset_index()
    region_counts.columns = ["Région", "Nombre"]
    m = folium.Map(location=[14.5, -14.5], zoom_start=6)
    coords = {
        "Ziguinchor": [12.5, -16.3],
        "Dakar": [14.7, -17.5],
        "Thiès": [14.8, -16.9],
        "Kolda": [12.9, -14.9],
        "Saint-Louis": [16.0, -16.5],
        "Tambacounda": [13.8, -13.7],
        "Matam": [15.3, -13.3],
        "Kaolack": [14.2, -16.1]
    }
    for _, row in region_counts.iterrows():
        nom = row["Région"]
        n = row["Nombre"]
        if nom in coords:
            folium.CircleMarker(
                location=coords[nom],
                radius=10,
                popup=f"{nom} : {n} cas",
                color="blue",
                fill=True,
                fill_color="blue"
            ).add_to(m)
    st_folium(m, width=700, height=400)

    st.markdown("## 🧾 Tableau des enfants")
    for i, enfant in enumerate(st.session_state["enfants"]):
        st.write(f"**{i+1}.** {enfant['Nom']} ({enfant['Phase nutritionnelle']}) – {enfant['Région']}")
        if st.button(f"🗑️ Supprimer {enfant['Nom']}", key=f"delete_{i}"):
            st.session_state["enfants"].pop(i)
            st.experimental_rerun()

else:
    st.info("Aucun enfant enregistré pour l’instant.")

st.markdown("## 📥 Exporter les données")
if st.session_state["enfants"]:
    df = pd.DataFrame(st.session_state["enfants"])
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📄 Télécharger CSV", csv, "enfants_anisan.csv", mime="text/csv")
