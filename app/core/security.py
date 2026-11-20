from pwdlib import PasswordHash


# Argon2id: algoritmo recomendado para proteger contraseñas.
password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Recibe una contraseña y devuelve su hash seguro.

    La contraseña original nunca se almacena en la base de datos.
    """

    if len(password) < 12:
        raise ValueError(
            "La contraseña debe tener al menos 12 caracteres."
        )

    return password_hasher.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Comprueba si una contraseña coincide con el hash almacenado.
    """

    return password_hasher.verify(
        plain_password,
        hashed_password
    )