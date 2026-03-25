import streamlit as st
import pandas as pd
import os
import requests

st.set_page_config(page_title="Calculateur Biométhanisation", layout="centered")

# --- CSS DESIGN ---
st.markdown("""
<style>
h1 { color: #76D2B6; text-align: center; }
.stButton>button {
    background-color: #E0684B;
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
}
.result-box {
    background-color: #76D2B6;
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    font-size: 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("🌱 Calculateur de valorisation des biodéchets")

# --- INPUTS ---
type_client = st.selectbox(
    "Type de client",
    ["École", "Entreprise", "Soins de santé", "Restaurant", "Industrie"]
)

connait_dechets = st.radio(
    "Connaissez-vous votre quantité de biodéchets ?",
    ["Oui", "Non"]
)

repas_ou_lits = None
dechets = None

if connait_dechets == "Oui":
    dechets = st.number_input("Quantité de biodéchets (kg/jour)", min_value=0.0)
else:
    if type_client in ["École", "Entreprise", "Restaurant"]:
        repas_ou_lits = st.number_input("Nombre de repas par jour", min_value=0)
    elif type_client == "Soins de santé":
        repas_ou_lits = st.number_input("Nombre de lits", min_value=0)
    elif type_client == "Industrie": 
        repas_ou_lits = st.number_input("Production journalière", min_value=0)

# --- CALCULS ---

if st.button("Calculer"):

    if connait_dechets == "Oui":
        dechets_jour = dechets
    else:
        if type_client == "Entreprise" : 
            dechets_jour = repas_ou_lits * 0.15                 #restau entreprise, 150g déchet
        elif type_client == "Soins de santé":
            dechets_jour = repas_ou_lits * 0.15 * 2.5           # Soins de santé, 150g déchet par repas (2,5 repas par lits)              
        elif type_client == "École":
            dechets_jour = repas_ou_lits * 0.17                 # Ecole 170g déchet
        elif type_client == "Restaurant":
            dechets_jour = repas_ou_lits * 0.2                  # Restaurant 200g déceht
        elif type_client == "Industrie" : 
            dechets_jour = repas_ou_lits * 0.025                # Industrie 2,5% de la production en déchet
        else:
            dechets_jour = repas_ou_lits


    # jours activité
    if type_client == "École" : 
        jours = 200
    elif type_client == "Restaurant" : 
        jours = 230
    elif type_client == "Hopital" : 
        jours = 365

        
    else :
        jours = 310

    # calculs
    dechets_annuel = dechets_jour * jours
    biogaz = dechets_annuel * 0.17                          #pouvoir méthanogène de 0.17
    energie = biogaz * 6                                    # m3 biogaz = 6 kWh
    valeur_energie = energie * 0.06                         # prix du kWh = 0.06€
    economie_dechets = (dechets_annuel / 1000) * 150        # éconimie sur le coût de transport des déchet 150€/tonne
    gain_total = valeur_energie + economie_dechets

    # --- DISPLAY ---
    st.markdown(f"""
    <div class="result-box">
        💰 Economies estimées <br><br>
        <strong>{round(gain_total,0)} € / an</strong> <br><br>
        ♻️ Quantités de déchets estimées <br><br>
        <strong>{dechets_annuel} kg / an</strong>
    </div>
    """, unsafe_allow_html=True)

    st.write(f"🌱 {round(dechets_jour,1)} kg/jour")
    st.write(f"⚡ {round(energie,0)} kWh/an")
