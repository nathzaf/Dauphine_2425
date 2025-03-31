import sys
from dotenv import load_dotenv
import os
import streamlit as st
import requests
from rest.model.chat_request import ChatRequest

# Charger les variables d'environnement
load_dotenv()
BASE_API_URL = "http://127.0.0.1:8000"
sys.path.append(os.getenv('PYTHONPATH'))

# Fonction pour créer une nouvelle conversation
def create_new_conversation():
    try:
        create_conversation_url = f"{BASE_API_URL}/conversation"
        response = requests.post(create_conversation_url)
        response.raise_for_status()
        return response.text.strip().strip('"')  # Supprime les espaces et les guillemets
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la création de la conversation : {e}")
        return None

# Initialiser st.session_state["conv_id"] si ce n'est pas déjà fait
if "conv_id" not in st.session_state:
    def create_default_conversation():
        new_conv_id = create_new_conversation()
        if new_conv_id:
            # Initialiser l'historique directement avec le message de l'assistant
            st.session_state["conv_id"] = new_conv_id
            st.session_state["messages"] = [{"role": "assistant", "message": "How can I help you?"}]
        else:
            st.error("Impossible de créer une nouvelle conversation par défaut.")
    
    create_default_conversation()

# Titre et description de l'application
st.title("💬 Chatbot")
st.caption("🚀 My First Chatbot using Cohere")

# Barre latérale avec description
with st.sidebar:
    st.markdown("""
        This page demonstrates how to create a memory-enabled chatbot using Cohere, showcasing
        the integration of advanced NLP capabilities in a user-friendly interface. Explore the 
        examples and learn how to build your own intelligent applications.     
    """)
    st.header("📚 Learn More")
    st.markdown("""Explore the examples and learn how to build your own intelligent applications.
        [Cohere API](https://docs.cohere.com/reference/chat)""")
    st.markdown("---")
    if st.button("New Conversation"):
        new_conv_id = create_new_conversation()
        if new_conv_id:
            # Réinitialiser l'historique avec le message de l'assistant
            st.session_state["conv_id"] = new_conv_id
            st.session_state["messages"] = [{"role": "assistant", "message": "Welcome! How can I assist you today?"}]

st.markdown("""
    On this demonstration we will be able to send request to Cohere and have a chat with history.
""")

# Fonction pour récupérer l'historique de la conversation
def get_conversation_history(conv_id):
    try:
        conversation_url = f"{BASE_API_URL}/conversation/{conv_id}"
        response = requests.get(conversation_url)
        response.raise_for_status()
        json_response = response.json()
        return json_response.get("history", {}).get("messages", [])
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération de l'historique : {e}")
        return []

# Initialiser et afficher l'historique de la conversation
history = get_conversation_history(st.session_state["conv_id"])
st.session_state["messages"] = history if history else []

# Afficher les messages existants (s'il y en a)
for msg in st.session_state["messages"]:
    role = msg.get("role", "assistant")
    content = msg.get("message", "Message non disponible")
    st.chat_message(role).write(content)

# Gestion de l'entrée utilisateur
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "message": prompt})
    st.chat_message("user").write(prompt)
    try:
        conversation_url = f"{BASE_API_URL}/conversation/{st.session_state['conv_id']}"
        request = ChatRequest(prompt=prompt)
        response = requests.post(conversation_url, json=request.to_dict())
        response.raise_for_status()
        json_response = response.json()
        history = json_response.get("history", {}).get("messages", [])
        bot_response = next(
            (msg["message"] for msg in reversed(history) if msg["role"] == "assistant"),
            "I didn't understand that."
        )
    except requests.exceptions.RequestException as e:
        bot_response = f"Error: {e}"
    st.session_state.messages.append({"role": "assistant", "message": bot_response})
    st.chat_message("assistant").write(bot_response)



