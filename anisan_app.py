import streamlit as st
import pandas as pd
import datetime
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

# --- Données CEDEAO/CILSS complètes avec coordonnées
countries_regions = {
    "Bénin": {
        "regions": {
            "Alibori": {"lat": 11.83, "lon": 2.53},
            "Atacora": {"lat": 10.50, "lon": 1.67},
            "Atlantique": {"lat": 6.50, "lon": 2.10},
            "Borgou": {"lat": 9.97, "lon": 2.60},
            "Collines": {"lat": 7.27, "lon": 2.20},
            "Donga": {"lat": 10.88, "lon": 1.68},
            "Couffo": {"lat": 6.70, "lon": 1.83},
            "Littoral": {"lat": 6.35, "lon": 2.44},
            "Mono": {"lat": 6.47, "lon": 1.85},
            "Ouémé": {"lat": 6.42, "lon": 2.63},
            "Plateau": {"lat": 7.73, "lon": 2.33},
            "Zou": {"lat": 7.43, "lon": 2.07},
        }
    },
    "Burkina Faso": {
        "regions": {
            "Boucle du Mouhoun": {"lat": 12.70, "lon": -3.10},
            "Cascades": {"lat": 10.82, "lon": -4.87},
            "Centre": {"lat": 12.37, "lon": -1.52},
            "Centre-Est": {"lat": 12.00, "lon": 0.15},
            "Centre-Nord": {"lat": 13.19, "lon": -1.42},
            "Centre-Ouest": {"lat": 12.91, "lon": -2.08},
            "Centre-Sud": {"lat": 11.00, "lon": -1.80},
            "Est": {"lat": 11.20, "lon": 0.67},
            "Hauts-Bassins": {"lat": 11.25, "lon": -4.35},
            "Nord": {"lat": 14.47, "lon": -1.57},
            "Plateau-Central": {"lat": 12.30, "lon": -1.35},
            "Sahel": {"lat": 14.33, "lon": -0.94},
            "Sud-Ouest": {"lat": 10.60, "lon": -3.10},
        }
    },
    "Cap-Vert": {
        "regions": {
            "Boa Vista": {"lat": 16.18, "lon": -22.86},
            "Brava": {"lat": 14.87, "lon": -24.71},
            "Maio": {"lat": 15.15, "lon": -23.20},
            "Sal": {"lat": 16.73, "lon": -22.95},
            "Santiago": {"lat": 15.10, "lon": -23.60},
            "Santo Antão": {"lat": 17.01, "lon": -25.07},
            "São Nicolau": {"lat": 16.57, "lon": -24.32},
            "São Vicente": {"lat": 16.90, "lon": -24.97},
        }
    },
    "Côte d'Ivoire": {
        "regions": {
            "Bas-Sassandra": {"lat": 5.19, "lon": -6.82},
            "Denguélé": {"lat": 9.38, "lon": -7.37},
            "Lacs": {"lat": 7.65, "lon": -5.10},
            "Lagunes": {"lat": 5.00, "lon": -4.08},
            "Montagnes": {"lat": 6.83, "lon": -7.62},
            "Savanes": {"lat": 9.42, "lon": -5.47},
            "Vallée du Bandama": {"lat": 7.73, "lon": -5.35},
            "Woroba": {"lat": 8.00, "lon": -7.00},
            "Yamoussoukro": {"lat": 6.82, "lon": -5.28},
            "Zanzan": {"lat": 9.77, "lon": -3.58},
        }
    },
    "Gambie": {
        "regions": {
            "Banjul": {"lat": 13.45, "lon": -16.57},
            "Central River": {"lat": 13.50, "lon": -15.40},
            "Lower River": {"lat": 13.15, "lon": -15.55},
            "North Bank": {"lat": 13.80, "lon": -15.50},
            "Upper River": {"lat": 13.30, "lon": -14.90},
            "West Coast": {"lat": 13.10, "lon": -16.10},
        }
    },
    "Ghana": {
        "regions": {
            "Ahafo": {"lat": 7.13, "lon": -2.24},
            "Ashanti": {"lat": 6.69, "lon": -1.62},
            "Bono East": {"lat": 7.84, "lon": -0.54},
            "Bono": {"lat": 7.82, "lon": -2.32},
            "Central": {"lat": 5.38, "lon": -1.45},
            "Eastern": {"lat": 6.39, "lon": -0.15},
            "Greater Accra": {"lat": 5.60, "lon": -0.20},
            "Northern": {"lat": 9.46, "lon": -0.94},
            "North East": {"lat": 10.78, "lon": -0.64},
            "Oti": {"lat": 8.79, "lon": 0.24},
            "Savannah": {"lat": 9.86, "lon": -1.36},
            "Upper East": {"lat": 10.60, "lon": -0.40},
            "Upper West": {"lat": 10.47, "lon": -2.45},
            "Volta": {"lat": 7.15, "lon": 0.35},
            "Western North": {"lat": 6.70, "lon": -2.20},
            "Western": {"lat": 5.50, "lon": -2.20},
        }
    },
    "Guinée": {
        "regions": {
            "Boké": {"lat": 10.94, "lon": -14.30},
            "Conakry": {"lat": 9.54, "lon": -13.68},
            "Faranah": {"lat": 10.00, "lon": -10.00},
            "Kankan": {"lat": 10.39, "lon": -9.31},
            "Kindia": {"lat": 10.05, "lon": -12.85},
            "Labé": {"lat": 11.31, "lon": -12.28},
            "Mamou": {"lat": 10.38, "lon": -11.29},
            "Nzérékoré": {"lat": 7.76, "lon": -8.58},
        }
    },
    "Guinée-Bissau": {
        "regions": {
            "Bafatá": {"lat": 12.18, "lon": -14.68},
            "Biombo": {"lat": 11.90, "lon": -15.56},
            "Bissau": {"lat": 11.87, "lon": -15.58},
            "Bolama": {"lat": 11.68, "lon": -15.43},
            "Cacheu": {"lat": 12.03, "lon": -16.06},
            "Gabú": {"lat": 12.26, "lon": -14.70},
            "Oio": {"lat": 12.02, "lon": -15.32},
            "Quinara": {"lat": 11.62, "lon": -15.92},
            "Tombali": {"lat": 10.70, "lon": -15.88},
        }
    },
    "Liberia": {
        "regions": {
            "Bomi": {"lat": 6.91, "lon": -11.69},
            "Bong": {"lat": 7.05, "lon": -9.51},
            "Gbarpolu": {"lat": 7.67, "lon": -10.50},
            "Grand Bassa": {"lat": 5.97, "lon": -10.03},
            "Grand Cape Mount": {"lat": 6.89, "lon": -11.55},
            "Grand Gedeh": {"lat": 6.00, "lon": -8.50},
            "Lofa": {"lat": 7.78, "lon": -10.83},
            "Margibi": {"lat": 6.56, "lon": -10.00},
            "Maryland": {"lat": 5.38, "lon": -7.98},
            "Montserrado": {"lat": 6.30, "lon": -10.80},
            "Nimba": {"lat": 7.63, "lon": -8.50},
            "Rivercess": {"lat": 6.11, "lon": -9.56},
            "Sinoe": {"lat": 5.30, "lon": -9.01},
        }
    },
    "Mali": {
        "regions": {
            "Gao": {"lat": 16.27, "lon": 0.04},
            "Kayes": {"lat": 14.45, "lon": -11.44},
            "Kidal": {"lat": 18.44, "lon": 1.41},
            "Koulikoro": {"lat": 12.86, "lon": -8.03},
            "Mopti": {"lat": 14.35, "lon": -4.00},
            "Ségou": {"lat": 13.44, "lon": -6.25},
            "Sikasso": {"lat": 11.32, "lon": -5.67},
            "Tombouctou": {"lat": 16.77, "lon": -3.00},
        }
    },
    "Niger": {
        "regions": {
            "Agadez": {"lat": 17.99, "lon": 8.00},
            "Diffa": {"lat": 13.31, "lon": 12.62},
            "Dosso": {"lat": 13.05, "lon": 3.20},
            "Maradi": {"lat": 13.49, "lon": 7.10},
            "Niamey": {"lat": 13.52, "lon": 2.10},
            "Tahoua": {"lat": 14.90, "lon": 5.27},
            "Tillabéri": {"lat": 14.23, "lon": 1.38},
            "Zinder": {"lat": 13.80, "lon": 8.99},
        }
    },
    "Nigeria": {
        "regions": {
            "Abia": {"lat": 5.53, "lon": 7.49},
            "Adamawa": {"lat": 9.32, "lon": 12.39},
            "Akwa Ibom": {"lat": 4.90, "lon": 7.85},
            "Anambra": {"lat": 6.22, "lon": 7.04},
            "Bauchi": {"lat": 10.31, "lon": 9.84},
            "Bayelsa": {"lat": 4.92, "lon": 6.22},
            "Benue": {"lat": 7.75, "lon": 8.53},
            "Borno": {"lat": 11.88, "lon": 13.15},
            "Cross River": {"lat": 5.96, "lon": 8.33},
            "Delta": {"lat": 5.52, "lon": 6.15},
            "Ebonyi": {"lat": 6.26, "lon": 8.11},
            "Edo": {"lat": 6.34, "lon": 5.63},
            "Ekiti": {"lat": 7.62, "lon": 5.22},
            "Enugu": {"lat": 6.45, "lon": 7.54},
            "Gombe": {"lat": 10.29, "lon": 11.17},
            "Imo": {"lat": 5.49, "lon": 7.03},
            "Jigawa": {"lat": 12.13, "lon": 9.59},
            "Kaduna": {"lat": 10.52, "lon": 7.44},
            "Kano": {"lat": 12.00, "lon": 8.52},
            "Katsina": {"lat": 12.99, "lon": 7.61},
            "Kebbi": {"lat": 12.45, "lon": 4.20},
            "Kogi": {"lat": 7.80, "lon": 6.73},
            "Kwara": {"lat": 8.50, "lon": 4.55},
            "Lagos": {"lat": 6.52, "lon": 3.38},
            "Nasarawa": {"lat": 8.50, "lon": 7.70},
            "Niger": {"lat": 9.62, "lon": 5.61},
            "Ogun": {"lat": 7.15, "lon": 3.35},
            "Ondo": {"lat": 7.08, "lon": 5.06},
            "Osun": {"lat": 7.45, "lon": 4.55},
            "Oyo": {"lat": 7.85, "lon": 3.93},
            "Plateau": {"lat": 9.02, "lon": 8.89},
            "Rivers": {"lat": 4.83, "lon": 7.00},
            "Sokoto": {"lat": 13.06, "lon": 5.24},
            "Taraba": {"lat": 8.90, "lon": 11.57},
            "Yobe": {"lat": 12.00, "lon": 11.75},
            "Zamfara": {"lat": 12.12, "lon": 6.00},
        }
    },
    "Sénégal": {
        "regions": {
            "Dakar": {"lat": 14.69, "lon": -17.44},
            "Diourbel": {"lat": 14.66, "lon": -16.21},
            "Fatick": {"lat": 14.27, "lon": -16.42},
            "Kaffrine": {"lat": 14.11, "lon": -15.58},
            "Kaolack": {"lat": 14.15, "lon": -16.07},
            "Kédougou": {"lat": 12.58, "lon": -12.16},
            "Kolda": {"lat": 12.50, "lon": -14.95},
            "Louga": {"lat": 15.61, "lon": -16.25},
            "Matam": {"lat": 15.67, "lon": -13.12},
            "Saint-Louis": {"lat": 16.02, "lon": -16.49},
            "Sédhiou": {"lat": 12.56, "lon": -15.59},
            "Tambacounda": {"lat": 13.75, "lon": -13.67},
            "Thiès": {"lat": 14.80, "lon": -16.91},
            "Ziguinchor": {"lat": 12.58, "lon": -16.27},
        }
    },
    "Sierra Leone": {
        "regions": {
            "Eastern": {"lat": 8.90, "lon": -11.91},
            "Northern": {"lat": 9.85, "lon": -12.84},
            "Southern": {"lat": 7.70, "lon": -11.87},
            "Western Area": {"lat": 8.48, "lon": -13.23},
        }
    },
    "Togo": {
        "regions": {
            "Centrale": {"lat": 8.62, "lon": 0.83},
            "Kara": {"lat": 9.59, "lon": 1.16},
            "Maritime": {"lat": 6.15, "lon": 1.22},
            "Plateaux": {"lat": 8.18, "lon": 1.40},
            "Savanes": {"lat": 10.75, "lon": 0.20},
        }
    },
}

