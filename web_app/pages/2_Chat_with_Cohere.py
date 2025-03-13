import os
import sys
import uuid

from dotenv import load_dotenv

from rest.model.history_request import HistoryRequest
from rest.model.role_message_request import RoleMessageRequest

load_dotenv()

sys.path.append(os.getenv('PYTHONPATH'))

import streamlit as st
import requests

from rest.model.chat_request import ChatRequest

# Titles
st.title("💬 Chatbot with Memory")
st.caption("🚀 My First Chatbot using Cohere")

# FastAPI created at
chat_api_url = "http://127.0.0.1:8000/chat"
history_api_url = "http://127.0.0.1:8000/histories"

# Sidebar with description
with st.sidebar:
    st.markdown("""
                This page demonstrates how to create a memory-enabled chatbot using Cohere, showcasing
                the integration of advanced NLP capabilities in a user-friendly interface. Explore the 
                examples and learn how to build your own intelligent applications.     
                """)
    st.header("📚 Learn More")
    st.markdown("""Explore the examples and learn how to build your own intelligent applications.
                [Cohere API](https://docs.cohere.com/reference/chat)""")

    # Ajout de la section Historiques
    st.divider()
    st.header("📜 Historiques des conversations")

    # Bouton pour créer une nouvelle conversation
    if st.button("➕ Nouvelle conversation", key="new_chat_button"):
        new_uuid = str(uuid.uuid4())
        st.session_state["chat_id"] = new_uuid
        st.session_state["current_chat_id"] = "new"
        st.session_state["messages"] = [{"role": "assistant", "content": "Comment puis-je vous aider?"}]
        st.rerun()

    # Récupération de tous les historiques
    try:
        all_histories_response = requests.get(history_api_url)
        all_histories = all_histories_response.json().get("histories", [])

        if not all_histories:
            st.info("Aucune conversation disponible")
        else:
            # Créer un conteneur défilable pour les historiques
            scroll_container = st.container()

            # Conteneur pour la liste défilable avec une classe CSS
            with st.container():

                # Pour chaque historique, créer un élément cliquable
                for history_item in all_histories:
                    history_id = history_item.get("chat_id")

                    # Utiliser le premier message utilisateur comme titre
                    chat_title = f"Conversation {history_id[:8]}..."
                    for msg in history_item.get("chat_history", []):
                        if msg.get("role") == "USER":
                            chat_title = msg.get("message", "")[:25]
                            if len(msg.get("message", "")) > 25:
                                chat_title += "..."
                            break

                    # Définir une classe CSS pour l'élément sélectionné
                    is_selected = "current_chat_id" in st.session_state and st.session_state[
                        "current_chat_id"] == history_id
                    item_class = "history-item selected" if is_selected else "history-item"

                    # Créer un bouton pour chaque conversation
                    if st.button(chat_title, key=f"history_{history_id}"):
                        st.session_state["chat_id"] = history_id
                        st.session_state["current_chat_id"] = history_id

                        # Récupérer l'historique spécifique
                        specific_history_response = requests.get(f"{history_api_url}/{history_id}")
                        specific_history = specific_history_response.json()

                        # Réinitialiser les messages dans la session
                        st.session_state["messages"] = []

                        # Ajouter les messages de l'historique à la session
                        for msg in specific_history.get("chat_history", []):
                            role = "user" if msg.get("role") == "USER" else "assistant"
                            content = msg.get("message", "")
                            st.session_state["messages"].append({"role": role, "content": content})

                        if not st.session_state["messages"]:
                            st.session_state["messages"] = [
                                {"role": "assistant", "content": "Comment puis-je vous aider?"}]

                        st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Erreur lors de la récupération des historiques: {str(e)}")

st.markdown(
    """
    On this demonstration we will be able to send request to Cohere and have a chat with history 
    """
)

chat_id = ""
chat_history = []

# Code copied from https://github.com/streamlit/llm-examples/blob/main/Chatbot.py
# Initialize the chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    st.session_state["chat_id"] = uuid.uuid4()
    chat_id = st.session_state["chat_id"]

# Display the chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
    chat_id = st.session_state["chat_id"]
    chat_history = requests.get(history_api_url + f"/{chat_id}").json().get("chat_history", [])

# When a user submits a message
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    ##st.chat_message("assistant").write("Hello Buddy")

    # Display the user's message
    st.chat_message("user").write(prompt)

    user_role_message = RoleMessageRequest(role="USER", message=prompt)

    # Prepare the payload for the API request
    request = ChatRequest(prompt=prompt, chat_history=chat_history)

    # Send the request to the API
    try:
        response = requests.post(chat_api_url, json=request.to_dict())
        response.raise_for_status()  # Will raise an exception for HTTP errors
        bot_response = response.json().get("response", "I didn't understand that.")
    except requests.exceptions.RequestException as e:
        bot_response = f"Error: {e}"

    # Display the bot's response
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    st.chat_message("assistant").write(bot_response)

    bot_role_message = RoleMessageRequest(role="CHATBOT", message=bot_response)

    # Save the chat history
    request = HistoryRequest(chat_id=str(chat_id), chat_history=[user_role_message, bot_role_message])
    response = requests.post(history_api_url, json=request.to_dict())
