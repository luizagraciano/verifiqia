import bcrypt

def password_hash(password: str):
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password_bytes, salt)
    return password_hash

"""VERIFIQIA — US-01: cadastro de conta de professor.

Execução:  flask --app app run
Variáveis: VERIFIQIA_SECRET_KEY, VERIFIQIA_CPF_KEY (chave Fernet), VERIFIQIA_CPF_INDEX_KEY, VERIFIQIA_DB
"""
import os
import sqlite3
import uuid
from datetime import datetime, timezone
 
from flask import Flask, flash, redirect, render_template, request, url_for

import banco
import seguranca
import validacao

MSG_SUCESSO = "Conta criada com sucesso"
MSG_DUPLICADO = "Já existe uma conta com este e-mail ou CPF"
MSG_FALHA = "Não foi possível criar a conta agora. Tente novamente em instantes."


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("VERIFIQIA_SECRET_KEY"),
        CPF_ENC_KEY=os.environ.get("VERIFIQIA_CPF_KEY"),
        CPF_INDEX_KEY=os.environ.get("VERIFIQIA_CPF_INDEX_KEY"),
        DATABASE=os.environ.get("VERIFIQIA_DB", "verifiqia.db"),
        TERMOS_VERSAO="2026-10",
        MAX_CONTENT_LENGTH=16 * 1024,
        SESSION_COOKIE_SAMESITE="Lax",  # em produção, defina também SESSION_COOKIE_SECURE=True
    )
    app.config.update(config or {})
    for chave in ("SECRET_KEY", "CPF_ENC_KEY", "CPF_INDEX_KEY"):
        if not app.config[chave]:
            raise RuntimeError(f"Configuração ausente: {chave}")

    protetor = seguranca.ProtetorCPF(app.config["CPF_ENC_KEY"], app.config["CPF_INDEX_KEY"])
    app.extensions["protetor_cpf"] = protetor
    banco.init_db(app.config["DATABASE"])

    def pagina(valores=None, erros=None, aviso=None):
        return render_template(
            "cadastro.html", v=valores or {}, e=erros or {}, aviso=aviso,
            etapas=validacao.ETAPAS, familiaridade=validacao.FAMILIARIDADE_IA,
            internet=validacao.ACESSO_INTERNET)

    @app.after_request
    def cabecalhos(resp):
        resp.headers["Cache-Control"] = "no-store"
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["Referrer-Policy"] = "no-referrer"
        return resp

    @app.get("/")
    def inicio():
        return redirect(url_for("cadastro"))

    @app.get("/login")
    def login():  # apenas destino do redirecionamento; autenticação fica fora da US-01
        return render_template("login.html")

    @app.route("/cadastro", methods=["GET", "POST"])
    def cadastro():
        if request.method == "GET":
            return pagina()

        valores = {k: v for k, v in request.form.items() if k != "senha"}  # nunca devolve a senha
        dados, erros = validacao.validar_cadastro(request.form)
        if erros:
            return pagina(valores, erros), 400

        agora = datetime.now(timezone.utc).isoformat(timespec="seconds")
        registro = {
            "id": str(uuid.uuid4()),
            "nome": dados["nome"],
            "email": dados["email"],
            "cpf_cifrado": protetor.cifrar(dados["cpf"]),
            "cpf_indice": protetor.indice(dados["cpf"]),
            "senha_hash": seguranca.hash_senha(dados["senha"]),
            "etapa_ano": dados["etapa_ano"],
            "familiaridade_ia": dados["familiaridade_ia"],
            "acesso_internet": dados["acesso_internet"],
            "termos_versao": app.config["TERMOS_VERSAO"],
            "termos_aceitos_em": agora,
            "criado_em": agora,
        }
        try:
            banco.inserir_professor(app.config["DATABASE"], registro)
        except (sqlite3.Error, OSError) as exc:
            if isinstance(exc, sqlite3.IntegrityError) and str(exc).startswith("UNIQUE"):
                return pagina(valores, aviso=MSG_DUPLICADO), 409
            app.logger.error("Falha ao gravar cadastro de professor: %s", type(exc).__name__)
            return pagina(valores, aviso=MSG_FALHA), 500

        flash(MSG_SUCESSO)
        return redirect(url_for("login"))

    return app