

class RoleMessage:
    def __init__(self, role: str, message: str):
        self.role = role
        self.message = message

    def __eq__(self, other):
        return self.role == other.role and self.message == other.message