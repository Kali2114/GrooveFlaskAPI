"""
Config for Pytest.
"""


import pytest

from app import create_app, db
from app.commands.db_manage_commands import add_data


@pytest.fixture
def app():
    app = create_app("testing")

    with app.app_context():
        db.create_all()

    yield app

    app.config["DB_FILE_PATH"].unlink(missing_ok=True)


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture
def user(client):
    user = {
        "username": "Test",
        "password": "Testpass",
        "email": "example@test.com"
    }
    client.post("api/auth/register", json=user)
    return user


@pytest.fixture
def token(client, user):
    res = client.post("api/auth/login", json={
        "username": user["username"],
        "password": user["password"],
    })
    return res.get_json()["token"]


@pytest.fixture
def sample_data(app):
    runner = app.test_cli_runner()
    runner.invoke(add_data)


@pytest.fixture
def artist():
    return {
        "name": "Oki",
        "label": "2020",
        "birth_date": "10-08-1998"
    }


@pytest.fixture
def album():
    return {
        "title": "Test Album",
        "number_of_songs": 10,
        "description": "Test description",
        "release_year": 2020,
    }