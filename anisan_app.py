import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
import os

# -------------------------------
# Données CEDEAO/CILSS complètes
# -------------------------------
CEDEAO_CILSS = {
    "Bénin": ["Alibori", "Atacora", "Atlantique", "Borgou", "Collines", "Donga",
              "Kouffo", "Littoral", "Mono", "Ouémé", "Plateau", "Zou"],
    "Burkina Faso": ["Boucle du Mouhoun", "Cascades", "Centre", "Centre-Est", "Centre-Nord",
                     "Centre-Ouest", "Centre-Sud", "Est", "Hauts-Bassins", "Nord",
                     "Plateau-Central", "Sahel", "Sud-Ouest"],
    "Cap-Vert": ["Santo Antão", "São Vicente", "São Nicolau", "Sal", "Boa Vista", "Maio",
                 "Santiago", "Fogo", "Brava"],
    "Côte d'Ivoire": ["Abidjan", "Bas-Sassandra", "Comoé", "Denguélé", "Gôh-Djiboua",
                      "Lacs", "Lagunes", "Montagnes", "Savanes", "Vallée du Bandama",
                      "Woroba", "Yamoussoukro", "Zanzan"],
    "Gambie": ["Banjul", "Kanifing", "Brikama", "Mansakonko", "Kerewan", "Janjanbureh",
               "Basse"],
    "Ghana": ["Ahafo", "Ashanti", "Bono", "Bono East", "Central", "Eastern",
              "Greater Accra", "North East", "Northern", "Oti", "Savannah",
              "Upper East", "Upper West", "Volta", "Western", "Western North"],
    "Guinée": ["Boké", "Conakry", "Faranah", "Kankan", "Kindia", "Labé", "Mamou", "Nzérékoré"],
    "Guinée-Bissau": ["Bissau", "Biombo", "Bafatá", "Gabú", "Oio", "Cacheu", "Bolama/Bijagos",
                       "Quinara", "Tombali"],
    "Liberia": ["Bomi", "Bong", "Gbarpolu", "Grand Bassa", "Grand Cape Mount", "Grand Gedeh",
                "Grand Kru", "Lofa", "Margibi", "Maryland", "Montserrado", "Nimba",
                "River Cess", "River Gee", "Sinoe"],
    "Mali": ["Bamako", "Gao", "Kayes", "Kidal", "Koulikoro", "Mopti", "Segou", "Sikasso",
             "Tombouctou"],
    "Mauritanie": ["Adrar", "Assaba", "Brakna", "Dakhlet Nouadhibou", "Gorgol", "Guidimaka",
                   "Hodh Ech Chargui", "Hodh El Gharbi", "Inchiri", "Nouakchott", "Tagant",
                   "Tiris Zemmour", "Trarza"],
    "Niger": ["Agadez", "Diffa", "Dosso", "Maradi", "Tahoua", "Tillabéri", "Zinder", "Niamey"],
    "Nigeria": ["Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue",
                "Borno", "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", "Gombe",
                "Imo", "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", "Kwara",
                "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo", "Osun", "Oyo", "Plateau",
                "Rivers", "Sokoto", "Taraba", "Yobe", "Zamfara", "FCT Abuja"],
    "Sénégal": ["Dakar", "Diourbel", "Fatick", "Kaffrine", "Kaolack", "Kédougou", "Kolda",
                "Louga", "Matam", "Saint-Louis", "Sédhiou", "Tambacounda", "Thiès", "Ziguinchor"],
    "Sierra Leone": ["Eastern", "Northern", "Southern", "Western Area"],
    "Togo": ["Centrale", "Kara", "Maritime", "Plateaux", "Savanes"]
}

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(page_title="ANISAN - Suivi Nutritionnel", layout="wide")

# Logo avec adaptation
logo_path = os.path.join(os.path.dirname(__file__), "logo_provisoire.png")
cols = st.columns([1,4])
with cols[0]:
    if os.path.exists(logo_path):
        st.image(logo_path, width=120)
with cols[1]:
    st.markdown("<h1 style='color:green'>ANISAN - Suivi Nutritionnel</h1>"
                "<h3 style='color:blue'>CILSS / CEDEAO / AES</h3>", unsafe_allow_html=True)

# -------------------------------
# DataFrame initial
# -------------------------------
if "df_enfants" not in st.session_state:
    st.session_state.df_enfants = pd.DataFrame(columns=[
        "Nom","Prenom","Date_naissance","Date_enregistrement","Poids","Taille","PB_mm",
        "Oedeme","Quartier/Commune","Pays","Region","IMC","Statut","Prediction",
        "Conseils","Age","Latitude","Longitude"
    ])

