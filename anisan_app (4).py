import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="ANISAN - Application Nutritionnelle", layout="centered")

st.title("🍼 Application ANISAN - Suivi Nutritionnel des Enfants")

if "enfants" not in st.session_state:
    st.session_state["enfants"] = []

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

    enfant = {
        "Nom": nom,
        "Sexe": sexe,
        "Âge (mois)": age,
        "Poids (kg)": poids,
        "Taille (cm)": taille,
        "PB (cm)": pb,
        "Œdème": oedeme,
        "Date de mesure": date_mesure.strftime("%d/%m/%Y"),
        "Phase nutritionnelle": f"{couleur} {phase}"
    }

    st.session_state["enfants"].append(enfant)
    st.success("✅ Données enregistrées avec succès !")

# Section tableau
st.markdown("### 📊 Tableau des enfants enregistrés")

if st.session_state["enfants"]:
    df = pd.DataFrame(st.session_state["enfants"])
    st.dataframe(df, use_container_width=True)
else:
    st.info("Aucun enfant enregistré pour l’instant.")


# Boutons de téléchargement
st.markdown("### 📥 Exporter les données")

if st.session_state["enfants"]:
    df = pd.DataFrame(st.session_state["enfants"])
    csv = df.to_csv(index=False).encode('utf-8')
    excel = df.to_excel("enfants.xlsx", index=False)

    st.download_button(
        label="📄 Télécharger au format CSV",
        data=csv,
        file_name='enfants_anisan.csv',
        mime='text/csv',
    )

    with open("enfants.xlsx", "rb") as f:
        st.download_button(
            label="📊 Télécharger au format Excel",
            data=f,
            file_name="enfants_anisan.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