# ----------------- Fonction pour calculer le statut nutritionnel (basique)

def nutrition_status(pb, oedeme):
    if oedeme == 1:
        return 2  # MAS
    if pb < 115:
        return 2  # MAS
    if 115 <= pb < 125:
        return 1  # MAM
    return 0      # Normal

def statut_to_label(statut):
    return {0:"Normal", 1:"MAM", 2:"MAS"}.get(statut, "Inconnu")

# ----------------- INITIALISATIONS

st.set_page_config(page_title="ANISAN - Suivi Nutritionnel", layout="wide")

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        "Date", "Nom", "Prenom", "Pays", "Region", "Latitude", "Longitude",
        "Poids_kg", "Taille_cm", "PB_mm", "Oedemes", "Statut"
    ])

# Sidebar logo et titre
try:
    st.sidebar.image("logo_provisoire.png", width=150)
except Exception:
    st.sidebar.write("Logo non trouvé.")
st.sidebar.title("ANISAN")

# ----------------- FORMULAIRE D’ENREGISTREMENT

# Sélection hors formulaire pour Pays + Région dynamique
pays = st.selectbox("Pays", sorted(countries_regions.keys()), key="pays_select")
regions = sorted(countries_regions[pays]["regions"].keys())
region = st.selectbox("Région", regions, key="region_select")

