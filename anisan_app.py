import streamlit as st

st.set_page_config(page_title="ANISAN", layout="centered")

st.title("🟢 ANISAN – Système de Suivi Nutritionnel")
st.subheader("Application de Nutrition et de Suivi Alimentaire National")
st.markdown("---")

st.header("📋 Saisie des données nutritionnelles")
with st.form("form_nutrition"):
    nom_enfant = st.text_input("Nom de l’enfant")
    age = st.number_input("Âge (mois)", min_value=0, max_value=60, step=1)
    sexe = st.radio("Sexe", ["Fille", "Garçon"])
    poids = st.number_input("Poids (kg)", min_value=0.0, step=0.1)
    taille = st.number_input("Taille (cm)", min_value=0.0, step=0.1)
    pb = st.number_input("Périmètre brachial (PB) en cm", min_value=0.0, step=0.1)
    oedeme = st.selectbox("Présence d’œdème", ["Non", "Oui"])
    submitted = st.form_submit_button("📨 Enregistrer")

    if submitted:
        # Analyse du statut nutritionnel
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

        st.success("✅ Données enregistrées avec succès !")
        st.markdown(f"**Statut nutritionnel : {couleur} {phase}**")


st.markdown("---")
st.caption("© ANISAN 2025 – Version prototype")
# -------------------------------
# 📊 ANALYSE VISUELLE DES DONNÉES
# -------------------------------
st.markdown("## 📈 Visualisation des données nutritionnelles")

if st.session_state["enfants"]:
    df = pd.DataFrame(st.session_state["enfants"])

    # Extraire le texte du statut nutritionnel
    df["Phase simplifiée"] = df["Phase nutritionnelle"].str.extract(r"[🔴🟥🟧🟨🟢] (.*)")

    # 📌 Graphique 1 : par phase nutritionnelle
    st.markdown("### 📌 Répartition par phase nutritionnelle")
    phase_count = df["Phase simplifiée"].value_counts().sort_index()
    st.bar_chart(phase_count)

    # 👦👧 Graphique 2 : par sexe
    st.markdown("### 👦👧 Répartition par sexe")
    sexe_count = df["Sexe"].value_counts()
    st.bar_chart(sexe_count)

    # ⏳ Graphique 3 : par tranche d’âge
    st.markdown("### ⏳ Répartition par tranche d’âge (mois)")
    bins = [0, 5, 11, 23, 59, 120]
    labels = ["0–5", "6–11", "12–23", "24–59", "60+"]
    df["Tranche d’âge"] = pd.cut(df["Âge (mois)"], bins=bins, labels=labels, include_lowest=True)
    age_group_count = df["Tranche d’âge"].value_counts().sort_index()
    st.bar_chart(age_group_count)
else:
    st.info("➡️ Enregistrez des enfants pour visualiser les graphiques.")
