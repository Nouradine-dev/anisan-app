import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
from datetime import date

st.set_page_config(page_title="ANISAN - Suivi Nutritionnel", layout="wide")

st.title("🍼 ANISAN - Suivi Nutritionnel des Enfants au Sahel et en Afrique de l'Ouest")

# --- FONCTIONS UTILES ---

def calc_phase(pb, oedeme):
    """Calcule la phase nutritionnelle et couleur selon PB et œdème"""
    if oedeme == "Oui" or pb < 11.5:
        return "MAS (Aiguë sévère)", "🔴🔴"
    elif 11.5 <= pb < 12.5:
        return "MAM (Aiguë modérée)", "🟠"
    elif 12.5 <= pb < 12.9:
        return "Stress nutritionnel", "🟡"
    else:
        return "Phase minimale", "🟢"

def analyse_alertes(enfants):
    """Analyse les enfants enregistrés et génère des alertes par région"""
    alertes = []
    if not enfants:
        return alertes

    df = pd.DataFrame(enfants)
    regions = df["Région"].unique()
    for region in regions:
        df_region = df[df["Région"] == region]
        total = len(df_region)
        mas_count = df_region["Phase nutritionnelle"].str.contains("MAS").sum()
        mas_pct = (mas_count / total) * 100

        # Seuil d'alerte : MAS > 5%
        if mas_pct > 5:
            alertes.append(f"⚠️ Alerte nutritionnelle : {mas_pct:.1f}% MAS à {region} ! Intervention urgente requise.")
    return alertes

# --- INITIALISATION DES ENFANTS ---

if "enfants" not in st.session_state:
    st.session_state["enfants"] = []

# --- AFFICHAGE DES ALERTES ---

alertes = analyse_alertes(st.session_state["enfants"])
if alertes:
    for alerte in alertes:
        st.error(alerte)
else:
    st.success("✅ Pas d’alerte nutritionnelle majeure détectée.")

# --- FORMULAIRE D’ENREGISTREMENT ---

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
    phase, couleur = calc_phase(pb, oedeme)
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
    st.experimental_rerun()  # Recharger pour mise à jour alertes et tableau

# --- ANALYSE ET VISUALISATION ---

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

# --- EXPORT CSV ---

st.markdown("## 📥 Exporter les données")
if st.session_state["enfants"]:
    df = pd.DataFrame(st.session_state["enfants"])
    csv = df.to_csv(index=False, sep=';').encode("utf-8")  # Séparateur ';' pour Excel francophone
    st.download_button("📄 Télécharger CSV (Excel compatible)", csv, "enfants_anisan.csv", mime="text/csv")
