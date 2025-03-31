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

st.markdown("""
    On this demonstration we will be able to send request to Cohere and have a chat with history.
""")

# Identifiant de la conversation
conv_id = "a6209fd2-5690-42ea-a7a9-068aae9c56b2"

# Fonction pour récupérer l'historique de la conversation
def get_conversation_history(conv_id):
    try:
        conversation_url = f"{BASE_API_URL}/conversation/{conv_id}"
        response = requests.get(conversation_url)
        response.raise_for_status()  # Vérifie les erreurs HTTP
        json_response = response.json()
        return json_response.get("history", {}).get("messages", [])
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération de l'historique : {e}")
        return []

# Initialiser et afficher l'historique de la conversation
history = get_conversation_history(conv_id)
st.session_state["messages"] = history if history else [{"role": "assistant", "message": "How can I help you my friend?"}]

for msg in st.session_state["messages"]:
    role = msg.get("role", "assistant")
    content = msg.get("message", "Message non disponible")
    st.chat_message(role).write(content)

# Gestion de l'entrée utilisateur
if prompt := st.chat_input():
    # Ajouter le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "message": prompt})
    st.chat_message("user").write(prompt)

    # Préparer et envoyer la requête POST à l'API
    try:
        conversation_url = f"{BASE_API_URL}/conversation/{conv_id}"
        request = ChatRequest(prompt=prompt)
        response = requests.post(conversation_url, json=request.to_dict())
        response.raise_for_status()
        json_response = response.json()

        # Extraire la réponse de l'assistant
        history = json_response.get("history", {}).get("messages", [])
        bot_response = next(
            (msg["message"] for msg in reversed(history) if msg["role"] == "assistant"),
            "I didn't understand that."
        )
    except requests.exceptions.RequestException as e:
        bot_response = f"Error: {e}"

    # Ajouter la réponse de l'assistant
    st.session_state.messages.append({"role": "assistant", "message": bot_response})
    st.chat_message("assistant").write(bot_response)



