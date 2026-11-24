from enum import Enum


class UserRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    MESERO = "MESERO"
    COCINERO = "COCINERO"
    CAJERO = "CAJERO"
    CLIENTE = "CLIENTE"