# Formulaire pour les autres infos
with st.form("form_enregistrement", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        nom = st.text_input("Nom de l'enfant")
        prenom = st.text_input("Prénom de l'enfant")
        date = st.date_input("Date d'enregistrement", value=datetime.date.today())

    with col2:
        poids = st.number_input("Poids (kg)", min_value=0.1, step=0.1, format="%.2f")
        taille = st.number_input("Taille (cm)", min_value=0.1, step=0.1, format="%.1f")
        pb = st.number_input("Périmètre brachial (mm)", min_value=0, step=1)
        oedeme = st.selectbox("Œdèmes bilatéraux ?", ["Non", "Oui"])
        oedeme_val = 1 if oedeme == "Oui" else 0

    submitted = st.form_submit_button("Enregistrer")

    if submitted:
        if not nom.strip() or not prenom.strip():
            st.warning("Nom et prénom sont obligatoires.")
        else:
            statut = nutrition_status(pb, oedeme_val)
            coord = countries_regions[pays]["regions"][region]
            new_entry = {
                "Date": date,
                "Nom": nom.strip(),
                "Prenom": prenom.strip(),
                "Pays": pays,
                "Region": region,
                "Latitude": coord["lat"],
                "Longitude": coord["lon"],
                "Poids_kg": poids,
                "Taille_cm": taille,
                "PB_mm": pb,
                "Oedemes": oedeme_val,
                "Statut": statut_to_label(statut)
            }
            st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_entry])], ignore_index=True)
            st.success(f"Enregistrement ajouté : {prenom} {nom} - Statut: {statut_to_label(statut)}")


