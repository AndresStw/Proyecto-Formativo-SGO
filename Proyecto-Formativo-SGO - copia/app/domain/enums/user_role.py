from enum import Enum


class UserRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    COCINERO = "COCINERO"
    CLIENTE = "CLIENTE"