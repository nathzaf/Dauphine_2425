import os
import sys
import uuid
import json
import requests
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.getenv('PYTHONPATH'))

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="CAF - Mon Espace",
    page_icon="📑",
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
    .highlight-section {
        border: 2px solid #0e1a40;
        border-radius: 5px;
        padding: 10px;
        background-color: #f0f4f8;
        margin-bottom: 15px;
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
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_id" not in st.session_state:
    st.session_state.chat_id = str(uuid.uuid4())
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = 0
if "history_loaded" not in st.session_state:
    st.session_state.history_loaded = False
if "show_histories" not in st.session_state:
    st.session_state.show_histories = False

# Get query parameters to determine which section to show
section = st.query_params.get("section", None)

# Header with CAF styling
st.markdown("""
<div class="caf-header">
    <div class="caf-logo">caf.fr</div>
    <div>Mon Espace</div>
</div>
""", unsafe_allow_html=True)

# Main title
st.title("Mon Espace Personnel")
st.caption("Accédez à vos documents et démarches")

# Sidebar with description
with st.sidebar:
    st.markdown("""
    # À propos
    
    Cet espace vous permet de gérer vos documents et de suivre vos démarches auprès de la CAF.
    
    ## Comment ça marche:
    1. Complétez vos informations personnelles
    2. Accédez à vos documents officiels
    3. Posez vos questions via notre assistant
    4. Suivez l'avancement de vos démarches
    """)
    
    st.divider()
    
    # User information section in sidebar
    st.subheader("📋 Mes Informations")
    
    # Highlight the profile section if coming from "Créer mon compte"
    if section == "profile":
        st.markdown('<div class="highlight-section">', unsafe_allow_html=True)
    
    with st.form("user_info_form"):
        first_name = st.text_input("Prénom")
        last_name = st.text_input("Nom")
        birth_date = st.date_input("Date de naissance", min_value=datetime(1900, 1, 1))
        id_number = st.text_input("N° Allocataire")
        
        submit_button = st.form_submit_button("Valider mes informations")
        
        if submit_button:
            if first_name and last_name and id_number:
                # Store user info in session state
                st.session_state["user_info"] = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "birth_date": birth_date.strftime("%Y-%m-%d"),
                    "id_number": id_number,
                    "submission_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state["documents_retrieved"] = True
                st.session_state["process_status"] = 33  # Set initial progress
                st.success("Informations enregistrées avec succès !")
                
                # If coming from profile section, switch to documents tab
                if section == "profile":
                    st.session_state["active_tab"] = 1
                    st.query_params["section"] = "documents"
                    st.rerun()
            else:
                st.error("Veuillez remplir tous les champs obligatoires.")
    
    # Close highlight div if needed
    if section == "profile":
        st.markdown('</div>', unsafe_allow_html=True)

# Status bar showing process advancement
st.subheader("État de votre dossier")
progress_bar = st.progress(st.session_state["process_status"])

# Status description
status_mapping = {
    0: "Veuillez compléter vos informations pour commencer",
    33: "Informations reçues. Récupération de vos documents...",
    66: "Documents récupérés. Vérification en cours...",
    100: "Processus terminé. Tous les documents sont vérifiés !"
}

current_status = status_mapping.get(st.session_state["process_status"], "En cours de traitement...")
st.info(current_status)

# Create tabs for different sections
tab1, tab2 = st.tabs(["💬 Assistant CAF", "📄 Mes Documents"])

# Set active tab based on query parameter
if section == "documents":
    st.session_state["active_tab"] = 1
elif section == "simulation":
    st.session_state["active_tab"] = 1  # Documents tab contains simulation

# Select the appropriate tab
if st.session_state["active_tab"] == 1:
    # This is a workaround since Streamlit doesn't have a direct way to programmatically select tabs
    tab_script = """
    <script>
    // Wait for tabs to be rendered
    setTimeout(function() {
        // Click on the second tab
        document.querySelector('[data-baseweb="tab-list"] [role="tab"]:nth-child(2)').click();
    }, 100);
    </script>
    """
    st.markdown(tab_script, unsafe_allow_html=True)

# Backend API configuration
API_BASE_URL = "http://127.0.0.1:8000"

def call_chat_api(prompt: str, chat_history: list) -> str:
    """Call the backend chat API"""
    try:
        # Convert chat history to the format expected by the backend
        formatted_history = []
        for msg in chat_history:
            formatted_history.append({
                "role": msg["role"].upper() if msg["role"] == "user" else "CHATBOT",
                "message": msg["content"]
            })
        
        # Prepare the request payload
        payload = {
            "prompt": prompt,
            "chat_history": formatted_history
        }
        
        # Make the API call
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=30)
        
        if response.status_code == 200:
            return response.json()["response"]
        else:
            st.error(f"Erreur API: {response.status_code}")
            return "Désolé, je rencontre des difficultés techniques. Veuillez réessayer."
            
    except requests.exceptions.ConnectionError:
        st.error("Impossible de se connecter au service de chat. Assurez-vous que le backend est démarré.")
        return "Service de chat temporairement indisponible."
    except requests.exceptions.Timeout:
        st.error("Le service de chat met trop de temps à répondre.")
        return "Le service met trop de temps à répondre. Veuillez réessayer."
    except Exception as e:
        st.error(f"Erreur inattendue: {str(e)}")
        return "Une erreur inattendue s'est produite."

