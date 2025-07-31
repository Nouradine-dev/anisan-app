import streamlit as st
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Entraînement modèle IA
model = RandomForestClassifier(n_estimators=100, random_state=42)
X = [[6.0, 5.2, 60.0, 11.2, 0.0, 1.0], [12.0, 7.8, 72.0, 13.4, 0.0, 0.0], 
     [24.0, 10.5, 85.0, 14.1, 0.0, 1.0], [18.0, 8.0, 75.0, 12.0, 1.0, 1.0], 
     [36.0, 12.0, 90.0, 15.0, 0.0, 0.0], [9.0, 6.0, 65.0, 11.0, 1.0, 1.0], 
     [30.0, 11.0, 88.0, 14.0, 0.0, 0.0], [15.0, 7.5, 70.0, 12.5, 1.0, 0.0], 
     [21.0, 9.0, 78.0, 13.0, 0.0, 1.0], [27.0, 10.0, 83.0, 13.5, 0.0, 1.0]]
y = [2, 0, 0, 1, 0, 2, 0, 1, 1, 0]
model.fit(X, y)

def predire_nutrition(age, poids, taille, pb, oedeme, sexe):
    data = np.array([[age, poids, taille, pb, oedeme, sexe]])
    prediction = model.predict(data)[0]
    probabilites = model.predict_proba(data)[0]

    phases = {
        0: ("🟢 Bon", "Statut nutritionnel normal"),
        1: ("🟡 MAM", "Malnutrition aiguë modérée"),
        2: ("🔴 MAS", "Malnutrition aiguë sévère")
    }

    recommandations = {
        0: (
            "✅ L’enfant présente un bon état nutritionnel.",
            "🔁 Maintenez une alimentation équilibrée : allaitement exclusif jusqu’à 6 mois, puis diversification avec des aliments riches en énergie, protéines, fer, vitamine A.",
            "📅 Continuez le suivi mensuel de la croissance (poids, taille, PB)."
        ),
        1: (
            "⚠️ L’enfant est en malnutrition aiguë modérée (MAM).",
            "🍲 Enrichissez son alimentation avec des bouillies fortifiées, purée d’arachide, poisson, œufs, huile.",
            "🏥 Consultez un agent de santé pour un appui communautaire (PCMA)."
        ),
        2: (
            "🚨 L’enfant est en malnutrition aiguë sévère (MAS).",
            "🏥 Consultez immédiatement un centre CRENAS ou CRENI pour une prise en charge thérapeutique.",
            "🍽️ Donnez-lui des aliments thérapeutiques prêts à l’emploi (ATPE) si disponibles, et assurez un suivi médical rigoureux."
        )
    }

    return phases[prediction], probabilites, recommandations[prediction]

st.set_page_config(page_title="Prédiction nutritionnelle IA", page_icon="🧠")
st.title("🔬 Module IA - Prédiction nutritionnelle intégrée")

st.markdown("Remplissez les champs ci-dessous pour évaluer le statut nutritionnel d’un enfant.")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Âge (mois)", min_value=0, max_value=60, value=12)
    poids = st.number_input("Poids (kg)", min_value=2.0, max_value=25.0, value=6.5, step=0.1)
    taille = st.number_input("Taille (cm)", min_value=40, max_value=120, value=70)

with col2:
    pb = st.number_input("Périmètre brachial (cm)", min_value=8.0, max_value=20.0, value=12.0, step=0.1)
    oedeme = st.selectbox("Œdème", options=["Non", "Oui"])
    sexe = st.radio("Sexe", options=["Garçon", "Fille"])

oedeme_val = 1 if oedeme == "Oui" else 0
sexe_val = 1 if sexe == "Garçon" else 0

if st.button("📊 Lancer la prédiction"):
    try:
        (label, description), probs, conseils = predire_nutrition(age, poids, taille, pb, oedeme_val, sexe_val)

        st.success(f"**Résultat : {label}**")
        st.caption(f"{description}")

        st.markdown("### 📈 Probabilités estimées par l’IA :")
        st.write({
            "Bon": f"{probs[0]*100:.1f}%",
            "MAM": f"{probs[1]*100:.1f}%",
            "MAS": f"{probs[2]*100:.1f}%"
        })

        st.info(
            f"L'enfant a {probs[0]*100:.1f}% de chances d’être en bon état nutritionnel, "
            f"{probs[1]*100:.1f}% pour une malnutrition aiguë modérée (MAM), "
            f"et {probs[2]*100:.1f}% pour une malnutrition aiguë sévère (MAS)."
        )

        st.markdown("### 🛡️ Recommandations personnalisées :")
        for reco in conseils:
            st.write(reco)

    except Exception as e:
        st.error(f"Erreur lors de la prédiction : {e}")
