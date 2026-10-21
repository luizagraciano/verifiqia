import pytest
import src.database.storage as storage
from tests.conftest import activity_data, incomplete_activity_data

def test_create_and_get_user(user_data):
    storage.create_user(**user_data)

    user = storage.get_user("testuser@example.com")

    assert user is not None
    assert user[1] == user_data["username"]
    assert user[2] == user_data["cpf"]
    assert user[3] == user_data["email"]
    assert user[4] != user_data["password"]


def test_get_nonexistent_user():
    with pytest.raises(ValueError) as error:
        storage.get_user("nonexistent@example.com")

    assert "Usuário ou senha incorreta." in str(error.value)


def test_get_user_with_empty_email():
    with pytest.raises(ValueError) as error:
        storage.get_user(None)

    assert "Erro ao buscar usuário" in str(error.value)


def test_create_user_with_existing_email(user_data):
    storage.create_user(**user_data)

    with pytest.raises(ValueError) as error:
        storage.create_user(**user_data)

    assert "Erro ao criar usuário" in str(error.value)

def test_create_user_with_empty_fields(invalid_user_data):
    with pytest.raises(ValueError) as error:
        storage.create_user(**invalid_user_data)

    assert "Erro ao criar usuário" in str(error.value)


def test_update_user(user_data):
    storage.create_user(**user_data)
    old_user = storage.get_user("testuser@example.com")

    storage.update_user("testuser@example.com", "newpassword")
    updated_user = storage.get_user("testuser@example.com")

    assert updated_user is not None
    assert updated_user[1] == user_data["username"]
    assert updated_user[2] == user_data["cpf"]
    assert updated_user[3] == user_data["email"]
    assert updated_user[4] != "newpassword"
    assert updated_user[4] != old_user[4]


def test_update_user_with_empty_password():
    with pytest.raises(ValueError) as error:
        storage.update_user("nonexistent@example.com", None)

    assert "Erro ao atualizar usuário" in str(error.value)


def test_create_and_get_activity(activity_data):
    storage.create_activity(**activity_data)
    activity_list = storage.get_activity_list()
    activity_id = activity_list[0][0]
    activity_content = storage.get_activity_content(activity_id)

    assert len(activity_list) == 1
    assert activity_list[0][1] == activity_data["name"]
    assert activity_list[0][2] == activity_data["description"]
    assert activity_list[0][3] == activity_data["tag"]
    assert activity_list[0][4] == activity_data["difficulty"]
    assert activity_list[0][5] is not None

    assert activity_content[1] == activity_id
    assert activity_content[2] == activity_data["instruction"]
    assert activity_content[3] == activity_data["answer"]
    assert activity_content[4] == activity_data["resources"]


def test_create_activity_with_missing_fields(incomplete_activity_data):
    with pytest.raises(ValueError) as error:
        storage.create_activity(**incomplete_activity_data)
    
    assert "Erro ao criar atividade" in str(error.value)


def test_get_empty_activity_list():
    activity_list = storage.get_activity_list()
    assert len(activity_list) == 0


def test_get_activity_list_by_tag(activity_data, activity_data2, activity_data3):
    storage.create_activity(**activity_data)
    storage.create_activity(**activity_data2)
    storage.create_activity(**activity_data3)

    activities_tag1 = storage.get_activity_list_by_tag("tag1")
    activities_tag2 = storage.get_activity_list_by_tag("tag2")

    assert len(activities_tag1) == 1
    assert activities_tag1[0][3] == activity_data["tag"]

    assert len(activities_tag2) == 2
    assert activities_tag2[0][3] == activity_data2["tag"]
    assert activities_tag2[1][3] == activity_data3["tag"]
    assert activities_tag2[0][3] == activities_tag2[1][3]
    assert activities_tag2[0][3] != activities_tag1[0][3]


def test_get_activity_list_by_nonexistent_tag():
    activity_list = storage.get_activity_list_by_tag("nonexistent_tag")
    assert len(activity_list) == 0


def test_update_activity(activity_data,updated_activity_data):
    storage.create_activity(**activity_data)
    activity_list = storage.get_activity_list()
    activity_id = activity_list[0][0]

    storage.update_activity(activity_id, **updated_activity_data)
    updated_activity_list = storage.get_activity_list()
    updated_activity_content = storage.get_activity_content(activity_id)

    assert updated_activity_list[0][1] == updated_activity_data["name"]
    assert updated_activity_list[0][2] == updated_activity_data["description"]
    assert updated_activity_list[0][3] == updated_activity_data["tag"]
    assert updated_activity_list[0][4] == updated_activity_data["difficulty"]

    assert updated_activity_content[2] == updated_activity_data["instruction"]
    assert updated_activity_content[3] == updated_activity_data["answer"]
    assert updated_activity_content[4] == updated_activity_data["resources"]


def test_partial_update_activity(activity_data):
    storage.create_activity(**activity_data)
    activity_list = storage.get_activity_list()
    activity_id = activity_list[0][0]

    storage.update_activity(activity_id, name="Partially Updated Activity", description=None, tag=None, difficulty=None, instruction=None, answer=None, resources=None)
    updated_activity_list = storage.get_activity_list()
    updated_activity_content = storage.get_activity_content(activity_id)

    assert updated_activity_list[0][1] == "Partially Updated Activity"
    assert updated_activity_list[0][2] == activity_data["description"]
    assert updated_activity_list[0][3] == activity_data["tag"]
    assert updated_activity_list[0][4] == activity_data["difficulty"]

    assert updated_activity_content[2] == activity_data["instruction"]
    assert updated_activity_content[3] == activity_data["answer"]
    assert updated_activity_content[4] == activity_data["resources"]


def test_delete_activity(activity_data):
    storage.create_activity(**activity_data)
    activity_list = storage.get_activity_list()
    activity_id = activity_list[0][0]

    storage.delete_activity(activity_id)
    deleted_activity_list = storage.get_activity_list()

    assert len(deleted_activity_list) == 0