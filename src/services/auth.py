import bcrypt

# Gera um hash seguro para a senha informada usando bcrypt e um salt aleatório.
def password_hash(password: str):
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password_bytes, salt)
    return password_hash

import hashlib
import os
from getpass import getpass
 
# Quantas vezes o hash da senha é repetido (deixa mais difícil de quebrar).
HASH_ROUNDS = 600_000
 
# Lista onde ficam os professores cadastrados (só na memória, enquanto o programa roda).
users = []

# ======================================================================
# CAMADA 1 e 2 — ENTRADA DE DADOS + CHECAGEM (CADASTRO)
# Cada dado é pedido num laço que só termina quando o valor está correto.
# ======================================================================
 
print("\n================= Cadastro de Professor =================")
 
# --- Nome: nome e sobrenome, sem números ---
while True:
    name = " ".join(input("\nNome completo: ").split())  # tira espaços extras
    if len(name.split()) >= 2 and not any(c.isdigit() for c in name):
        break
    print("Nome inválido. Digite nome e sobrenome, sem números.")
 
# --- E-mail: um "@", sem espaços, e um ponto no domínio (ex.: nome@escola.com) ---
while True:
    email = input("\nE-mail: ").strip().lower()
    if email.count("@") == 1 and " " not in email:
        local, domain = email.split("@")
        if local != "" and "." in domain and not domain.startswith(".") and not domain.endswith("."):
            break
    print("E-mail inválido. Exemplo: nome@escola.com")
 
# --- Senha: mínimo 8 caracteres, com letras e números, digitada duas vezes ---
while True:
    password = getpass("\nSenha (mín. 8 caracteres, com letras e números): ")
 
    if len(password) < 8 or not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
        print("Senha inválida. Use pelo menos 8 caracteres, com letras e números.")
        continue
 
    if password != getpass("Confirme a senha: "):
        print("As senhas não conferem. Digite novamente.")
        continue
 
    break
 
# ======================================================================
# CAMADA 3 — ARMAZENAMENTO
# A senha nunca é guardada: guardamos só o hash dela, misturado com um "salt" aleatório.
# ======================================================================
 
salt = os.urandom(16)
password_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, HASH_ROUNDS)
 
users.append({
    "name": name,
    "email": email,
    "salt": salt,
    "password_hash": password_hash,
})
 
print("\nCadastro realizado com sucesso!")
 
# ======================================================================
# CAMADA 4 — LOGIN
# Pede e-mail e senha, refaz o hash e compara com o que está guardado (até 3 tentativas).
# ======================================================================
 
print("\n======================== Login ========================")
 
logged_user = None
 
for attempt in range(3):
    login_email = input("\nE-mail: ").strip().lower()
    login_password = getpass("Senha: ")
 
    for user in users:
        if user["email"] == login_email:
            digest = hashlib.pbkdf2_hmac("sha256", login_password.encode(), user["salt"], HASH_ROUNDS)
            if digest == user["password_hash"]:
                logged_user = user
 
    if logged_user is not None:
        break
 
    print("E-mail ou senha incorretos.")
 
if logged_user is not None:
    print(f"\nBem-vindo(a), {logged_user['name'].split()[0]}!")
else:
    print("\nMuitas tentativas incorretas. Encerrando.")
