import json
import unittest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from infrastructure.history_repository.history_repository import HistoryRepository
from rest.model.chat_request import ChatRequest
from rest.model.history_request import HistoryRequest
from rest.model.role_message_request import RoleMessageRequest
from rest.setup import create_generator_rest_adapter


class IntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        adapter = create_generator_rest_adapter()
        app = FastAPI()
        app.include_router(adapter.get_router())
        cls.client = TestClient(app)

        cls.history_repository = HistoryRepository()

    def test_history_endpoint(self):
        expected = json.dumps({
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
        })

        chat_id = "uuid-chat-1"
        response = self.client.get(f"/histories/{chat_id}")

        actual = json.dumps(response.json())

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, actual)

    def test_save_new_history(self):
        payload = HistoryRequest(chat_id="test-chat-uuid", chat_history=[
            RoleMessageRequest(role="USER", message="Hello"),
            RoleMessageRequest(role="CHATBOT", message="Hi there!"),
        ])

        response = self.client.post("/history", json=payload.to_dict())
        self.assertEqual(200, response.status_code)

        actual = self.history_repository.get_history("test-chat-uuid")
        self.assertEqual(payload.chat_history, actual.chat_history)

    def test_chat_with_history(self):
        chat_history = [
            RoleMessageRequest(role="USER", message="My name is Kim?"),
            RoleMessageRequest(role="CHATBOT",
                               message="Hello, Kim! It's nice to meet you. How can I assist you today? Whether you have questions, need help with a task, or just want to chat, I'm here for you.")
        ]
        payload = ChatRequest(prompt="Can you recall my name ?", chat_history=chat_history)

        response = self.client.post("/chat", json=payload.to_dict())

        self.assertEqual(200, response.status_code)

        print(response.json())

    def test_get_all_histories(self):
        response = self.client.get("/histories")
        self.assertEqual(200, response.status_code)

        response = json.dumps(response.json())
        print(response)