import unittest
from unittest.mock import MagicMock

from domain.model.history import History
from infrastructure.adapter.chat_application_adapter import ChatApplicationAdapter
from infrastructure.history_repository.history_repository import HistoryRepository
from infrastructure.text_generator.cohere_text_generator import CohereTextGenerator


class TestChatApplicationAdapter(unittest.TestCase):
    def setUp(self):
        # Create mocks for the dependencies.
        self.text_generator_mock = MagicMock(spec=CohereTextGenerator)
        self.history_repository_mock = MagicMock(spec=HistoryRepository)
        self.adapter = ChatApplicationAdapter(
            text_generator=self.text_generator_mock,
            history_repository=self.history_repository_mock
        )

    def test_get_generated_text(self):
        prompt = "Test prompt"
        expected_text = "Generated text from model"
        self.text_generator_mock.generate_text.return_value = expected_text

        result = self.adapter.get_generated_text(prompt)

        self.text_generator_mock.generate_text.assert_called_once_with(prompt=prompt, chat_history=[])
        self.assertEqual(result, expected_text)

    def test_get_history(self):
        chat_id = "uuid-chat-1"
        expected_history = History(chat_id, chat_history=[])
        self.history_repository_mock.get_history.return_value = expected_history

        result = self.adapter.get_history(chat_id)

        self.history_repository_mock.get_history.assert_called_once_with(chat_id)
        self.assertEqual(result, expected_history)

    def test_save_history(self):
        history = History("uuid-chat-1", chat_history=[])
        self.adapter.save_history(history)

        self.history_repository_mock.save_history.assert_called_once_with(history)
