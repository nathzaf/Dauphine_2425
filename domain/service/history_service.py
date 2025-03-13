from abc import ABC, abstractmethod

from domain.model.role_message import RoleMessage

class HistoryService(ABC):
    def __init__(self):
        self.history = []

    @abstractmethod
    def save_message(self, role_message: RoleMessage):
        pass

    @abstractmethod
    def get_history(self):
        pass

    @abstractmethod
    def clear_history(self):
        pass