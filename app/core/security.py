import bcrypt
from pwdlib import PasswordHash


# Argon2id: algoritmo recomendado para proteger contraseñas.
password_hasher = PasswordHash.recommended()


def hash_password(password: str, minimum_length: int = 12) -> str:
    """
    Recibe una contraseña y devuelve su hash seguro.

    La contraseña original nunca se almacena en la base de datos.
    """

    if len(password) < minimum_length:
        raise ValueError(
            f"La contraseña debe tener al menos {minimum_length} caracteres."
        )

    return password_hasher.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Comprueba si una contraseña coincide con el hash almacenado.
    """

    if hashed_password.startswith(("$2a$", "$2b$", "$2y$")):
        # Some bcrypt hashes use the $2y$ prefix; Python bcrypt expects $2b$.
        bcrypt_hash = hashed_password
        if bcrypt_hash.startswith("$2y$"):
            bcrypt_hash = "$2b$" + bcrypt_hash[4:]
        try:
            return bcrypt.checkpw(
                plain_password.encode("utf-8"),
                bcrypt_hash.encode("ascii"),
            )
        except (ValueError, TypeError):
            return False

    try:
        return password_hasher.verify(plain_password, hashed_password)
    except Exception:
        # Un hash legado dañado no debe convertir un login fallido en un 500.
        return False


def password_needs_rehash(hashed_password: str) -> bool:
    """Indica si un hash heredado debe actualizarse al algoritmo actual."""
    return hashed_password.startswith(("$2a$", "$2b$", "$2y$"))
