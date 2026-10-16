from connection import get_db, close_db
from services.auth import password_hash

#User operations
def get_user(email: str):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
    except Exception as e:
        print(f"Erro ao buscar usuário: {e}")
        raise e
    finally:
        close_db(db)
    return user
    

def create_user(email: str, cpf: str, password: str):
    try:
        db = get_db()
        cursor = db.cursor()
        hashed_password = password_hash(password)
        cursor.execute("INSERT INTO users (email, cpf, password) VALUES (?, ?, ?)", (email, cpf, hashed_password))
        db.commit()
    except Exception as e:
        print(f"Erro ao criar usuário: {e}")
        db.rollback()
        raise e
    finally:
        close_db(db)


def update_user(email: str, password: str):
    try:
        db = get_db()
        cursor = db.cursor()
        hashed_password = password_hash(password)
        cursor.execute("UPDATE users SET password = ? WHERE email = ?", (hashed_password, email))
        db.commit()
    except Exception as e:
        print(f"Erro ao atualizar usuário: {e}")
        db.rollback()
        raise e
    finally:
        close_db(db)


#Activity operations
def get_activity_list():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM activity_list ORDER BY id DESC")
        activity_list = cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar atividades: {e}")
        raise e
    finally:
        close_db(db)
    return activity_list


def get_activity_list_by_tag(tag: str):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM activity_list WHERE tag = ?", (tag))
        activity_by_tag = cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar atividades por tag: {e}")
        raise e
    finally:
        close_db(db)
    return activity_by_tag


def get_activity_content(activity_id: int):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM activity_content WHERE activity_id = ?", (activity_id,))
        activity_content = cursor.fetchone()
    except Exception as e:
        print(f"Erro ao buscar conteúdo da atividade: {e}")
        raise e
    finally:
        close_db(db)
    return activity_content


def create_activity(name: str, description: str, tag: str, difficulty: str, instruction: str, answer: str, content: str, resources: str):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO activity_list (name, description, tag, difficulty) VALUES (?, ?, ?, ?)", (name, description, tag, difficulty))
        activity_id = cursor.lastrowid
        cursor.execute("INSERT INTO activity_content (activity_id, instruction, answer, content, resources) VALUES (?, ?, ?, ?, ?)", (activity_id, instruction, answer, content, resources))
        db.commit()
    except Exception as e:
        print(f"Erro ao criar atividade: {e}")
        db.rollback()
        raise e
    finally:
        close_db(db)
  
