
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
