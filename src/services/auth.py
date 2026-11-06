import bcrypt

# Gera um hash seguro para a senha informada usando bcrypt e um salt aleatório.
def password_hash(password: str):
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password_bytes, salt)
    return password_hash