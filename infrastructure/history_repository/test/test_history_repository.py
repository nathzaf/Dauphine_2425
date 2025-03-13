import json
import unittest
from unittest.mock import patch, mock_open

from domain.model.history import History
from domain.model.role_message import RoleMessage
from infrastructure.history_repository.history_repository import HistoryRepository


class TestHistoryRepository(unittest.TestCase):

    def setUp(self):
        self.json_data = json.dumps([
            {
                "chat_id": "uuid-chat-1",
                "chat_history": [
                    {
                        "role": "USER",
                        "message": "Who discovered gravity?"
                    },
                    {
                        "role": "CHATBOT",
                        "message": "The man who is widely credited with discovering gravity is Sir Isaac Newton"
                    }
                ]
            }
        ])
        self.history_repository = HistoryRepository()

    @patch("builtins.open", new_callable=mock_open, read_data='[]')
    def test_get_history_with_no_existing_chat(self, mock_file):
        history = self.history_repository.get_history("non-existing-chat")
        self.assertEqual(history.chat_id, "non-existing-chat")
        self.assertEqual(history.chat_history, [])
        mock_file.assert_called_with(self.history_repository.path, 'r')

    @patch("builtins.open", new_callable=mock_open)
    def test_get_history_with_existing_chat(self, mock_file):
        mock_file.return_value.read.return_value = self.json_data

        history = self.history_repository.get_history("uuid-chat-1")
        self.assertEqual(history.chat_id, "uuid-chat-1")

        expected_messages = [
            RoleMessage("USER", "Who discovered gravity?"),
            RoleMessage("CHATBOT", "The man who is widely credited with discovering gravity is Sir Isaac Newton")
        ]
        self.assertEqual(history.chat_history, expected_messages)
        mock_file.assert_called_with(self.history_repository.path, 'r')

    @patch("builtins.open", new_callable=mock_open)
    def test_save_history_with_new_chat(self, mock_file):
        mock_file.return_value.read.return_value = self.json_data

        expected_data = json.loads(self.json_data)
        expected_data.append({
            "chat_id": "uuid-chat-2",
            "chat_history": [
                {
                    "role": "USER",
                    "message": "What is the capital of France?"
                },
                {
                    "role": "CHATBOT",
                    "message": "The capital of France is Paris"
                }
            ]
        })

        new_history = History("uuid-chat-2", [RoleMessage("USER", "What is the capital of France?"),
                                              RoleMessage("CHATBOT", "The capital of France is Paris")])

        self.history_repository.save_history(new_history)

    @patch("builtins.open", new_callable=mock_open)
    def test_save_history_updates_existing_chat(self, mock_file):
        mock_file.return_value.read.return_value = self.json_data

        # Expected result: the new conversation should be appended to the existing chat's history.
        expected_data = json.loads(self.json_data)
        expected_data[0]["chat_history"].append([
            {"role": "USER", "message": "What is the speed of light?"},
            {"role": "CHATBOT", "message": "Approximately 299,792 km/s"}
        ])

        # Create a new history update for an existing chat.
        new_history = History("uuid-chat-1", [
            RoleMessage("USER", "What is the speed of light?"),
            RoleMessage("CHATBOT", "Approximately 299,792 km/s")
        ])

        # Call the method under test.
        self.history_repository.save_history(new_history)


    @patch("builtins.open", new_callable=mock_open)
    def test_get_all_histories(self, mock_file):
        mock_file.return_value.read.return_value = self.json_data

        histories = self.history_repository.get_all_histories()
        self.assertEqual(len(histories), 1)

        expected_history = History("uuid-chat-1", [
            RoleMessage("USER", "Who discovered gravity?"),
            RoleMessage("CHATBOT", "The man who is widely credited with discovering gravity is Sir Isaac Newton")
        ])

        self.assertEqual(histories[0].chat_id, expected_history.chat_id)
        self.assertEqual(histories[0].chat_history, expected_history.chat_history)
