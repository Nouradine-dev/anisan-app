
import streamlit as st
import pandas as pd
from datetime import date

# Configuration de la page
st.set_page_config(page_title="ANISAN - Suivi Nutritionnel", layout="centered")
st.title("🍼 ANISAN - Application de Suivi Nutritionnel des Enfants")

# Pays et Régions enregistrés
pays_regions = {
    "Bénin": ["Alibori", "Atacora", "Atlantique", "Borgou", "Collines", "Donga", "Kouffo", "Littoral", "Mono", "Ouémé", "Plateau", "Zou"],
    "Burkina Faso": ["Boucle du Mouhoun", "Cascades", "Centre", "Centre-Est", "Centre-Nord", "Centre-Ouest", "Centre-Sud", "Est", "Hauts-Bassins", "Nord", "Plateau-Central", "Sahel", "Sud-Ouest"],
    "Cap-Vert": ["Santiago", "São Vicente", "Sal", "Fogo"],
    "Côte d'Ivoire": ["Abidjan", "Yamoussoukro", "Bas-Sassandra", "Comoé", "Denguélé", "Gôh-Djiboua", "Lacs", "Montagnes", "Sassandra-Marahoué", "Savanes", "Vallée du Bandama", "Woroba", "Zanzan"],
    "Gambie": ["Banjul", "Lower River", "Central River", "North Bank", "Upper River", "West Coast"],
    "Ghana": ["Greater Accra", "Ashanti", "Western", "Eastern", "Northern", "Volta", "Central", "Upper East", "Upper West", "Bono"],
    "Guinée": ["Boké", "Conakry", "Faranah", "Kankan", "Kindia", "Labé", "Mamou", "N’Zérékoré"],
    "Guinée-Bissau": ["Bafata", "Biombo", "Bissau", "Bolama", "Cacheu", "Gabu", "Oio", "Quinara", "Tombali"],
    "Liberia": ["Bomi", "Bong", "Gbarpolu", "Grand Bassa", "Grand Cape Mount", "Grand Gedeh", "Grand Kru", "Lofa", "Margibi", "Maryland", "Montserrado", "Nimba", "River Cess", "River Gee", "Sinoe"],
    "Mali": ["Bamako", "Gao", "Kayes", "Kidal", "Koulikoro", "Mopti", "Ségou", "Sikasso", "Tombouctou"],
    "Mauritanie": ["Adrar", "Assaba", "Brakna", "Dakhlet Nouadhibou", "Gorgol", "Guidimakha", "Hodh Ech Chargui", "Hodh El Gharbi", "Inchiri", "Nouakchott", "Tagant", "Tiris Zemmour", "Trarza"],
    "Niger": ["Agadez", "Diffa", "Dosso", "Maradi", "Niamey", "Tahoua", "Tillabéri", "Zinder"],
    "Nigeria": ["Abuja", "Lagos", "Kano", "Kaduna", "Rivers", "Oyo", "Katsina", "Borno", "Bauchi", "Enugu", "Cross River"],
    "Sénégal": ["Dakar", "Diourbel", "Fatick", "Kaffrine", "Kaolack", "Kédougou", "Kolda", "Louga", "Matam", "Saint-Louis", "Sédhiou", "Tambacounda", "Thiès", "Ziguinchor"],
    "Sierra Leone": ["Eastern", "Northern", "Southern", "Western Area"],
    "Togo": ["Centrale", "Kara", "Maritime", "Plateaux", "Savanes"]
}

# Initialisation de la session
if "enfants" not in st.session_state:
    st.session_state["enfants"] = []

# Formulaire de saisie
st.markdown("### ➕ Ajouter un nouvel enfant")

with st.form("form_enfant"):
    pays = st.selectbox("Pays", list(pays_regions.keys()))
    region = st.selectbox("Région", pays_regions[pays])
    nom = st.text_input("Nom de l’enfant")
    sexe = st.selectbox("Sexe", ["M", "F"])
    age = st.number_input("Âge (en mois)", min_value=0, max_value=120)
    poids = st.number_input("Poids (kg)", min_value=0.0, step=0.1)
    taille = st.number_input("Taille (cm)", min_value=0.0, step=0.1)
    pb = st.number_input("Périmètre brachial (cm)", min_value=0.0, step=0.1)
    oedeme = st.radio("Œdème nutritionnel ?", ["Non", "Oui"])
    date_mesure = st.date_input("Date de la mesure", value=date.today())

    submit = st.form_submit_button("📨 Enregistrer")

# Analyse OMS/FAO et conseils personnalisés
def analyser_statut(pb, oedeme):
    if oedeme == "Oui" or pb <= 11.0:
        return "Famine nutritionnelle", "🔴", "Traitement d’urgence immédiat (hospitalisation recommandée)"
    elif pb <= 11.5:
        return "Malnutrition aiguë sévère (MAS)", "🟥", "Diriger vers un centre de réhabilitation nutritionnelle (CRENI)"
    elif pb <= 12.5:
        return "Malnutrition aiguë modérée (MAM)", "🟧", "Suivi communautaire + supplémentation nutritionnelle"
    elif pb <= 12.9:
        return "Stress nutritionnel", "🟨", "Conseils nutritionnels et suivi mensuel"
    else:
        return "Phase minimale (normale)", "🟢", "Continuer les bonnes pratiques nutritionnelles"

# Enregistrement des données
if submit:
    phase, couleur, recommandation = analyser_statut(pb, oedeme)

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
        "Date de mesure": date_mesure.strftime("%d/%m/%Y"),
        "Statut nutritionnel": f"{couleur} {phase}",
        "Recommandation": recommandation
    }

    st.session_state["enfants"].append(enfant)
    st.success(f"✅ Enfant enregistré avec statut : {phase}")

# Affichage du tableau
st.markdown("### 📋 Données enregistrées")
if st.session_state["enfants"]:
    df = pd.DataFrame(st.session_state["enfants"])
    st.dataframe(df, use_container_width=True)
else:
    st.info("Aucun enfant enregistré pour l’instant.")

# Téléchargement
st.markdown("### 📥 Exporter les données")
if st.session_state["enfants"]:
    df = pd.DataFrame(st.session_state["enfants"])
    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button("📄 Télécharger au format CSV", data=csv, file_name="anisan_enfants.csv", mime="text/csv")
