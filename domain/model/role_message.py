from dataclasses import dataclass

@dataclass
class RoleMessage:
    role: str
    message: str