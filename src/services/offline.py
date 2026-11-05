from src.database.storage import get_db, close_db

def salvar_atividade_offline(name, description, tag, difficulty, instruction, answer, resources):
    """
    Salva uma atividade completa no banco de dados local (biblioteca offline).
    """
    db = get_db()
    if not db:
        print("Erro: não foi possível conectar ao banco de dados.")
        return

    try:
        cursor = db.cursor()
        
        # 1. Salva os dados principais na tabela activity_list
        cursor.execute(
            """
            INSERT INTO activity_list (name, description, tag, difficulty) 
            VALUES (?, ?, ?, ?)
            """,
            (name, description, tag, difficulty)
        )
        
        # Pega o ID da atividade que acabou de ser criada
        activity_id = cursor.lastrowid 
        
        # 2. Salva o conteúdo na tabela activity_content
        cursor.execute(
            """
            INSERT INTO activity_content (activity_id, instruction, answer, resources) 
            VALUES (?, ?, ?, ?)
            """,
            (activity_id, instruction, answer, resources)
        )
        
        db.commit()
        print(f"Sucesso! Atividade '{name}' salva na biblioteca offline.")
        
    except Exception as e:
        print(f"Erro ao salvar atividade offline: {e}")
        db.rollback() # Desfaz a operação se der erro no meio do caminho
    finally:
        close_db(db)

def listar_atividades_offline():
    """
    Busca as atividades salvas localmente juntando as duas tabelas.
    """
    db = get_db()
    try:
        cursor = db.cursor()
        # O JOIN junta os dados da lista com os conteúdos
        cursor.execute("""
            SELECT a.id, a.name, a.description, a.tag, a.difficulty, c.instruction 
            FROM activity_list a
            JOIN activity_content c ON a.id = c.activity_id
        """)
        atividades = cursor.fetchall()
        return atividades
    except Exception as e:
        print(f"Erro ao buscar atividades: {e}")
        return []
    finally:
        close_db(db)