import streamlit as st

st.set_page_config(page_title="Calculateur Biométhanisation", layout="centered")

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
    else:
        repas_ou_lits = st.number_input("Estimation kg déchets/jour", min_value=0)

# --- CALCULS ---

if st.button("Calculer"):

    if connait_dechets == "Oui":
        dechets_jour = dechets
    else:
        if type_client == "Entreprise" or type_client == "Soins de santé":
            dechets_jour = repas_ou_lits * 0.15
        elif type_client == "École":
            dechets_jour = repas_ou_lits * 0.17
        elif type_client == "Restaurant":
            dechets_jour = repas_ou_lits * 0.2
        else:
            dechets_jour = repas_ou_lits

    # jours activité
    if type_client == "École" : 
        jours = 200
    elif type_client == "Restaurant" : 
        jours = 230
    else :
        jours = 310

    # calculs
    dechets_annuel = dechets_jour * jours
    biogaz = dechets_annuel * 0.17
    energie = biogaz * 6
    valeur_energie = energie * 0.06
    economie_dechets = (dechets_annuel / 1000) * 150
    gain_total = valeur_energie + economie_dechets

    # --- OUTPUT ---

    st.subheader("📊 Résultats")

    st.write(f"🌱 Biodéchets : **{round(dechets_jour,1)} kg/jour**")
    st.write(f"📦 Annuel : **{round(dechets_annuel/1000,2)} tonnes/an**")
    st.write(f"🔥 Biogaz : **{round(biogaz,0)} m³/an**")
    st.write(f"⚡ Energie : **{round(energie,0)} kWh/an**")

    st.success(f"💰 Economies potentielles : {round(gain_total,0)} €/an")

    # effet wow
    cafes = energie / 0.04
    st.info(f"☕ ≈ {round(cafes,0)} cafés par an")