# -------------------------------
# Pays et régions dynamiques
# -------------------------------
pays = st.selectbox("Pays", list(CEDEAO_CILSS.keys()))
regions_dispo = CEDEAO_CILSS[pays]
region = st.selectbox("Région", regions_dispo)

# -------------------------------
# Formulaire
# -------------------------------
with st.form("enregistrement_form"):
    nom = st.text_input("Nom de l'enfant")
    prenom = st.text_input("Prénom de l'enfant")
    date_naissance = st.date_input("Date de naissance")
    date_enregistrement = st.date_input("Date d'enregistrement", datetime.today())
    poids = st.number_input("Poids (kg)", min_value=0.0, step=0.1)
    taille = st.number_input("Taille (cm)", min_value=0.0, step=0.1)
    pb_mm = st.number_input("PB (mm)", min_value=0.0, step=0.1)
    oedeme = st.selectbox("Présence d’œdèmes bilatéraux ?", ["Non", "Oui"])
    quartier = st.text_input("Quartier/Commune (optionnel)")

    submitted = st.form_submit_button("Enregistrer")
    
    if submitted:
        imc = poids / ((taille/100)**2) if taille>0 else 0
        age = int((date_enregistrement - date_naissance).days / 30.44)
        lat, lon = 0.0, 0.0  # Coordonnées fictives pour l'exemple, on peut intégrer API si souhaité

        # Statut et prédiction IA
        if imc < 14:
            statut = "MAS"
            prediction = "Malnutrition Aiguë Sévère"
            conseils = "Suivi médical urgent requis, alimentation thérapeutique."
        elif imc < 16:
            statut = "MAM"
            prediction = "Malnutrition Aiguë Modérée"
            conseils = "Suivi nutritionnel conseillé, renforcer alimentation."
        else:
            statut = "Normal"
            prediction = "Normal"
            conseils = "État nutritionnel acceptable, maintenir alimentation équilibrée."

        # Ajout au DataFrame
        st.session_state.df_enfants.loc[len(st.session_state.df_enfants)] = [
            nom, prenom, date_naissance, date_enregistrement, poids, taille, pb_mm,
            oedeme, quartier, pays, region, round(imc,2), statut, prediction, conseils,
            age, lat, lon
        ]

# -------------------------------
# Affichage prédiction & conseils
# -------------------------------
if submitted:
    st.subheader("Prédictions et conseils IA")
    st.write(f"Enfant : {prenom} {nom}")
    st.write(f"Statut nutritionnel : **{statut}**")
    st.write(f"Prédiction IA : {prediction}")
    st.write(f"Conseils : {conseils}")
    if statut != "Normal":
        st.warning(f"Alerte : {prenom} {nom} présente {statut}")

# -------------------------------
# Affichage tableau et carte
# -------------------------------
if not st.session_state.df_enfants.empty:
    st.subheader("Données enregistrées")
    df = st.session_state.df_enfants
    st.dataframe(df)
    
    # Histogramme IMC
    fig, ax = plt.subplots()
    ax.hist(df["IMC"], bins=10, color="skyblue", edgecolor="black")
    ax.set_title("Répartition IMC des enfants")
    ax.set_xlabel("IMC")
    ax.set_ylabel("Nombre d'enfants")
    st.pyplot(fig)
    
    # Carte
    st.subheader("Carte de localisation")
    map_center = [df["Latitude"].mean(), df["Longitude"].mean()]
    carte = folium.Map(location=map_center, zoom_start=6)
    for idx, row in df.iterrows():
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=8,
            color='blue',
            fill=True,
            fill_color='blue',
            popup=f"{row['Prenom']} {row['Nom']} - IMC {row['IMC']} - {row['Statut']}"
        ).add_to(carte)
    st_folium(carte, width=700, height=450)

    # Export CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Télécharger CSV", data=csv, file_name="enfants.csv", mime="text/csv")

    # Export PDF
    pdf_bytes = BytesIO()
    c = canvas.Canvas(pdf_bytes, pagesize=A4)
    c.drawString(50, 800, "Rapport ANISAN")
    y = 750
    for i, row in df.iterrows():
        c.drawString(50, y, f"{row['Prenom']} {row['Nom']} | {row['Pays']} - {row['Region']} | "
                             f"Quartier: {row['Quartier/Commune']} | Age: {row['Age']} mois | "
                             f"IMC: {row['IMC']} | Statut: {row['Statut']} | PB: {row['PB_mm']} mm | "
                             f"Conseils: {row['Conseils']}")
        y -= 20
        if y < 50:
            c.showPage()
            y = 800
    c.save()
    pdf_bytes.seek(0)
    st.download_button("Télécharger PDF", data=pdf_bytes, file_name="rapport_anisan.pdf", mime="application/pdf")
