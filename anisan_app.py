<<<<<<< HEAD
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="ANISAN - Suivi Nutritionnel", layout="centered")
st.title("🍼 Application ANISAN - Suivi Nutritionnel des Enfants")

# Pays et régions CEDEAO + CILSS
pays_regions = {
    "Bénin": ["Alibori", "Atacora", "Atlantique", "Borgou"],
    "Burkina Faso": ["Centre", "Boucle du Mouhoun", "Est", "Hauts-Bassins"],
    "Cap-Vert": ["Santiago", "São Vicente", "Fogo"],
    "Côte d’Ivoire": ["Abidjan", "Bouaké", "Korhogo", "Man"],
    "Gambie": ["Banjul", "Lower River", "Upper River"],
    "Ghana": ["Greater Accra", "Ashanti", "Northern"],
    "Guinée": ["Conakry", "Kindia", "Labé", "Nzérékoré"],
    "Guinée-Bissau": ["Bissau", "Biombo", "Cacheu"],
    "Libéria": ["Montserrado", "Bong", "Lofa"],
    "Mali": ["Kayes", "Koulikoro", "Sikasso", "Tombouctou"],
    "Mauritanie": ["Nouakchott", "Trarza", "Hodh El Gharbi", "Tagant"],
    "Niger": ["Niamey", "Maradi", "Zinder", "Tahoua"],
    "Nigeria": ["Lagos", "Kano", "Abuja", "Kaduna"],
    "Sénégal": ["Dakar", "Thiès", "Kaolack", "Ziguinchor"],
    "Sierra Leone": ["Western Area", "Bo", "Kenema"],
    "Tchad": ["N'Djamena", "Lac", "Mayo-Kebbi Est", "Ouaddaï"],
    "Togo": ["Lomé", "Kara", "Savanes"]
}

if "enfants" not in st.session_state:
    st.session_state["enfants"] = []

# Interface pays/région
st.markdown("### 🌍 Choisir le pays et la région")
pays = st.selectbox("Pays", list(pays_regions.keys()))
region = st.selectbox("Région", pays_regions[pays])

# Formulaire
st.markdown("### ➕ Ajouter un nouvel enfant")
with st.form("formulaire_enfant"):
    nom = st.text_input("Nom de l’enfant")
    sexe = st.selectbox("Sexe", ["M", "F"])
    age = st.number_input("Âge (en mois)", min_value=0, max_value=120)
    poids = st.number_input("Poids (kg)", min_value=0.0, step=0.1)
    taille = st.number_input("Taille (cm)", min_value=0.0, step=0.1)
    pb = st.number_input("Périmètre brachial (cm)", min_value=0.0, step=0.1)
    oedeme = st.radio("Œdème nutritionnel ?", ["Non", "Oui"])
    date_mesure = st.date_input("Date de la mesure", value=date.today())
    submitted = st.form_submit_button("📨 Enregistrer")

