from abc import ABC, abstractmethod

from domain.model.chat_history import ChatHistory
from domain.model.role_message import RoleMessage

class ChatHistoryPersistencePort(ABC):
    """
    ChatHistoryPeristencePort Interface
    =========================

    This interface defines the contract for storing chat history (conversations).
    It must be implemented by any adapter responsible for handling chat history storage
    and retrieval.
    """
    
    @abstractmethod
    def get_all_conversations(self) -> list[str]:
        """
        Retrieves all conversation GUIDs stored in the system.

        Returns:
            list: A list of conversation GUIDs.
        """
        pass

    @abstractmethod
    def get_history(self, conversation_guid: str) -> ChatHistory:
        """
        Retrieves the chat history for a specific conversation.

        Parameters:
            conversation_guid (str): The unique identifier for the conversation.

        Returns:
            ChatHistory: An object representing containing all the messages.
        """
        pass
    
    @abstractmethod
    def create_conversation(self) -> str:
        """
        Creates a new conversation and returns its unique identifier (GUID).

        Returns:
            str: The GUID of the newly created conversation.
        """
        pass


    @abstractmethod
    def add_message_to_history(self, conversation_guid: str, role_message: RoleMessage) -> ChatHistory:
        """
        Adds a new message to the chat history of a specific conversation.

        Parameters:
            conversation_guid (str): The unique identifier for the conversation.
            role_message (RoleMessage): The message to be added to the history.

        Returns:
            ChatHistory: The updated ChatHistory object after adding the new message.
        """
        pass

    @abstractmethod
    def clear_history(self, conversation_guid: str) -> ChatHistory:
        """
        Clears the chat history for a specific conversation.

        Parameters:
            conversation_guid (str): The unique identifier for the conversation.

        Returns:
            ChatHistory: The updated ChatHistory object after clearing (should be empty).
        """
        pass