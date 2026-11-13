import bcrypt
from src.database.storage import get_user, create_user

def password_hash(password):
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)  # Gera um salt aleatório com 12 rounds de complexidade
    password_hash = bcrypt.hashpw(password_bytes, salt)
    return password_hash


# Verifica se a senha informada corresponde ao hash armazenado no banco de dados.
def verify_password(password, hashed):
    password_bytes = password.encode('utf-8')
    verified_password = bcrypt.checkpw(password_bytes, hashed)
    return verified_password


# Verifica se a senha informada corresponde ao hash armazenado no banco de dados.
def check_login(email, password):
    try:
        user = get_user(email)
        if user and verify_password(password, user["password"]):
            return user
        else:
            raise ValueError("\nE-mail ou senha incorretos. Tente novamente.")
    except Exception as e:
        raise ValueError(f"{e}")


# Registra um novo usuário no banco de dados, garantindo que o e-mail e o CPF sejam únicos.
def register_user(name, email, cpf, password):
    # Verifica se o e-mail já está cadastrado
    if get_user(email) or get_user(cpf) is not None:
        raise ValueError("Usuário já cadastrado. Por favor, use outro e-mail ou cpf.")

    # Gera o hash da senha
    password_hash_value = password_hash(password)

    try:
        create_user(name, email, cpf, password_hash_value)
    except Exception as e:
        raise ValueError(f"{e}")
