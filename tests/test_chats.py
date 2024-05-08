
from fastapi.testclient import TestClient

from backend.main import app
from backend import database as db


def test_get_all_chats():
    client = TestClient(app)
    response = client.get("/chats")
    assert response.status_code == 200

    meta = response.json()["meta"]
    chats = response.json()["chats"]
    assert meta["count"] == len(chats)
    assert chats == sorted(chats, key=lambda chat: chat["name"])


def test_get_valid_id():
    chat_id = "6215e6864e884132baa01f7f972400e2"
    client = TestClient(app)
    response = client.get(f"/chats/{chat_id}")
    data = response.json()
    assert response.status_code == 200
    print(data)
    assert "id" in data["chat"]
    assert chat_id == data["chat"]["id"]
    assert "skynet" == data["chat"]["name"]


def test_get_chat_invalid_id():
    chat_id = "abcdefghijklmnopqrstrv1234567890"
    client = TestClient(app)
    response = client.get(f"/chats/{chat_id}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id,
        },
    }


def test_update_chat_name():
    chat_id = "6215e6864e884132baa01f7f972400e2"
    update_params = {"name": "testTestTest"}
    expected_chat = {
        "chat": {
            "id": "6215e6864e884132baa01f7f972400e2",
            "name": update_params["name"],
            "user_ids": [
                "sarah",
                "terminator"
            ],
            "owner_id": "sarah",
            "created_at": "2023-07-08T18:46:47"
        }
    }
    client = TestClient(app)
    response = client.put(f"/chats/{chat_id}", json=update_params)
    assert response.status_code == 200
    assert response.json() == expected_chat

    response = client.get(f"/chats/{chat_id}")
    assert response.status_code == 200
    assert response.json() == expected_chat


def test_update_invalid_chat_name():
    client = TestClient(app)
    chat_id = "213141413420932"
    update_params = {"name": "chatchat"}
    response = client.put(f"/chats/{chat_id}", json=update_params)
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id,
        },
    }


def test_delete_chat():
    chat_id = "6215e6864e884132baa01f7f972400e2"
    client = TestClient(app)
    response = client.delete(f"/chats/{chat_id}")
    assert response.status_code == 204
    assert response.content == b""

    response = client.get(f"/chats/{chat_id}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id,
        },
    }


def test_delete_invalid():
    chat_id = "2313123sda"
    client = TestClient(app)
    response = client.delete(f"/chats/{chat_id}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id,
        },
    }


def test_get_chat_messages():
    client = TestClient(app)
    chat_id = "660c7a6bc1324e4488cafabc59529c93"

    response = client.get(f"/chats/{chat_id}/messages")
    assert response.status_code == 200
    assert 19 == response.json()["meta"]["count"]


def test_get_chat_messages_invalid():
    client = TestClient(app)
    chat_id = "dsasd312123234dsad"
    response = client.get(f"/chats/{chat_id}/messages")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id,
        },
    }


def test_get_chat_users():
    client = TestClient(app)
    chat_id = "660c7a6bc1324e4488cafabc59529c93"

    response = client.get(f"/chats/{chat_id}/users")
    assert response.status_code == 200
    assert any(
        user['id'] == 'reese' and 'sarah' for user in response.json()['users'])


def test_get_chat_users_invalid():
    client = TestClient(app)
    chat_id = "wdasdw2123"

    response = client.get(f"/chats/{chat_id}/users")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id,
        },
    }
