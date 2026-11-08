from src.database.storage import create_activity, get_offline_activity_list_by_tag, get_db, close_db

# As tags fixas do sistema
TAGS_SISTEMA = ["Ética", "Matemática", "Português", "História", "Ciências", "Geografia"]

def salvar_atividade_offline(name: str, description: str, tag: str, difficulty: str, instruction: str, answer: str, resources: str):
    """Salva uma atividade na tabela exclusiva de offline."""
    if tag not in TAGS_SISTEMA:
        raise ValueError(f"A tag '{tag}' é inválida. O sistema só aceita: {TAGS_SISTEMA}")
    
    db = get_db()
    try:
        cursor = db.cursor()
        
        # 1. Salva na tabela offline_activity_list
        cursor.execute("""
            INSERT INTO offline_activity_list (name, description, tag, difficulty) 
            VALUES (?, ?, ?, ?)
            """, (name, description, tag, difficulty))
        
        activity_id = cursor.lastrowid 
        
        # 2. Salva na tabela offline_activity_content
        cursor.execute("""
            INSERT INTO offline_activity_content (activity_id, instruction, answer, resources) 
            VALUES (?, ?, ?, ?)
            """, (activity_id, instruction, answer, resources))
        
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise ValueError(f"Erro ao salvar atividade offline: {e}")
    finally:
        close_db(db)

def buscar_atividades_por_tag_offline(tag: str):
    """Busca as atividades no banco usando a função do arquivo storage.py"""
    if tag not in TAGS_SISTEMA:
        return []
        
    # Puxa a lista do banco
    atividades = get_offline_activity_list_by_tag(tag)
    
    # Se a função do storage.py retornar None (vazio), devolvemos uma lista vazia
    if not atividades:
        return []
        
    return atividades

def listar_atividades_offline():
    """Mantida conforme alinhado durante reunião do grupo."""
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute("""
            SELECT a.id, a.name, a.description, a.tag, a.difficulty, c.instruction 
            FROM activity_list a
            JOIN activity_content c ON a.id = c.activity_id
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar atividades: {e}")
        return []
    finally:
        close_db(db)