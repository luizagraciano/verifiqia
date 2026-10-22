import sqlite3


from pathlib import Path

DB_NAME = Path(__file__).resolve().parents[2] / "data" / "database.sqlite"


def get_activity(activity_id):
    """
    Busca uma atividade pelo ID e retorna seus dados,
    incluindo instruções, respostas e recursos.
    """

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.description,
                a.tag,
                a.difficulty,
                a.created_at,
                c.id AS content_id,
                c.instruction,
                c.answer,
                c.resources
            FROM activity_list AS a
            LEFT JOIN activity_content AS c
                ON a.id = c.activity_id
            WHERE a.id = ?
        """, (activity_id,))

        rows = cursor.fetchall()

        if not rows:
            return None

        activity = dict(rows[0])
        activity["contents"] = []

        for row in rows:
            if row["content_id"] is not None:
                activity["contents"].append({
                    "id": row["content_id"],
                    "instruction": row["instruction"],
                    "answer": row["answer"],
                    "resources": row["resources"]
                })

        return activity

    finally:
        conn.close()


def edit_activity(
    activity_id,
    name,
    description,
    tag,
    difficulty,
    instruction,
    answer,
    resources
):
    """
    Edita uma atividade existente.
    Retorna uma mensagem de sucesso ou de erro.
    """

    # Valida os campos obrigatórios antes de salvar.
    fields = {
        "Título": name,
        "Descrição": description,
        "Tema": tag,
        "Dificuldade": difficulty,
        "Instruções": instruction,
        "Respostas": answer,
        "Recursos/orientações": resources
    }

    for field_name, value in fields.items():
        if not isinstance(value, str) or not value.strip():
            return {
                "success": False,
                "message": f"O campo {field_name} é obrigatório."
            }

    conn = sqlite3.connect(DB_NAME)

    try:
        cursor = conn.cursor()

        # Confirma que a atividade existe.
        cursor.execute("""
            SELECT id
            FROM activity_list
            WHERE id = ?
        """, (activity_id,))

        if cursor.fetchone() is None:
            return {
                "success": False,
                "message": "Atividade não encontrada."
            }

        # Atualiza as informações principais.
        cursor.execute("""
            UPDATE activity_list
            SET name = ?,
                description = ?,
                tag = ?,
                difficulty = ?
            WHERE id = ?
        """, (
            name.strip(),
            description.strip(),
            tag.strip(),
            difficulty.strip(),
            activity_id
        ))

        # Verifica se já existe conteúdo para a atividade.
        cursor.execute("""
            SELECT id
            FROM activity_content
            WHERE activity_id = ?
            LIMIT 1
        """, (activity_id,))

        content = cursor.fetchone()

        if content:
            # Atualiza o conteúdo existente.
            cursor.execute("""
                UPDATE activity_content
                SET instruction = ?,
                    answer = ?,
                    resources = ?
                WHERE activity_id = ?
            """, (
                instruction.strip(),
                answer.strip(),
                resources.strip(),
                activity_id
            ))
        else:
            # Cria o conteúdo caso ainda não exista.
            cursor.execute("""
                INSERT INTO activity_content (
                    activity_id,
                    instruction,
                    answer,
                    resources
                )
                VALUES (?, ?, ?, ?)
            """, (
                activity_id,
                instruction.strip(),
                answer.strip(),
                resources.strip()
            ))

        # Confirma as alterações no banco.
        conn.commit()

        return {
            "success": True,
            "message": "Atividade atualizada com sucesso."
        }

    except sqlite3.Error:
        conn.rollback()

        return {
            "success": False,
            "message": "Erro ao atualizar a atividade."
        }

    finally:
        conn.close()
