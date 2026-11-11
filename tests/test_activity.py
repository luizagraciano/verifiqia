import pytest
import src.database.storage as storage
from src.services.activity import get_activity, edit_activity_in_database


def test_get_activity(activity_data):
    storage.create_activity(**activity_data)

    activity_id = storage.get_activity_list()[0]["id"]
    activity = get_activity(activity_id)

    assert activity is not None
    assert activity["name"] == activity_data["name"]
    assert activity["instruction"] == activity_data["instruction"]


def test_get_nonexistent_activity():
    activity = get_activity(999)

    assert activity is None


def test_edit_activity(activity_data, updated_activity_data):
    storage.create_activity(**activity_data)

    activity_id = storage.get_activity_list()[0]["id"]

    result = edit_activity_in_database(activity_id, **updated_activity_data)

    updated_activity = get_activity(activity_id)

    assert updated_activity["name"] == updated_activity_data["name"]
    assert updated_activity["description"] == updated_activity_data["description"]
    assert updated_activity["instruction"] == updated_activity_data["instruction"]


def test_edit_nonexistent_activity(activity_data):
    with pytest.raises(ValueError) as error:
        edit_activity_in_database(999, **activity_data)

    assert str(error.value) == "Atividade não encontrada."
