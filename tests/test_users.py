from datetime import datetime

from fastapi.testclient import TestClient
from backend.database import DB
from backend.auth import build_access_token



from backend.main import app
import sys


# def test_get_all_users():
#     client = TestClient(app)
#     response = client.get("/users")
#     assert response.status_code == 200

#     meta = response.json()["meta"]
#     users = response.json()["users"]
#     assert meta["count"] == len(users)
#     assert users == sorted(users, key=lambda user: user["id"])
def test_get_all_users(client, user_fixture):
    db_users = [user_fixture(username=username) for username in ["juniper"]]
    response = client.get("/users")
    assert response.status_code == 200

    meta = response.json()["meta"]
    users = response.json()["users"]

    assert meta["count"] == len(db_users)
    assert {user["username"] for user in users} == {
        db_user.username for db_user in db_users
    }


# def test_create_user():
#     create_params = {
#         "id": "karl barx",

#     }
#     client = TestClient(app)
#     response = client.post("/users", json=create_params)

#     assert response.status_code == 200
#     data = response.json()
#     assert "user" in data
#     user = data["user"]
#     for key, value in create_params.items():
#         assert user[key] == value

#     response = client.get(f"/users/{user['id']}")
#     assert response.status_code == 200
#     data = response.json()
#     assert "user" in data
#     user = data["user"]
#     for key, value in create_params.items():
#         assert user[key] == value


# def test_create_duplicate_id():
#     client = TestClient(app)
#     create_params = {
#         "id": "bishop",
#     }

#     response = client.post("/users", json=create_params)
#     assert response.status_code == 422
#     assert response.json() == {
#         "detail": {
#             "type": "duplicate_entity",
#             "entity_name": "User",
#             "entity_id": create_params["id"],
#         },
#     }


# def test_valid_id():
#     client = TestClient(app)
#     user_id = "bishop"
#     response = client.get(f"/users/{user_id}")
#     assert response.status_code == 200
#     data = response.json()
#     assert "user" in data
#     assert user_id == data["user"]["id"]


# def test_get_user_invalid_id():
#     user_id = "abcdefghijklmnopqrstrv1234567890"
#     client = TestClient(app)
#     response = client.get(f"/users/{user_id}")
#     assert response.status_code == 404
#     assert response.json() == {
#         "detail": {
#             "type": "entity_not_found",
#             "entity_name": "User",
#             "entity_id": user_id,
#         },
#     }


def test_get_users_chats():
    client = TestClient(app)
    user_id = "7"
    response = client.get(f"/users/{user_id}/chats")

    assert response.status_code == 200

    data = response.json()
    print(response.json())


# def test_get_invalid_users_chats():
#     client = TestClient(app)
#     user_id = "johnny"
#     response = client.get(f"/users/{user_id}/chats")

#     assert response.status_code == 404

#     assert response.json() == {
#         "detail": {
#             "type": "entity_not_found",
#             "entity_name": "User",
#             "entity_id": user_id,
#         },
#     }