# ----------------- AFFICHAGE DONNÉES ET FILTRAGE

st.markdown("---")
st.header("Données enregistrées")

df = st.session_state.data

if df.empty:
    st.info("Aucun enregistrement.")
    df_filtered = df
else:
    filt_pays = st.selectbox("Filtrer par pays", options=["Tous"] + sorted(df["Pays"].unique()))
    filt_region_opts = ["Tous"]
    if filt_pays != "Tous":
        filt_region_opts += sorted(df.loc[df["Pays"] == filt_pays, "Region"].unique())
    filt_region = st.selectbox("Filtrer par région", filt_region_opts)

    filt_statut = st.selectbox("Filtrer par statut nutritionnel", options=["Tous", "Normal", "MAM", "MAS"])

    df_filtered = df.copy()
    if filt_pays != "Tous":
        df_filtered = df_filtered[df_filtered["Pays"] == filt_pays]
    if filt_region != "Tous":
        df_filtered = df_filtered[df_filtered["Region"] == filt_region]
    if filt_statut != "Tous":
        df_filtered = df_filtered[df_filtered["Statut"] == filt_statut]

    st.dataframe(df_filtered.reset_index(drop=True))

    # Suppression
    if not df_filtered.empty:
        index_to_del = st.number_input("Index à supprimer", min_value=0, max_value=len(df_filtered)-1, step=1)
        if st.button("Supprimer l'enregistrement sélectionné"):
            idx = df_filtered.index[index_to_del]
            st.session_state.data = st.session_state.data.drop(idx).reset_index(drop=True)
            st.success(f"Enregistrement index {idx} supprimé.")
            st.experimental_rerun()

    # Téléchargement CSV
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button("Télécharger CSV", data=csv, file_name="anisan_donnees.csv", mime="text/csv")

