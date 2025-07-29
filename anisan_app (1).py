import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="ANISAN - Application Nutritionnelle", layout="centered")

st.title("🍼 Application ANISAN - Suivi Nutritionnel des Enfants")

# Initialisation de la mémoire pour enregistrer les enfants
if "enfants" not in st.session_state:
    st.session_state["enfants"] = []

# Formulaire de saisie
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
        "Statut nutritionnel": f"{couleur} {phase}"
    }

    st.session_state["enfants"].append(enfant)
    st.success("✅ Données enregistrées avec succès !")

# Affichage du tableau des enfants enregistrés
st.markdown("### 📊 Tableau des enfants enregistrés")

if st.session_state["enfants"]:
    df = pd.DataFrame(st.session_state["enfants"])
    st.dataframe(df, use_container_width=True)

    # Export CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📄 Télécharger les données (CSV)",
        data=csv,
        file_name='donnees_anisan.csv',
        mime='text/csv',
    )

    # Export Excel
    excel_path = "donnees_anisan.xlsx"
    df.to_excel(excel_path, index=False)
    with open(excel_path, "rb") as f:
        st.download_button(
            label="📊 Télécharger les données (Excel)",
            data=f,
            file_name="donnees_anisan.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("Aucune donnée enregistrée pour le moment.")
