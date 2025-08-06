import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="ANISAN - Suivi Nutritionnel", layout="centered")
st.title("🍼 ANISAN - Suivi Nutritionnel des Enfants")

if "enfants" not in st.session_state:
    st.session_state["enfants"] = []

regions_par_pays = {
    "Bénin": ["Alibori", "Atacora", "Atlantique", "Borgou", "Collines", "Donga", "Kouffo", "Littoral", "Mono", "Ouémé", "Plateau", "Zou"],
    "Burkina Faso": ["Boucle du Mouhoun", "Cascades", "Centre", "Centre-Est", "Centre-Nord", "Centre-Ouest", "Centre-Sud", "Est", "Hauts-Bassins", "Nord", "Plateau-Central", "Sahel", "Sud-Ouest"],
    "Sénégal": ["Dakar", "Diourbel", "Fatick", "Kaffrine", "Kaolack", "Kédougou", "Kolda", "Louga", "Matam", "Saint-Louis", "Sédhiou", "Tambacounda", "Thiès", "Ziguinchor"],
    "Niger": ["Agadez", "Diffa", "Dosso", "Maradi", "Niamey", "Tahoua", "Tillabéri", "Zinder"]
}

st.markdown("### ➕ Ajouter un enfant")

with st.form("form_enfant"):
    pays = st.selectbox("Pays", list(regions_par_pays.keys()))
    region = st.selectbox("Région", regions_par_pays[pays])
    nom = st.text_input("Nom de l’enfant")
    sexe = st.radio("Sexe", ["M", "F"], horizontal=True)
    age = st.number_input("Âge (mois)", min_value=0, max_value=60)
    poids = st.number_input("Poids (kg)", min_value=0.0, step=0.1)
    taille = st.number_input("Taille (cm)", min_value=0.0, step=0.1)
    pb = st.number_input("Périmètre brachial (cm)", min_value=0.0, step=0.1)
    oedeme = st.radio("Œdème ?", ["Non", "Oui"])
    date_mesure = st.date_input("Date de la mesure", value=date.today())
    submitted = st.form_submit_button("📨 Enregistrer")

if submitted:
    phase = ""
    couleur = ""
    conseil = ""

    if oedeme == "Oui" or pb <= 11.0:
        phase = "Famine nutritionnelle"
        couleur = "🔴"
        conseil = "⚠️ Urgence médicale. Référer immédiatement vers un centre spécialisé."
    elif pb <= 11.5:
        phase = "Malnutrition aiguë sévère (MAS)"
        couleur = "🟥"
        conseil = "⚠️ Introduire un traitement thérapeutique d'urgence. Suivi intensif requis."
    elif pb <= 12.5:
        phase = "Malnutrition aiguë modérée (MAM)"
        couleur = "🟧"
        conseil = "🍲 Complément nutritionnel recommandé (PlumpySup), suivi hebdomadaire."
    elif pb <= 12.9:
        phase = "Stress nutritionnel"
        couleur = "🟨"
        conseil = "🍌 Surveiller, diversifier l’alimentation avec bouillies enrichies, micronutriments."
    else:
        phase = "Bonne situation nutritionnelle"
        couleur = "🟢"
        conseil = "✅ Continuer une alimentation équilibrée. Contrôle régulier mensuel."

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
        "Date de mesure": date_mesure.strftime("%d/%m/%Y"),
        "Phase nutritionnelle": f"{couleur} {phase}",
        "Conseils": conseil
    }

    st.session_state["enfants"].append(enfant)
    st.success("✅ Données enregistrées avec succès !")

if st.session_state["enfants"]:
    df = pd.DataFrame(st.session_state["enfants"])
    st.markdown("### 📋 Tableau de Suivi")
    st.dataframe(df, use_container_width=True)

    st.markdown("### 📥 Export des données")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📄 Télécharger les données (CSV)", data=csv, file_name="enfants_anisan.csv", mime="text/csv")

    st.markdown("### 📌 Conseils nutritionnels")
    for i, enfant in enumerate(st.session_state["enfants"]):
        st.markdown(f"**{enfant['Nom']} ({enfant['Phase nutritionnelle']})** : {enfant['Conseils']}")
else:
    st.info("📋 Aucune donnée enregistrée pour l’instant.")