def save_chat_history():
    """Save chat history to backend"""
    try:
        if not st.session_state.messages:
            return
            
        # Convert messages to backend format
        formatted_history = []
        for msg in st.session_state.messages:
            formatted_history.append({
                "role": msg["role"].upper() if msg["role"] == "user" else "CHATBOT",
                "message": msg["content"]
            })
        
        payload = {
            "chat_id": st.session_state.chat_id,
            "chat_history": formatted_history
        }
        
        response = requests.post(f"{API_BASE_URL}/histories", json=payload, timeout=10)
        
        if response.status_code == 201:
            print(f"Chat history saved successfully for chat_id: {st.session_state.chat_id}")
        else:
            print(f"Failed to save chat history: {response.status_code}")
            
    except Exception as e:
        print(f"Error saving chat history: {str(e)}")

def load_chat_history(chat_id: str = None):
    """Load chat history from backend"""
    try:
        target_chat_id = chat_id or st.session_state.chat_id
        response = requests.get(f"{API_BASE_URL}/histories/{target_chat_id}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # Convert backend format to frontend format
            messages = []
            for msg in data["chat_history"]:
                role = "user" if msg["role"] == "USER" else "assistant"
                messages.append({"role": role, "content": msg["message"]})
            
            st.session_state.messages = messages
            st.session_state.chat_id = target_chat_id
            return True
        elif response.status_code == 404:
            # Chat history doesn't exist yet, start fresh
            st.session_state.messages = []
            return True
        else:
            print(f"Error loading chat history: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Error loading chat history: {str(e)}")
        return False

def get_all_chat_histories():
    """Get all available chat histories"""
    try:
        response = requests.get(f"{API_BASE_URL}/histories", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("histories", [])
        else:
            print(f"Error getting all histories: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error getting all histories: {str(e)}")
        return []

def check_backend_status():
    """Check if backend is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        return response.status_code == 200
    except:
        return False

def display_chat_management():
    """Display chat history management"""
    st.subheader("Gestion des conversations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🆕 Nouvelle conversation", use_container_width=True):
            st.session_state.chat_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.session_state.history_loaded = False
            st.success("Nouvelle conversation créée!")
            st.rerun()
    
    with col2:
        if st.button("📋 Voir historiques", use_container_width=True):
            histories = get_all_chat_histories()
            if histories:
                st.session_state.show_histories = True
            else:
                st.info("Aucun historique disponible")
    
    # Show available histories if requested
    if st.session_state.get("show_histories", False):
        st.write("**Conversations disponibles:**")
        histories = get_all_chat_histories()
        
        if histories:
            for i, history in enumerate(histories, 1):
                chat_id = history["chat_id"]
                
                # Create a meaningful preview from the conversation
                preview = "Conversation vide"
                if history["chat_history"]:
                    # Get the first user message as preview
                    first_user_msg = None
                    for msg in history["chat_history"]:
                        if msg["role"] == "USER":
                            first_user_msg = msg["message"]
                            break
                    
                    if first_user_msg:
                        preview = first_user_msg[:70] + "..." if len(first_user_msg) > 70 else first_user_msg
                    else:
                        # If no user message, use first message
                        first_msg = history["chat_history"][0]["message"]
                        preview = first_msg[:70] + "..." if len(first_msg) > 70 else first_msg
                
                # Display conversation with number and preview
                col_preview, col_load = st.columns([4, 1])
                with col_preview:
                    st.write(f"**Conversation {i}:** {preview}")
                with col_load:
                    if st.button("Charger", key=f"load_{i}"):
                        if load_chat_history(chat_id):
                            st.session_state.history_loaded = True
                            st.session_state.show_histories = False
                            st.success(f"Conversation {i} chargée!")
                            st.rerun()
                        else:
                            st.error("Erreur lors du chargement")
        
        if st.button("Fermer"):
            st.session_state.show_histories = False
            st.rerun()

# Tab 1: Chatbot
with tab1:
    st.header("Échanger avec l'assistant CAF")
    
    # Backend status indicator
    backend_connected = check_backend_status()
    
    if backend_connected:
        st.success("🟢 Service de chat connecté")
        
        # Chat management section in sidebar or collapsible
        with st.expander("🔧 Gestion des conversations", expanded=False):
            display_chat_management()
        
        # Load chat history on first load
        if not st.session_state.history_loaded:
            load_chat_history()
            st.session_state.history_loaded = True
        
        # Create a container for the chat interface
        chat_container = st.container()
        
        # Display existing chat messages
        with chat_container:
            for msg in st.session_state.messages:
                st.chat_message(msg["role"]).write(msg["content"])
        
        # Handle new user input - this must be at the root level, not in a container
        if prompt := st.chat_input("Posez votre question..."):
            # Add user message to session state first
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Get bot response
            with st.spinner("L'assistant réfléchit..."):
                bot_response = call_chat_api(prompt, st.session_state.messages[:-1])
            
            # Add bot response to session state
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            
            # Auto-save chat history to backend
            save_chat_history()
            
            # Rerun to display the new messages
            st.rerun()
    else:
        st.error("🔴 Service de chat déconnecté - Veuillez démarrer le backend")
        st.info("Pour démarrer le backend, exécutez: `python main.py`")
        st.warning("Le chat ne sera pas disponible tant que le backend n'est pas démarré.")

# Tab 2: Documents
with tab2:
    st.header("Mes Documents CAF")
    
    if not st.session_state["user_info"]:
        st.warning("Veuillez compléter vos informations dans la barre latérale pour accéder à vos documents.")
    else:
        # Display user information
        st.subheader("Informations personnelles")
        user_info = st.session_state["user_info"]
        st.write(f"**Nom:** {user_info['last_name']} {user_info['first_name']}")
        st.write(f"**Date de naissance:** {user_info['birth_date']}")
        st.write(f"**N° Allocataire:** {user_info['id_number']}")
        st.write(f"**Date de mise à jour:** {user_info['submission_time']}")
        
        st.divider()
        
        # Display mock documents
        st.subheader("Documents officiels")
        
        # Highlight the documents section if coming from "Vérifier mes droits"
        if section == "documents":
            st.markdown('<div class="highlight-section">', unsafe_allow_html=True)
        
        # Create expandable sections for each document
        with st.expander("🆔 Attestation de droits", expanded=True):
            st.write("**Statut:** Disponible ✅")
            st.write("**Émis par:** CAF")
            st.write("**Date d'émission:** 15/05/2023")
            st.write("**Date de validité:** 14/05/2024")
            
            # Simulate document content
            st.code(json.dumps({
                "type_document": "Attestation de droits",
                "nom_allocataire": f"{user_info['last_name']} {user_info['first_name']}",
                "numero_allocataire": user_info['id_number'],
                "date_naissance": user_info['birth_date'],
                "prestations": ["Allocations Familiales", "Aide au Logement"],
                "montant_total": "453,21€",
                "date_emission": datetime.now().strftime("%Y-%m-%d")
            }, indent=2), language="json")
            
            # Button to download document
            st.download_button(
                label="Télécharger l'attestation",
                data="Ceci est une attestation de droits CAF",
                file_name="attestation_droits_caf.pdf",
                mime="application/pdf"
            )
        
        with st.expander("🏠 Attestation de logement"):
            st.write("**Statut:** En attente de vérification ⏳")
            st.write("**Émis par:** CAF")
            
            # Simulate address verification process
            if st.button("Demander une attestation de logement"):
                st.session_state["process_status"] = 66
                st.success("Demande d'attestation de logement envoyée. Notre service va traiter votre demande.")
                st.rerun()
        
        with st.expander("💼 Déclaration trimestrielle de ressources"):
            st.write("**Statut:** À compléter ❗")
            st.write("**Période concernée:** Trimestre 2 - 2023")
            st.write("**Date limite:** 30/06/2023")
            
            # Simulate tax document content
            col1, col2 = st.columns(2)
            with col1:
                st.number_input("Revenus du mois 1 (€)", min_value=0.0, step=10.0)
            with col2:
                st.number_input("Revenus du mois 2 (€)", min_value=0.0, step=10.0)
            
            col3, col4 = st.columns(2)
            with col3:
                st.number_input("Revenus du mois 3 (€)", min_value=0.0, step=10.0)
            with col4:
                st.selectbox("Situation professionnelle", ["Salarié", "Auto-entrepreneur", "Sans activité", "Étudiant", "Retraité"])
            
            # Button to submit declaration
            st.button("Soumettre ma déclaration")
        
        # Close highlight div if needed
        if section == "documents":
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Highlight the simulation section if coming from "Accéder à mes prestations"
        if section == "simulation":
            st.markdown('<div class="highlight-section">', unsafe_allow_html=True)
        
        with st.expander("📊 Simulation de droits"):
            st.write("**Statut:** Disponible ✅")
            st.write("**Description:** Simulez vos droits aux prestations CAF")
            
            # Simple simulation form
            st.selectbox("Situation familiale", ["Célibataire", "En couple", "Famille monoparentale", "Colocation"])
            st.number_input("Nombre d'enfants à charge", min_value=0, max_value=10)
            st.number_input("Revenu mensuel du foyer (€)", min_value=0.0, step=100.0)
            st.number_input("Loyer mensuel (€)", min_value=0.0, step=50.0)
            
            # Button to run simulation
            if st.button("Lancer la simulation"):
                st.success("D'après nos estimations, vous pourriez bénéficier des aides suivantes :")
                st.metric("Aide personnalisée au logement (APL)", "320,45 €/mois")
                st.metric("Prime d'activité", "175,30 €/mois")
        
        # Close highlight div if needed
        if section == "simulation":
            st.markdown('</div>', unsafe_allow_html=True)

# Button to complete the process (for demonstration)
if st.session_state["process_status"] >= 33 and st.session_state["process_status"] < 100:
    if st.button("Finaliser la vérification de mes documents"):
        st.session_state["process_status"] = 100
        st.balloons()
        st.success("Tous vos documents ont été vérifiés avec succès !")
        st.rerun() 