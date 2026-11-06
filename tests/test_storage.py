import pytest
import src.database.storage as storage
from tests.conftest import activity_data, incomplete_activity_data

# Verifica a criação de um usuário e a recuperação dos seus dados.
def test_create_and_get_user(user_data):
    storage.create_user(**user_data)

    user = storage.get_user("testuser@example.com")

    assert user is not None
    assert user["username"] == user_data["username"]
    assert user["cpf"] == user_data["cpf"]
    assert user["email"] == user_data["email"]
    assert user["password"] != user_data["password"]


# Verifica que a busca de um usuário inexistente retorna vazio.
def test_get_nonexistent_user():
    user = storage.get_user("nonexistent@example.com")

    assert user is None


# Verifica o comportamento da busca quando o e-mail não é informado.
def test_get_user_with_empty_email():
    user = storage.get_user(None)

    assert user is None


# Verifica que não é possível criar dois usuários com os mesmos dados únicos.
def test_create_user_with_existing_email(user_data):
    storage.create_user(**user_data)

    with pytest.raises(ValueError) as error:
        storage.create_user(**user_data)

    assert "Erro ao criar usuário" in str(error.value)

# Verifica que campos obrigatórios ausentes impedem a criação de um usuário.
def test_create_user_with_empty_fields(invalid_user_data):
    with pytest.raises(ValueError) as error:
        storage.create_user(**invalid_user_data)

    assert "Erro ao criar usuário" in str(error.value)


# Verifica a atualização da senha sem alterar os demais dados do usuário.
def test_update_user(user_data):
    storage.create_user(**user_data)
    old_user = storage.get_user("testuser@example.com")

    storage.update_user("testuser@example.com", "newpassword")
    updated_user = storage.get_user("testuser@example.com")

    assert updated_user is not None
    assert updated_user["username"] == user_data["username"]
    assert updated_user["cpf"] == user_data["cpf"]
    assert updated_user["email"] == user_data["email"]
    assert updated_user["password"] != "newpassword"
    assert updated_user["password"] != old_user["password"]


# Verifica que uma senha ausente gera erro durante a atualização.
def test_update_user_with_empty_password():
    with pytest.raises(ValueError) as error:
        storage.update_user("nonexistent@example.com", None)

    assert "Erro ao atualizar usuário" in str(error.value)


# Verifica a criação de uma atividade e a recuperação do seu conteúdo.
def test_create_and_get_activity(activity_data):
    storage.create_activity(**activity_data)
    activity_list = storage.get_activity_list()
    activity_id = activity_list[0]["id"]
    activity_content = storage.get_activity_content(activity_id)

    assert len(activity_list) == 1
    assert activity_list[0]["name"] == activity_data["name"]
    assert activity_list[0]["description"] == activity_data["description"]
    assert activity_list[0]["tag"] == activity_data["tag"]
    assert activity_list[0]["difficulty"] == activity_data["difficulty"]
    assert activity_list[0]["created_at"] is not None

    assert activity_content["activity_id"] == activity_id
    assert activity_content["instruction"] == activity_data["instruction"]
    assert activity_content["answer"] == activity_data["answer"]
    assert activity_content["resources"] == activity_data["resources"]


# Verifica que campos obrigatórios ausentes impedem a criação de uma atividade.
def test_create_activity_with_missing_fields(incomplete_activity_data):
    with pytest.raises(ValueError) as error:
        storage.create_activity(**incomplete_activity_data)

    assert "Erro ao criar atividade" in str(error.value)


# Verifica que a listagem retorna vazio quando não há atividades cadastradas.
def test_get_empty_activity_list():
    activity_list = storage.get_activity_list()

    assert activity_list is None


