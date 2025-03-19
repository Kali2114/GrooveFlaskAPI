"""
Tests for authentication.
"""

import pytest


def test_registration(client):
    res = client.post("api/auth/register",
                      json={
                            "username": "test",
                            "password": "Testpass123",
                            "email": "test@example.com"
                      })
    res_data = res.get_json()

    assert res.status_code == 201
    assert res.headers['Content-Type'] == "application/json"
    assert res_data["success"] is True
    assert res_data["token"]


@pytest.mark.parametrize(
    "data, missing_field",
    [
        ({"username": "test", "password": "Testpass"}, "email"),
        ({"username": "test", "email": "test@example.com"}, "password"),
        ({"password": "Testpass", "email": "test@example.com"}, "username"),
    ]
)
def test_registration_invalid_data(client, data, missing_field):
    res = client.post("api/auth/register",
                      json=data
                      )
    res_data = res.get_json()

    assert res.status_code == 400
    assert res.headers['Content-Type'] == "application/json"
    assert res_data["success"] is False
    assert "token" not in res_data
    assert missing_field in res_data["message"]


def test_registration_invalid_content_type(client):
    res = client.post("api/auth/register",
                      data={
                          "username": "test",
                          "password": "Testpass123",
                          "email": "test@example.com"
                      })
    res_data = res.get_json()

    assert res.status_code == 415
    assert res.headers["Content-Type"] == "application/json"
    assert res_data["success"] is False
    assert "token" not in res_data


def test_registration_already_used_username(client, user):
    res = client.post("api/auth/register",
                      json={
                          "username": user["username"],
                          "password": "Testpass123",
                          "email": "test1@example.com"
                      })
    res_data = res.get_json()

    assert res.status_code == 409
    assert res.headers["Content-Type"] == "application/json"
    assert res_data["success"] is False
    assert "token" not in res_data


def test_get_current_user(client, user, token):
    res = client.get("api/auth/me",
                     headers={
                         "Authorization": f"Bearer {token}"
                     })
    res_data = res.get_json()
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"
    assert res_data["success"] is True
    assert res_data["data"]["username"] == user["username"]
    assert res_data["data"]["email"] == user["email"]
    assert "id" in res_data["data"]
    assert "creation_date" in res_data["data"]


def test_get_current_user_missing_token(client):
    res = client.get("api/auth/me")
    res_data = res.get_json()
    assert res.status_code == 401
    assert res.headers["Content-Type"] == "application/json"
    assert res_data["success"] is False
    assert "data" not in res_data
