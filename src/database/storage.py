from src.database.connection import get_db, close_db
from src.services.auth import password_hash

#User operations
def get_user(email: str):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT * 
            FROM users 
            WHERE email = ?
            """, 
            (email,)
        )
        user = cursor.fetchone()

    except Exception as e:
        raise ValueError(f"Erro ao buscar usuário: {e}")
    finally:
        close_db(db)
    return dict(user) if user else None
    

def create_user(username: str, email: str, cpf: str, password: str):
    try:
        db = get_db()
        cursor = db.cursor()
        hashed_password = password_hash(password)
        cursor.execute("""
            INSERT INTO users (username, email, cpf, password) 
            VALUES (?, ?, ?, ?)
            """, 
            (username, email, cpf, hashed_password)
        )
        db.commit()
    except Exception as e:
        raise ValueError(f"Erro ao criar usuário: {e}")
        db.rollback()
    finally:
        close_db(db)


def update_user(email: str, password: str):
    try:
        db = get_db()
        cursor = db.cursor()
        hashed_password = password_hash(password)
        cursor.execute("""
            UPDATE users 
            SET password = ? 
            WHERE email = ?
            """, 
            (hashed_password, email)
        )
        db.commit()
    except Exception as e:
        db.rollback()
        raise ValueError(f"Erro ao atualizar usuário: {e}")
    finally:
        close_db(db)


#Activity operations
def get_activity_list():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT * 
            FROM activity_list 
            ORDER BY id DESC
            """
        )
        activity_list = cursor.fetchall()

    except Exception as e:
        raise ValueError(f"Erro ao buscar atividades: {e}")
    finally:
        close_db(db)
    return [dict(activity) for activity in activity_list] if activity_list else None


def get_activity_list_by_tag(tag: str):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT * 
            FROM activity_list 
            WHERE tag = ?
            """, 
            (tag,)
        )
        activity_by_tag = cursor.fetchall()
        
    except Exception as e:
        raise ValueError(f"Erro ao buscar atividades por tag: {e}")
    finally:
        close_db(db)
    return [dict(activity) for activity in activity_by_tag] if activity_by_tag else None


def get_activity_by_id(activity_id: int):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT activity_list.*, 
            activity_content.instruction, 
            activity_content.answer, 
            activity_content.resources
            FROM activity_list
            LEFT JOIN activity_content ON activity_list.id = activity_content.activity_id 
            WHERE activity_list.id = ?
            """, 
            (activity_id,)
        )
        activity = cursor.fetchone()

    except Exception as e:
        raise ValueError(f"Erro ao buscar atividade: {e}")
    finally:
        close_db(db)
    return dict(activity) if activity else None


def get_activity_content(activity_id: int):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT * 
            FROM activity_content 
            WHERE activity_id = ?
            """, 
            (activity_id,)
        )

        activity_content = cursor.fetchone()

        if not activity_content:
            raise ValueError(f"Nenhum conteúdo encontrado para a atividade: {activity_id}")
        
    except Exception as e:
        raise ValueError(f"Erro ao buscar conteúdo da atividade: {e}")
    finally:
        close_db(db)
    return dict(activity_content) if activity_content else None


def create_activity(name: str, description: str, tag: str, difficulty: str, instruction: str, answer: str, resources: str):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO activity_list (name, description, tag, difficulty) 
            VALUES (?, ?, ?, ?)
            """, 
            (name, description, tag, difficulty)
        )
        activity_id = cursor.lastrowid
        cursor.execute("""
            INSERT INTO activity_content (activity_id, instruction, answer, resources) 
            VALUES (?, ?, ?, ?)
            """, 
            (activity_id, instruction, answer, resources)
        )
        db.commit()
    except Exception as e:
        db.rollback()
        raise ValueError(f"Erro ao criar atividade: {e}")
    finally:
        close_db(db)


def update_activity(activity_id: int, name: str, description: str, tag: str, difficulty: str, instruction: str, answer: str, resources: str):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE activity_list 
            SET name = COALESCE(?, name), 
                description = COALESCE(?, description), 
                tag = COALESCE(?, tag), 
                difficulty = COALESCE(?, difficulty) 
            WHERE id = ?
            """, 
            (name, description, tag, difficulty, activity_id)
        )
                       
        cursor.execute("""
            UPDATE activity_content 
            SET instruction = COALESCE (?, instruction), 
                answer = COALESCE (?, answer), 
                resources = COALESCE (?, resources) 
            WHERE activity_id = ?
            """, 
            (instruction, answer, resources, activity_id)
        )
        db.commit()
    except Exception as e:
        db.rollback()
        raise ValueError(f"Erro ao atualizar atividade: {e}")
    finally:
        close_db(db)


def delete_activity(activity_id: int):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            DELETE FROM activity_content 
            WHERE activity_id = ?
            """, 
            (activity_id,)
        )
        cursor.execute("""
            DELETE FROM activity_list 
            WHERE id = ?
            """, 
            (activity_id,)
        )
        db.commit()
    except Exception as e:
        db.rollback()
        raise ValueError(f"Erro ao deletar atividade: {e}")
    finally:
        close_db(db)
