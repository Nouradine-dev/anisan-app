import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide", page_title="Tableau de bord ANISAN")

st.title("📊 Application de suivi nutritionnel ANISAN")

# Chargement des données enfants
@st.cache_data
def charger_donnees():
    try:
        return pd.read_excel("enfants.xlsx").to_dict(orient="records")
    except:
        return []

# Initialisation des données
if "enfants" not in st.session_state:
    st.session_state["enfants"] = charger_donnees()

# Pays et régions (exemple : Sénégal)
countries_regions = {
    "Sénégal": ["Dakar", "Thiès", "Ziguinchor", "Kolda", "Saint-Louis", "Tambacounda", "Matam", "Kaolack"]
}

# Sélection dynamique
selected_country = st.selectbox("Sélectionnez le pays", list(countries_regions.keys()), key="country")
selected_region = st.selectbox("Sélectionnez la région", countries_regions[selected_country], key="region")

st.markdown("### 🧒🏽 Ajouter un enfant")

with st.form("ajout_enfant"):
    nom = st.text_input("Nom de l’enfant")
    age = st.number_input("Âge (mois)", min_value=0, max_value=60, step=1)
    poids = st.number_input("Poids (kg)", min_value=1.0, max_value=30.0, step=0.1)
    taille = st.number_input("Taille (cm)", min_value=30.0, max_value=130.0, step=0.1)
    phase = st.selectbox("Phase nutritionnelle", ["Phase minimale", "Stress", "MAM", "MAS", "Urgence", "Famine"])
    submit = st.form_submit_button("Ajouter")

    if submit and nom:
        nouvel_enfant = {
            "Nom": nom,
            "Âge (mois)": age,
            "Poids (kg)": poids,
            "Taille (cm)": taille,
            "Région": selected_region,
            "Pays": selected_country,
            "Phase nutritionnelle": phase
        }
        st.session_state["enfants"].append(nouvel_enfant)
        st.success(f"{nom} a été ajouté avec succès.")

# Fonction pour calculer les indicateurs
def calc_indicateurs_par_region(enfants):
    df = pd.DataFrame(enfants)
    indicateurs = []
    if df.empty:
        return indicateurs

    regions = df["Région"].unique()
    for region in regions:
        df_region = df[df["Région"] == region]
        total = len(df_region)
        mas_pct = (df_region["Phase nutritionnelle"].str.contains("MAS").sum() / total) * 100
        mam_pct = (df_region["Phase nutritionnelle"].str.contains("MAM").sum() / total) * 100
        stress_pct = (df_region["Phase nutritionnelle"].str.contains("Stress").sum() / total) * 100

        # Détermination de la couleur
        if mas_pct > 15:
            couleur = "darkred"         # famine
        elif mas_pct > 10 or mam_pct > 10:
            couleur = "red"             # urgence
        elif mam_pct > 5:
            couleur = "orange"          # crise
        elif stress_pct > 5:
            couleur = "yellow"          # stress
        else:
            couleur = "green"           # minimale

        indicateurs.append({
            "Région": region,
            "Total": total,
            "MAS (%)": mas_pct,
            "MAM (%)": mam_pct,
            "Stress (%)": stress_pct,
            "Couleur": couleur
        })
    return indicateurs

# Coordonnées de base des régions (à adapter à terme)
coords = {
    "Ziguinchor": [12.5, -16.3],
    "Dakar": [14.7, -17.5],
    "Thiès": [14.8, -16.9],
    "Kolda": [12.9, -14.9],
    "Saint-Louis": [16.0, -16.5],
    "Tambacounda": [13.8, -13.7],
    "Matam": [15.3, -13.3],
    "Kaolack": [14.2, -16.1]
}

# Carte dynamique
st.markdown("## 🗺️ Carte dynamique des zones à risque nutritionnel")
indicateurs = calc_indicateurs_par_region(st.session_state["enfants"])
m = folium.Map(location=[14.5, -14.5], zoom_start=6)

for ind in indicateurs:
    region = ind["Région"]
    if region in coords:
        popup_text = (
            f"{region}\n"
            f"Enfants : {ind['Total']}\n"
            f"MAS : {ind['MAS (%)']:.1f}%\n"
            f"MAM : {ind['MAM (%)']:.1f}%\n"
            f"Stress : {ind['Stress (%)']:.1f}%"
        )
        folium.CircleMarker(
            location=coords[region],
            radius=15,
            popup=popup_text,
            color=ind["Couleur"],
            fill=True,
            fill_color=ind["Couleur"],
            fill_opacity=0.6
        ).add_to(m)

st_folium(m, width=700, height=450)

# Statistiques générales
st.markdown("### 📈 Statistiques générales")
df = pd.DataFrame(st.session_state["enfants"])
st.dataframe(df, use_container_width=True)

# Export Excel
if not df.empty:
    st.download_button("📥 Télécharger les données", data=df.to_csv(index=False).encode("utf-8"),
                       file_name="donnees_nutritionnelles.csv", mime="text/csv")
