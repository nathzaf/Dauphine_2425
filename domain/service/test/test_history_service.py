import unittest
from unittest.mock import MagicMock

from domain.model.history import History
from domain.model.role_message import RoleMessage
from domain.port.chat_application_port import ChatApplicationPort
from domain.service.history_service import HistoryService


class TestHistoryService(unittest.TestCase):
    def setUp(self):
        # Create a mock for ChatApplicationPort.
        self.chat_application_port_mock = MagicMock(spec=ChatApplicationPort)
        self.history_service = HistoryService(chat_application_port=self.chat_application_port_mock)

    def test_get_history_returns_expected_history(self):
        # Given: a chat_id and an expected history.
        chat_id = "uuid-chat-1"
        expected_history = History(chat_id, chat_history=[
            RoleMessage("USER", "Hello"),
            RoleMessage("CHATBOT", "Hi there!"),
        ])

        # When: the get_history method is called on the chat_application_port_mock.
        self.chat_application_port_mock.get_history.return_value = expected_history

        result = self.history_service.get_history(chat_id)

        # Then: the chat_application_port_mock.get_history method is called with the chat_id.
        self.chat_application_port_mock.get_history.assert_called_once_with(chat_id)
        self.assertEqual(result, expected_history)

    def test_save_history(self):
        # Given: a history object.
        history = History("uuid-chat-1", chat_history=[
            RoleMessage("USER", "Hello"),
            RoleMessage("CHATBOT", "Hi there!"),
        ])

        # When: the save_history method is called on the chat_application_port_mock.
        self.history_service.save_history(history)

        # Then: the chat_application_port_mock.save_history method is called with the history object.
        self.chat_application_port_mock.save_history.assert_called_once_with(history)
