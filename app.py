import streamlit as st
import pandas as pd
import json
import os
import joblib
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="ANISAN", layout="centered")

# ---------- FONCTIONS ----------
def charger_coords():
    with open("pays_regions_coords.json", "r", encoding="utf-8") as f:
        return json.load(f)

def charger_donnees():
    if os.path.exists("enfants.json"):
        with open("enfants.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def enregistrer_donnees(data):
    with open("enfants.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def entrainer_modele():
    X = [[24, 12.5, 8.2, 80], [36, 11.2, 7.5, 75], [18, 13.0, 8.5, 82], [30, 10.5, 7.2, 70]]
    y = ["Normal", "MAS", "Normal", "MAM"]
    model = RandomForestClassifier()
    model.fit(X, y)
    joblib.dump(model, "model.pkl")

def charger_modele():
    if not os.path.exists("model.pkl"):
        entrainer_modele()
    return joblib.load("model.pkl")

def faire_prediction(age, pb_cm, poids, taille):
    model = charger_modele()
    prediction = model.predict([[age, pb_cm, poids, taille]])[0]
    proba = model.predict_proba([[age, pb_cm, poids, taille]])[0]
    return prediction, proba

def donner_recommandations(prediction):
    if prediction == "MAS":
        return "⚠️ L'enfant est en malnutrition aiguë sévère. Référez immédiatement au centre de santé pour prise en charge thérapeutique."
    elif prediction == "MAM":
        return "⚠️ L'enfant est en malnutrition aiguë modérée. Fournir des suppléments nutritionnels et un suivi rapproché."
    else:
        return "✅ L'état nutritionnel est normal. Poursuivre l’alimentation équilibrée et les consultations régulières."

# ---------- INTERFACE UTILISATEUR ----------
st.title("🧒🏽 ANISAN - Suivi Nutritionnel de l’Enfant")

data_geo = charger_coords()
donnees = charger_donnees()

pays = st.selectbox("🌍 Sélectionner un pays", list(data_geo.keys()))
regions = [r["region"] for r in data_geo[pays]]
region = st.selectbox("📍 Sélectionner une région", regions)
coords = next((r for r in data_geo[pays] if r["region"] == region), None)

nom = st.text_input("Nom de l'enfant")
age = st.number_input("Âge (mois)", min_value=0, max_value=60, step=1)
pb = st.number_input("Périmètre brachial (mm)", min_value=50.0, max_value=200.0, step=1.0)
poids = st.number_input("Poids (kg)", min_value=2.0, max_value=30.0, step=0.1)
taille = st.number_input("Taille (cm)", min_value=30.0, max_value=120.0, step=0.1)

if st.button("📥 Enregistrer et Analyser"):
    pb_cm = pb / 10  # conversion mm → cm
    pred, proba = faire_prediction(age, pb_cm, poids, taille)
    reco = donner_recommandations(pred)

    enfant = {
        "nom": nom,
        "age": age,
        "pb": pb,  # stocké en mm
        "poids": poids,
        "taille": taille,
        "pays": pays,
        "region": region,
        "latitude": coords["latitude"],
        "longitude": coords["longitude"],
        "prediction": pred,
        "recommandation": reco,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    donnees.append(enfant)
    enregistrer_donnees(donnees)

    st.success(f"✅ Données enregistrées pour {nom}")
    st.info(f"**Évaluation IA :** {pred}")
    st.write(f"**Recommandation :** {reco}")

    st.map(pd.DataFrame([{
        "lat": coords["latitude"],
        "lon": coords["longitude"]
    }], columns=["lat", "lon"]))

# ---------- TABLEAU DES DONNÉES ----------
st.subheader("📊 Enregistrements existants")

if donnees:
    df = pd.DataFrame(donnees)
    st.dataframe(df[["nom", "age", "pb", "poids", "taille", "pays", "region", "prediction", "date"]])

    st.subheader("🗑️ Supprimer un enregistrement")
    noms = [e["nom"] for e in donnees]
    choix_nom = st.selectbox("Choisir un enfant à supprimer", noms)
    if st.button("Supprimer"):
        donnees = [e for e in donnees if e["nom"] != choix_nom]
        enregistrer_donnees(donnees)
        st.success(f"Enregistrement pour {choix_nom} supprimé.")
else:
    st.info("Aucun enregistrement disponible pour le moment.")