# ----------------- GRAPHIQUE RÉPARTITION STATUT NUTRITIONNEL

if not df_filtered.empty:
    repartition = df_filtered["Statut"].value_counts().reindex(["Normal", "MAM", "MAS"]).fillna(0)
    fig, ax = plt.subplots()
    repartition.plot(kind="bar", color=["green", "orange", "red"], ax=ax)
    ax.set_ylabel("Nombre d'enfants")
    ax.set_xlabel("Statut nutritionnel")
    ax.set_title("Répartition par statut nutritionnel")
    st.pyplot(fig)

# ----------------- CONSEILS

conseils = {
    "Normal": "L'enfant est en bonne santé nutritionnelle. Continuez une alimentation équilibrée.",
    "MAM": "L'enfant présente une malnutrition aiguë modérée (MAM). Renforcer la ration alimentaire et suivre médicalement.",
    "MAS": "L'enfant présente une malnutrition aiguë sévère (MAS). Consultation médicale urgente nécessaire.",
}

if not df_filtered.empty:
    dernier_statut = df_filtered.iloc[-1]["Statut"]
    st.info(conseils.get(dernier_statut, "Pas de conseil disponible."))

# ----------------- CARTE FOLIUM

if not df_filtered.empty:
    center_lat = df_filtered["Latitude"].mean()
    center_lon = df_filtered["Longitude"].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=6)

    for _, row in df_filtered.iterrows():
        couleur = {"Normal": "green", "MAM": "orange", "MAS": "red"}.get(row["Statut"], "blue")
        popup_text = (
            f"<b>{row['Prenom']} {row['Nom']}</b><br>"
            f"Statut: {row['Statut']}<br>"
            f"Date: {row['Date']}"
        )
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=6,
            color=couleur,
            fill=True,
            fill_color=couleur,
            fill_opacity=0.7,
            popup=popup_text,
        ).add_to(m)
    st_folium(m, width=700, height=450)
else:
    st.info("Pas de données à afficher sur la carte.")
