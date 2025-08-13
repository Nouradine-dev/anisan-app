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
# Données CEDEAO/CILSS avec régions et coordonnées
# -------------------------------
CEDEAO_CILSS = {
    "Bénin": {"Alibori": (10.0333, 11.6333), "Atacora": (10.2, 1.8333), "Atlantique": (6.4833, 2.3),
              "Borgou": (9.7667, 3.25), "Collines": (7.2, 2.3), "Donga": (9.9833, 2.6667),
              "Kouffo": (6.6333, 1.8333), "Littoral": (6.3667, 2.4333), "Mono": (6.6333, 1.7833),
              "Ouémé": (6.4833, 2.6167), "Plateau": (7.9833, 1.6167), "Zou": (7.1667, 2.25)},
    "Burkina Faso": {"Boucle du Mouhoun": (12.5, -3.0), "Cascades": (10.5, -4.0), "Centre": (12.35, -1.5167),
                     "Centre-Est": (11.5, -0.85), "Centre-Nord": (13.0, -1.0), "Centre-Ouest": (12.0, -2.0),
                     "Centre-Sud": (11.0, -1.5), "Est": (11.5, 0.0), "Hauts-Bassins": (11.25, -4.25),
                     "Nord": (14.0, 0.0), "Plateau-Central": (12.5, -1.5), "Sahel": (14.0, 0.0),
                     "Sud-Ouest": (10.5, -3.0)},
    "Cap-Vert": {"Santo Antão": (17.1, -25.5), "São Vicente": (16.8833, -24.9833)},
    "Côte d'Ivoire": {"Abidjan": (5.336, -4.026), "Yamoussoukro": (6.816, -5.277)},
    "Gambie": {"Banjul": (13.4549, -16.5790), "Kanifing": (13.4430, -16.6737)},
    "Ghana": {"Greater Accra": (5.6, -0.2), "Ashanti": (6.6667, -1.6167)},
    "Guinée": {"Conakry": (9.5, -13.7), "Kindia": (10.05, -12.85)},
    "Guinée-Bissau": {"Bissau": (11.85, -15.5833), "Cacheu": (12.0, -16.25)},
    "Liberia": {"Montserrado": (6.3, -10.8), "Bong": (7.0, -9.25)},
    "Mali": {"Bamako": (12.65, -8.0), "Kayes": (13.4667, -11.4167)},
    "Mauritanie": {"Nouakchott": (18.0735, -15.9582), "Nouadhibou": (20.9333, -17.0333)},
    "Niger": {"Niamey": (13.5125, 2.1125), "Zinder": (13.8, 8.9833)},
    "Nigeria": {"Lagos": (6.5244, 3.3792), "Abuja": (9.0578, 7.4951)},
    "Sénégal": {"Dakar": (14.6928, -17.4467), "Thiès": (14.7833, -16.95)},
    "Sierra Leone": {"Freetown": (8.4844, -13.2344), "Bo": (7.9667, -11.7333)},
    "Togo": {"Lomé": (6.1167, 1.2167), "Kara": (9.555, 1.85)}
}

# -------------------------------
# Configuration page
# -------------------------------
st.set_page_config(page_title="ANISAN - Système de Suivi Nutritionnel (CILSS / CEDEAO / AES)", layout="wide")

# Logo robuste
logo_path = os.path.join(os.path.dirname(__file__), "logo_provisoire.png")
if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        st.sidebar.image(f.read(), use_container_width=True)
else:
    st.sidebar.write("Logo non trouvé")

st.title("ANISAN - Système de Suivi Nutritionnel (CILSS / CEDEAO / AES)")

# -------------------------------
# Initialisation DataFrame
# -------------------------------
if "df_enfants" not in st.session_state:
    st.session_state.df_enfants = pd.DataFrame(columns=[
        "Nom","Prenom","Date_naissance","Date_enregistrement","Poids","Taille","Oedeme",
        "Pays","Region","IMC","Statut","Prediction","Conseils","Age","Latitude","Longitude"
    ])

# -------------------------------
# Initialisation regions
# -------------------------------
if "regions_dispo" not in st.session_state:
    st.session_state.regions_dispo = []
if "last_pays" not in st.session_state:
    st.session_state.last_pays = None

# -------------------------------
# Formulaire d'enregistrement
# -------------------------------
with st.form("enregistrement_form"):
    nom = st.text_input("Nom de l'enfant")
    prenom = st.text_input("Prénom de l'enfant")
    date_naissance = st.date_input("Date de naissance")
    date_enregistrement = st.date_input("Date d'enregistrement", datetime.today())
    poids = st.number_input("Poids (kg)", min_value=0.0, step=0.1)
    taille = st.number_input("Taille (cm)", min_value=0.0, step=0.1)
    oedeme = st.selectbox("Présence d’œdèmes bilatéraux ?", ["Non", "Oui"])
    
    # Pays / Régions dynamiques
    def update_regions():
        st.session_state.regions_dispo = list(CEDEAO_CILSS[st.session_state.pays_select].keys())

    pays = st.selectbox(
        "Pays",
        list(CEDEAO_CILSS.keys()),
        key="pays_select",
        on_change=update_regions
    )

    if st.session_state.regions_dispo:
        region = st.selectbox("Région", st.session_state.regions_dispo, key="region_select")
    else:
        region = st.selectbox("Région", ["Aucune région disponible"])

    submitted = st.form_submit_button("Enregistrer")
    
    if submitted:
        imc = poids / ((taille/100)**2) if taille>0 else 0
        age = int((date_enregistrement - date_naissance).days / 30.44)
        lat, lon = CEDEAO_CILSS[pays][region]

        # Classification nutritionnelle
        if imc < 14:
            statut = "MAS"
            prediction = ("Malnutrition Aiguë Sévère. Suivi médical urgent requis. "
                          "Alimentation thérapeutique recommandée.")
        elif imc < 16:
            statut = "MAM"
            prediction = ("Malnutrition Aiguë Modérée. Suivi nutritionnel conseillé. "
                          "Renforcer l'alimentation avec nutriments clés.")
        else:
            statut = "Normal"
            prediction = ("État nutritionnel acceptable. Maintenir alimentation équilibrée.")

        st.session_state.df_enfants.loc[len(st.session_state.df_enfants)] = [
            nom, prenom, date_naissance, date_enregistrement, poids, taille, oedeme, pays, region,
            round(imc,2), statut, prediction, prediction, age, lat, lon
        ]
        st.success(f"Enregistrement effectué pour {prenom} {nom}.")
        st.info(f"Statut nutritionnel: {statut}\nConseils: {prediction}")

# -------------------------------
# Affichage des données
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
        c.drawString(50, y, f"{row['Prenom']} {row['Nom']} | {row['Pays']} - {row['Region']} | Age: {row['Age']} mois | IMC: {row['IMC']} | Statut: {row['Statut']} | Conseils: {row['Conseils']}")
        y -= 20
        if y < 50:
            c.showPage()
            y = 800
    c.save()
    pdf_bytes.seek(0)
    st.download_button("Télécharger PDF", data=pdf_bytes, file_name="rapport_anisan.pdf", mime="application/pdf")