# Verifica a filtragem de atividades por tag.
def test_get_activity_list_by_tag(activity_data, activity_data2, activity_data3):
    storage.create_activity(**activity_data)
    storage.create_activity(**activity_data2)
    storage.create_activity(**activity_data3)

    activities_tag1 = storage.get_activity_list_by_tag("tag1")
    activities_tag2 = storage.get_activity_list_by_tag("tag2")

    assert len(activities_tag1) == 1
    assert activities_tag1[0]["tag"] == activity_data["tag"]

    assert len(activities_tag2) == 2
    assert activities_tag2[0]["tag"] == activity_data2["tag"]
    assert activities_tag2[1]["tag"] == activity_data3["tag"]
    assert activities_tag2[0]["tag"] == activities_tag2[1]["tag"]
    assert activities_tag2[0]["tag"] != activities_tag1[0]["tag"]


# Verifica que uma tag inexistente não retorna atividades.
def test_get_activity_list_by_nonexistent_tag():
    activity_list = storage.get_activity_list_by_tag("nonexistent_tag")

    assert activity_list is None


# Verifica a busca de uma atividade pelo identificador e seu conteúdo.
def test_get_activity_by_id(activity_data):
    storage.create_activity(**activity_data)
    activity_list = storage.get_activity_list()
    activity_id = activity_list[0]["id"]

    activity_content = storage.get_activity_content(activity_id)

    assert activity_list is not None
    assert len(activity_list) == 1
    assert activity_list[0]["id"] == activity_id
    assert activity_list[0]["name"] == activity_data["name"]
    assert activity_list[0]["description"] == activity_data["description"]
    assert activity_list[0]["tag"] == activity_data["tag"]
    assert activity_list[0]["difficulty"] == activity_data["difficulty"]
    assert activity_content is not None
    assert activity_content["id"] == activity_id
    assert activity_content["instruction"] == activity_data["instruction"]
    assert activity_content["answer"] == activity_data["answer"]
    assert activity_content["resources"] == activity_data["resources"]


# Verifica a atualização completa dos dados de uma atividade.
def test_update_activity(activity_data,updated_activity_data):
    storage.create_activity(**activity_data)
    activity_list = storage.get_activity_list()
    activity_id = activity_list[0]["id"]

    storage.update_activity(activity_id, **updated_activity_data)
    updated_activity_list = storage.get_activity_list()
    updated_activity_content = storage.get_activity_content(activity_id)

    assert updated_activity_list[0]["name"] == updated_activity_data["name"]
    assert updated_activity_list[0]["description"] == updated_activity_data["description"]
    assert updated_activity_list[0]["tag"] == updated_activity_data["tag"]
    assert updated_activity_list[0]["difficulty"] == updated_activity_data["difficulty"]

    assert updated_activity_content["instruction"] == updated_activity_data["instruction"]
    assert updated_activity_content["answer"] == updated_activity_data["answer"]
    assert updated_activity_content["resources"] == updated_activity_data["resources"]


# Verifica a atualização parcial preservando os campos não informados.
def test_partial_update_activity(activity_data):
    storage.create_activity(**activity_data)
    activity_list = storage.get_activity_list()
    activity_id = activity_list[0]["id"]

    storage.update_activity(activity_id, name="Partially Updated Activity", description=None, tag=None, difficulty=None, instruction=None, answer=None, resources=None)
    updated_activity_list = storage.get_activity_list()
    updated_activity_content = storage.get_activity_content(activity_id)

    assert updated_activity_list[0]["name"] == "Partially Updated Activity"
    assert updated_activity_list[0]["description"] == activity_data["description"]
    assert updated_activity_list[0]["tag"] == activity_data["tag"]
    assert updated_activity_list[0]["difficulty"] == activity_data["difficulty"]

    assert updated_activity_content["instruction"] == activity_data["instruction"]
    assert updated_activity_content["answer"] == activity_data["answer"]
    assert updated_activity_content["resources"] == activity_data["resources"]


# Verifica a remoção de uma atividade da listagem persistida.
def test_delete_activity(activity_data):
    storage.create_activity(**activity_data)
    activity_list = storage.get_activity_list()
    activity_id = activity_list[0]["id"]

    storage.delete_activity(activity_id)
    deleted_activity_list = storage.get_activity_list()

    assert deleted_activity_list is None
