import os
import sys
import uuid
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.getenv('PYTHONPATH'))

import streamlit as st
import json

# Page configuration
st.set_page_config(
    page_title="CAF - Mes Services",
    page_icon="🏠",
    layout="wide"
)

# Custom CSS for CAF styling
st.markdown("""
<style>
    .main {
        background-color: #f5f7fa;
    }
    .stApp header {
        background-color: #0e1a40;
        color: white;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: white;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0e1a40;
        color: white;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #e6e9ef;
        border-radius: 4px;
        margin-bottom: 10px;
    }
    .service-card {
        background-color: white;
        padding: 20px;
        border-radius: 5px;
        margin-bottom: 20px;
        border-left: 5px solid #0e1a40;
    }
    .caf-button {
        background-color: #0e1a40;
        color: white;
        border-radius: 4px;
        padding: 10px 20px;
        font-weight: bold;
        text-align: center;
        margin: 10px 0;
    }
    .caf-header {
        background-color: #0e1a40;
        color: white;
        padding: 10px;
        display: flex;
        align-items: center;
    }
    .caf-logo {
        font-size: 24px;
        font-weight: bold;
        margin-right: 10px;
    }
    .category-card {
        border-radius: 5px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .vie-personnelle {
        background-color: #e91e63;
        color: white;
    }
    .vie-professionnelle {
        background-color: #2196f3;
        color: white;
    }
    .logement {
        background-color: #9c27b0;
        color: white;
    }
    .handicap {
        background-color: #009688;
        color: white;
    }
    .steps-container {
        display: flex;
        justify-content: space-between;
        margin: 20px 0;
    }
    .step-box {
        background-color: white;
        border: 1px solid #e6e9ef;
        border-radius: 5px;
        padding: 15px;
        width: 32%;
        text-align: center;
    }
    .step-box h4 {
        margin-top: 10px;
        margin-bottom: 15px;
    }
    .step-box p {
        margin-bottom: 15px;
    }
    .step-number {
        background-color: #0e1a40;
        color: white;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 10px auto;
        font-weight: bold;
    }
    .caf-action-button {
        display: inline-block;
        background-color: #0e1a40;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 10px 15px;
        font-weight: bold;
        text-align: center;
        text-decoration: none;
        cursor: pointer;
        margin-top: 10px;
        width: 100%;
    }
    .caf-action-button.secondary {
        background-color: #f5f7fa;
        color: #0e1a40;
        border: 1px solid #0e1a40;
    }
    .caf-action-button.disabled {
        background-color: #cccccc;
        cursor: not-allowed;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables if they don't exist
if "user_info" not in st.session_state:
    st.session_state["user_info"] = None
if "documents_retrieved" not in st.session_state:
    st.session_state["documents_retrieved"] = False
if "process_status" not in st.session_state:
    st.session_state["process_status"] = 0
if "activities_checked" not in st.session_state:
    st.session_state["activities_checked"] = False

# Header with CAF styling
st.markdown("""
<div class="caf-header">
    <div class="caf-logo">caf.fr</div>
    <div>Ma CAF</div>
</div>
""", unsafe_allow_html=True)

# Main title
st.title("Mes services CAF")
st.caption("Accédez à vos droits et prestations")

# Sidebar with navigation
with st.sidebar:
    # User profile summary if logged in
    if st.session_state["user_info"]:
        user_info = st.session_state["user_info"]
        st.markdown("### 👤 Mon Compte")
        st.write(f"**Nom:** {user_info['first_name']} {user_info['last_name']}")
        st.write(f"**N° Allocataire:** {user_info['id_number']}")
        
        # Quick status indicator
        status_color = "🟢" if st.session_state["process_status"] == 100 else "🟡" if st.session_state["process_status"] > 0 else "🔴"
        st.write(f"{status_color} **Statut:** {st.session_state['process_status']}% Complété")
    else:
        st.info("Veuillez compléter votre profil pour accéder à vos droits et prestations.")
        if st.button("Accéder à mon espace"):
            st.switch_page("pages/1_Mon_Espace_CAF.py")
    
    st.divider()
    
    # Menu items
    st.markdown("### Menu")
    menu_items = [
        "📌 Actualités",
        "📝 Aides et démarches",
        "💼 Ma CAF",
        "👨‍👩‍👧‍👦 Vie de famille"
    ]
    
    for item in menu_items:
        st.button(item, use_container_width=True)

# Main content
if not st.session_state["user_info"]:
    # Welcome message for new users
    st.header("Bienvenue sur votre espace CAF")
    
    st.markdown("""
    ### Votre guichet unique pour vos prestations sociales
    
    La CAF vous accompagne dans votre quotidien :
    - ✅ Allocations familiales et aides au logement
    - 📄 Accès à vos documents et attestations
    - 🔍 Simulation de vos droits
    - 📱 Suivi de vos démarches en ligne
    
    Pour commencer, accédez à votre espace personnel et complétez votre profil.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Se connecter", use_container_width=True):
            st.switch_page("pages/1_Mon_Espace_CAF.py")
    with col2:
        st.button("Simuler mes droits", use_container_width=True, disabled=True)
        
    # Comment ça marche section with properly styled buttons
    st.divider()
    st.subheader("Comment ça marche")
    
    # Using Streamlit native components instead of custom HTML
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 1️⃣ Créer mon compte")
        st.markdown("Complétez votre profil avec vos informations personnelles pour accéder à vos droits.")
        st.link_button("Créer mon compte", "pages/1_Mon_Espace_CAF.py", use_container_width=True, type="primary")
    
    with col2:
        st.markdown("### 2️⃣ Vérifier mes droits")
        st.markdown("Notre système vérifie automatiquement vos droits aux différentes prestations.")
        st.link_button("Vérifier mes droits", "pages/1_Mon_Espace_CAF.py", use_container_width=True, type="secondary")
    
    with col3:
        st.markdown("### 3️⃣ Accéder à mes prestations")
        st.markdown("Accédez à vos prestations et téléchargez vos attestations en quelques clics.")
        st.link_button("Accéder à mes prestations", "pages/1_Mon_Espace_CAF.py", use_container_width=True, type="secondary")
        
else:
    # Dashboard for logged-in users
    st.header(f"Bonjour, {st.session_state['user_info']['first_name']} !")
    
    # Check eligibility for activities based on documents
    if not st.session_state["activities_checked"] and st.session_state["documents_retrieved"]:
        with st.spinner("Vérification de vos droits..."):
            # Simulate checking process
            import time
            time.sleep(1)
            st.session_state["activities_checked"] = True
    
    # Status cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Documents vérifiés", value=f"{st.session_state['process_status']}%", delta="Complété" if st.session_state["process_status"] == 100 else "En cours")
    
    with col2:
        eligible_activities = 0
        if st.session_state["process_status"] >= 33:
            eligible_activities = 3
        if st.session_state["process_status"] >= 66:
            eligible_activities = 7
        if st.session_state["process_status"] == 100:
            eligible_activities = 12
            
        st.metric(label="Prestations disponibles", value=eligible_activities, delta=f"+{eligible_activities}" if eligible_activities > 0 else None)
    
    with col3:
        pending_actions = 3 if st.session_state["process_status"] < 100 else 0
        st.metric(label="Actions en attente", value=pending_actions, delta="-3" if st.session_state["process_status"] == 100 else None, delta_color="inverse")
    
    # Prestations section
    st.subheader("Droits et prestations")
    
    if st.session_state["process_status"] == 0:
        st.warning("Veuillez compléter votre profil pour accéder à vos droits et prestations.")
        if st.button("Compléter mon profil"):
            st.switch_page("pages/1_Mon_Espace_CAF.py")
    else:
        # Filter tabs
        filter_tab1, filter_tab2, filter_tab3, filter_tab4 = st.tabs(["Tout", "Vie personnelle", "Vie professionnelle", "Logement"])
        
        with filter_tab1:
            # Vie personnelle section
            st.markdown("""
            <div class="category-card vie-personnelle">
                <h3>Vie personnelle</h3>
                <p>Paje (Prestation d'accueil du jeune enfant), Af (Allocations familiales), Allocation de soutien familial (Asf), Allocation de rentrée scolaire, Cmg (Complément de mode de garde)...</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state["process_status"] >= 33:
                with st.expander("👶 Prestation d'accueil du jeune enfant (Paje)", expanded=True):
                    st.write("**Statut:** Disponible")
                    st.write("**Montant estimé:** 184,62€ par mois")
                    st.write("**Documents requis:** Attestation d'identité ✅")
                    st.button("S'informer sur les aides", key="paje_info")
                
                with st.expander("👨‍👩‍👧‍👦 Allocations familiales (Af)"):
                    st.write("**Statut:** Disponible")
                    st.write("**Montant estimé:** Selon le nombre d'enfants et vos ressources")
                    st.write("**Documents requis:** Attestation d'identité ✅, Justificatif de domicile ❌")
                    st.button("S'informer sur les aides", key="af_info", disabled=st.session_state["process_status"] < 66)
            
            # Vie professionnelle section
            st.markdown("""
            <div class="category-card vie-professionnelle">
                <h3>Vie professionnelle</h3>
                <p>Prime d'activité, RSA (Revenu de solidarité active)...</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state["process_status"] >= 33:
                with st.expander("💼 Prime d'activité"):
                    st.write("**Statut:** Disponible")
                    st.write("**Montant estimé:** Selon vos revenus d'activité")
                    st.write("**Documents requis:** Attestation d'identité ✅, Justificatifs de revenus ✅")
                    st.button("S'informer sur les aides", key="prime_activite_info")
            
            # Logement section
            st.markdown("""
            <div class="category-card logement">
                <h3>Logement</h3>
                <p>Aides au logement, APL, Logement étudiant, Prime de déménagement, Prêt à l'amélioration de l'habitat...</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state["process_status"] >= 66:
                with st.expander("🏠 Aide personnalisée au logement (APL)"):
                    st.write("**Statut:** Disponible")
                    st.write("**Montant estimé:** Selon votre situation locative et vos ressources")
                    st.write("**Documents requis:** Attestation d'identité ✅, Justificatif de domicile ✅")
                    st.button("S'informer sur les aides", key="apl_info")
            
            # Handicap section
            st.markdown("""
            <div class="category-card handicap">
                <h3>Handicap</h3>
                <p>Aah (Allocation aux adultes handicapés), Aeeh (Allocation d'éducation de l'enfant handicapé), Ajpp (Allocation journalière de présence parentale)...</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state["process_status"] == 100:
                with st.expander("♿ Allocation aux adultes handicapés (AAH)"):
                    st.write("**Statut:** Disponible")
                    st.write("**Montant estimé:** Jusqu'à 956,65€ par mois")
                    st.write("**Documents requis:** Tous les documents vérifiés ✅")
                    st.button("S'informer sur les aides", key="aah_info")
        
        with filter_tab2:
            # Vie personnelle section
            st.markdown("""
            <div class="category-card vie-personnelle">
                <h3>Vie personnelle</h3>
                <p>Paje (Prestation d'accueil du jeune enfant), Af (Allocations familiales), Allocation de soutien familial (Asf), Allocation de rentrée scolaire, Cmg (Complément de mode de garde)...</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state["process_status"] >= 33:
                with st.expander("👶 Prestation d'accueil du jeune enfant (Paje)"):
                    st.write("**Statut:** Disponible")
                    st.write("**Montant estimé:** 184,62€ par mois")
                    st.write("**Documents requis:** Attestation d'identité ✅")
                    st.button("S'informer sur les aides", key="paje_info_2")
                
                with st.expander("👨‍👩‍👧‍👦 Allocations familiales (Af)"):
                    st.write("**Statut:** Disponible")
                    st.write("**Montant estimé:** Selon le nombre d'enfants et vos ressources")
                    st.write("**Documents requis:** Attestation d'identité ✅, Justificatif de domicile ❌")
                    st.button("S'informer sur les aides", key="af_info_2", disabled=st.session_state["process_status"] < 66)
                
                with st.expander("🏫 Allocation de rentrée scolaire"):
                    st.write("**Statut:** Disponible")
                    st.write("**Montant estimé:** Entre 392,05€ et 428,03€ par enfant")
                    st.write("**Documents requis:** Attestation d'identité ✅, Certificat de scolarité ❌")
                    st.button("S'informer sur les aides", key="rentree_scolaire_info")
        
        with filter_tab3:
            # Vie professionnelle section
            st.markdown("""
            <div class="category-card vie-professionnelle">
                <h3>Vie professionnelle</h3>
                <p>Prime d'activité, RSA (Revenu de solidarité active)...</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state["process_status"] >= 33:
                with st.expander("💼 Prime d'activité"):
                    st.write("**Statut:** Disponible")
                    st.write("**Montant estimé:** Selon vos revenus d'activité")
                    st.write("**Documents requis:** Attestation d'identité ✅, Justificatifs de revenus ✅")
                    st.button("S'informer sur les aides", key="prime_activite_info_2")
            
            if st.session_state["process_status"] >= 66:
                with st.expander("📊 RSA (Revenu de solidarité active)"):
                    st.write("**Statut:** Disponible")
                    st.write("**Montant estimé:** Jusqu'à 607,75€ pour une personne seule")
                    st.write("**Documents requis:** Attestation d'identité ✅, Justificatifs de revenus ✅")
                    st.button("S'informer sur les aides", key="rsa_info")
        
        with filter_tab4:
            # Logement section
            st.markdown("""
            <div class="category-card logement">
                <h3>Logement</h3>
                <p>Aides au logement, APL, Logement étudiant, Prime de déménagement, Prêt à l'amélioration de l'habitat...</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state["process_status"] >= 33:
                with st.expander("🏠 Aide personnalisée au logement (APL)"):
                    st.write("**Statut:** Disponible")
                    st.write("**Montant estimé:** Selon votre situation locative et vos ressources")
                    st.write("**Documents requis:** Attestation d'identité ✅, Justificatif de domicile ✅")
                    st.button("S'informer sur les aides", key="apl_info_2")
            
            if st.session_state["process_status"] >= 66:
                with st.expander("🎓 Logement étudiant"):
                    st.write("**Statut:** Disponible")
                    st.write("**Montant estimé:** Selon votre situation")
                    st.write("**Documents requis:** Attestation d'identité ✅, Certificat de scolarité ✅")
                    st.button("S'informer sur les aides", key="logement_etudiant_info")
                
                with st.expander("🚚 Prime de déménagement"):
                    st.write("**Statut:** Disponible")
                    st.write("**Montant estimé:** Selon les frais réels de déménagement")
                    st.write("**Documents requis:** Attestation d'identité ✅, Justificatif de domicile ✅")
                    st.button("S'informer sur les aides", key="demenagement_info")
    
    # Recent activity feed
    st.divider()
    st.subheader("Activités récentes")
    
    if st.session_state["process_status"] > 0:
        activities = []
        
        if st.session_state["process_status"] >= 33:
            activities.append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "action": "Informations personnelles soumises",
                "status": "Terminé"
            })
        
        if st.session_state["process_status"] >= 66:
            activities.append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "action": "Vérification d'adresse demandée",
                "status": "Terminé"
            })
        
        if st.session_state["process_status"] == 100:
            activities.append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "action": "Vérification des documents terminée",
                "status": "Terminé"
            })
        
        # Display activities in a table
        st.dataframe(
            activities,
            column_config={
                "date": "Date & Heure",
                "action": "Action",
                "status": st.column_config.TextColumn(
                    "Statut",
                    help="Statut actuel de l'activité",
                    width="medium"
                )
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("Aucune activité récente. Complétez votre profil pour commencer.")