# Enregistrement et analyse
if submitted:
    phase, couleur, conseil = "", "", ""

    if oedeme == "Oui" or pb < 11.0:
        phase = "Famine nutritionnelle"
        couleur = "🟥 Rouge vif"
        conseil = "⚠️ Hospitalisation urgente recommandée. Fournir des aliments thérapeutiques (ATPE), suivi médical renforcé et prise en charge des complications."
    elif pb < 11.5:
        phase = "Urgence nutritionnelle (MAS)"
        couleur = "🔴 Rouge"
        conseil = "⚠️ Traitement immédiat requis. Fournir ATPE (Plumpy'Nut), référer à un centre nutritionnel."
    elif pb < 12.5:
        phase = "Crise nutritionnelle (MAM)"
        couleur = "🟧 Orange"
        conseil = "🍲 Fournir des aliments enrichis (Plumpy'Sup, CSB++), suivi hebdomadaire à domicile ou centre de récupération."
    elif pb < 13.0:
        phase = "Stress nutritionnel"
        couleur = "🟨 Jaune"
        conseil = "🥦 Sensibilisation sur l'alimentation diversifiée, éducation nutritionnelle, supplémentation en micronutriments."
    else:
        phase = "Phase minimale"
        couleur = "🟢 Vert"
        conseil = "✅ Suivi régulier recommandé. Continuer les bonnes pratiques alimentaires et d’hygiène."

    enfant = {
        "Nom": nom,
        "Sexe": sexe,
        "Âge (mois)": age,
        "Poids (kg)": poids,
        "Taille (cm)": taille,
        "PB (cm)": pb,
        "Œdème": oedeme,
        "Date de mesure": date_mesure.strftime("%d/%m/%Y"),
        "Pays": pays,
        "Région": region,
        "Phase nutritionnelle": f"{couleur} - {phase}",
        "Conseil": conseil
    }

    st.session_state["enfants"].append(enfant)
    st.success("✅ Données enregistrées avec succès !")
    st.info(f"**Statut :** {couleur} {phase}  
**Conseil :** {conseil}")

# Tableau des enfants
st.markdown("### 📋 Données enregistrées")
if st.session_state["enfants"]:
    df = pd.DataFrame(st.session_state["enfants"])
    st.dataframe(df, use_container_width=True)

    # Suppression
    st.markdown("### ❌ Supprimer un enregistrement")
    noms = [f"{i+1}. {e['Nom']}" for i, e in enumerate(st.session_state["enfants"])]
    selection = st.selectbox("Choisissez un enfant à supprimer", ["Aucun"] + noms)
    if selection != "Aucun":
        index = noms.index(selection)
        if st.button("Supprimer"):
            st.session_state["enfants"].pop(index)
            st.success("🗑️ Enfant supprimé.")
else:
    st.info("➡️ Enregistrez des enfants pour visualiser les données.")

# Export des données
st.markdown("### 📤 Exporter les données")
if st.session_state["enfants"]:
    df = pd.DataFrame(st.session_state["enfants"])
    csv = df.to_csv(index=False).encode('utf-8')
    try:
        df.to_excel("enfants.xlsx", index=False)
        with open("enfants.xlsx", "rb") as f:
            st.download_button("⬇️ Télécharger Excel", f, "enfants_anisan.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except:
        st.warning("📦 openpyxl requis pour exporter en Excel")
    st.download_button("⬇️ Télécharger CSV", csv, "enfants_anisan.csv", mime="text/csv")
=======

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# ---- TITRE ----
st.set_page_config(page_title="ANISAN – Suivi Nutritionnel", layout="wide")
st.title("🍼 ANISAN – Application de Suivi Nutritionnel des Enfants")

# ---- SESSION STATE INIT ----
if "data" not in st.session_state:
    st.session_state.data = []
if "country" not in st.session_state:
    st.session_state.country = "Niger"

# ---- DICTIONNAIRE DES RÉGIONS ----
countries_regions = {
    "Niger": ["Agadez", "Diffa", "Dosso", "Maradi", "Niamey", "Tahoua", "Tillabéri", "Zinder"],
    "Sénégal": ["Dakar", "Diourbel", "Fatick", "Kaffrine", "Kaolack", "Kédougou", "Kolda", "Louga", "Matam",
                "Saint-Louis", "Sédhiou", "Tambacounda", "Thiès", "Ziguinchor"]
}

# ---- FORMULAIRE ----
with st.form("form_enfant"):
    st.header("📋 Informations de l'enfant")
    col1, col2 = st.columns(2)
    with col1:
        nom = st.text_input("Nom de l’enfant")
        age = st.number_input("Âge (mois)", min_value=0, max_value=59)
        sexe = st.selectbox("Sexe", ["Masculin", "Féminin"])
        oedeme = st.selectbox("Œdème", ["Non", "Oui"])
        st.session_state.country = st.selectbox("Sélectionnez le pays", list(countries_regions.keys()), index=list(countries_regions.keys()).index(st.session_state.country))
    with col2:
        pb = st.number_input("Périmètre brachial (cm)", min_value=5.0, max_value=25.0)
        poids = st.number_input("Poids (kg)", min_value=1.0, max_value=30.0)
        taille = st.number_input("Taille (cm)", min_value=30.0, max_value=150.0)
        region = st.selectbox("Sélectionnez la région", countries_regions[st.session_state.country])

    submit = st.form_submit_button("📥 Enregistrer")
    if submit:
        st.session_state.data.append({
            "Nom": nom,
            "Âge (mois)": age,
            "Sexe": sexe,
            "PB (cm)": pb,
            "Poids (kg)": poids,
            "Taille (cm)": taille,
            "Œdème": oedeme,
            "Pays": st.session_state.country,
            "Région": region
        })
        st.success(f"✅ Enfant {nom} enregistré avec succès.")

        # ---- MINI IA EMBARQUÉE ----
        result = "Bon"
        score = 0
        if pb < 11.5 or poids < 6 or taille < 65 or oedeme == "Oui":
            result = "MAS"
            score = 2
        elif pb < 12.5 or poids < 7:
            result = "MAM"
            score = 1

        # Probabilités simulées
        probs = {"Bon": "60.0%", "MAM": "25.0%", "MAS": "15.0%"}
        if result == "MAS":
            probs = {"Bon": "10.0%", "MAM": "30.0%", "MAS": "60.0%"}
        elif result == "MAM":
            probs = {"Bon": "20.0%", "MAM": "50.0%", "MAS": "30.0%"}

        st.subheader("🤖 Résultat IA")
        st.write(f"🧠 **Statut nutritionnel prédit :** {result}")
        st.write("📊 **Détail des probabilités :**")
        st.json(probs)
        st.markdown(f"👉 Ce résultat signifie que l’enfant a **{probs[result]}** de chance d’être classé comme *{result}*.")

        st.subheader("🍽️ Recommandations personnalisées")
        if result == "Bon":
            st.markdown("- ✅ Maintenir une alimentation équilibrée adaptée à l’âge")
            st.markdown("- 👶 Allaitement exclusif jusqu’à 6 mois, puis diversification")
            st.markdown("- 📈 Suivi régulier de la croissance")
        elif result == "MAM":
            st.markdown("- ⚠️ Enrichir les repas avec protéines et lipides")
            st.markdown("- 🩺 Surveillance communautaire")
            st.markdown("- 🔁 Suivi hebdomadaire du PB et poids")
        else:
            st.markdown("- 🚨 Diriger vers un centre de récupération nutritionnelle")
            st.markdown("- 🥣 Utilisation d'ATPE (Plumpy'nut, etc.)")
            st.markdown("- 📅 Suivi médical rigoureux + traitement des infections")

# ---- CARTE FOLIUM ----
if st.session_state.data:
    latest = st.session_state.data[-1]
    st.header("📍 Localisation estimée de l’enfant")

    m = folium.Map(location=[13.5, 2.1], zoom_start=5)
    folium.Marker(
        location=[13.5, 2.1],
        popup=f"{latest['Nom']} ({latest['Région']}, {latest['Pays']})",
        tooltip="Enfant enregistré",
        icon=folium.Icon(color="red" if result == "MAS" else "orange" if result == "MAM" else "green")
    ).add_to(m)
    st_folium(m, width=700)
>>>>>>> 28c12d7fcf87d5c36bca1cd0f91349ccbf1d4468
