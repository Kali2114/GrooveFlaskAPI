"""
Tests for albums model.
"""

import pytest


def test_get_albums(client, sample_data):
    res = client.get("/api/albums")
    res_data = res.get_json()

    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"
    assert res_data["success"] == True
    assert res_data["number_of_records"]
    assert len(res_data["data"]) == 5
    assert res_data["pagination"] == {
        "total_pages": 4,
        "total_records": 18,
        "current_page": "/api/albums?page=1",
        "next_page": "/api/albums?page=2",
    }


def test_get_albums_with_params(client, sample_data):
    res = client.get("api/albums?fields=title&sort=-id&page=2&limit=2")
    res_data = res.get_json()
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"
    assert res_data["success"] == True
    assert res_data["number_of_records"] == 2
    assert len(res_data["data"]) == 2
    assert res_data["pagination"] == {
        "total_pages": 9,
        "total_records": 18,
        "current_page": "/api/albums?page=2&fields=title&sort=-id&limit=2",
        "next_page": "/api/albums?page=3&fields=title&sort=-id&limit=2",
        "previous_page": "/api/albums?page=1&fields=title&sort=-id&limit=2"
    }
    assert res_data["data"] == [
        {
            "title": "Postanawia Umrzec"
        },
        {
            "title": "Refluks"
        }
    ]


def test_get_single_album(client, sample_data):
    res = client.get("/api/albums/2")
    res_data = res.get_json()
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"
    assert res_data["success"] == True
    assert res_data["data"]["description"] == "Third VNM's legal album."
    assert res_data["data"]["number_of_songs"] == 13
    assert res_data["data"]["release_year"] == 2012
    assert res_data["data"]["title"] == "Propejn"


def test_get_single_album_not_found(client, sample_data):
    res = client.get("/api/albums/50")
    res_data = res.get_json()
    assert res.status_code == 404
    assert res.headers["Content-Type"] == "application/json"
    assert res_data["success"] == False
    assert "data" not in res_data


def test_create_album(client, token, sample_data, album):
    album_res = client.post("/api/artist/1/albums",
                            json=album,
                            headers={
                                "Authorization": f"Bearer {token}"
                            })
    created_album = album_res.get_json()
    res = client.get(f"/api/albums/{created_album['data']['id']}")
    res_data = res.get_json()

    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"
    assert res_data["success"] is True
    assert res_data["data"]["title"] == album["title"]
    assert res_data["data"]["number_of_songs"] == album["number_of_songs"]
    assert res_data["data"]["release_year"] == album["release_year"]


@pytest.mark.parametrize(
    "data, missing_field",
    [
        ({"title": "Wielkie Sny", "number_of_songs": 15}, "release_year"),
        ({"number_of_songs": 15, "release_year": 2020}, "title"),
        ({"title": "Wielkie Sny", "release_year": 2020}, "number_of_songs"),
    ]
)
def test_create_album_invalid_data(client, token, data, missing_field):
    res = client.post("/api/artist/1/albums",
                      json=data,
                      headers={
                          "Authorization": f"Bearer {token}"
                      })
    res_data = res.get_json()

    assert res.status_code == 400
    assert res.headers['Content-Type'] == "application/json"
    assert res_data["success"] is False
    assert "data" not in res_data
    assert missing_field in res_data["message"]


def test_create_album_invalid_content_type(client, token, artist):
    res = client.post("/api/artist/1/albums",
                      data=artist,
                      headers={
                          "Authorization": f"Bearer {token}"
                      })
    res_data = res.get_json()
    assert res.status_code == 415
    assert res.headers["Content-Type"] == "application/json"
    assert res_data["success"] is False
    assert "data" not in res_data


def test_create_artist_missing_token(client, artist):
    res = client.post("/api/artist/1/albums",
                      json=artist,
                      )
    res_data = res.get_json()
    assert res.status_code == 401
    assert res.headers["Content-Type"] == "application/json"
    assert res_data["success"] is False
    assert "data" not in res_data


def test_update_album(client, album, token, sample_data):
    updated_data = {
        "description": "Test Desc",
        "number_of_songs": 11,
        "release_year": 1992,
        "title": "Test Title"
    }
    res = client.put("/api/albums/2",
                       json=updated_data,
                       headers={
                           "Authorization": f"Bearer {token}"
                       })
    res_data = res.get_json()
    print(res)
    print(res_data)
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"

    for field, value in updated_data.items():
        assert res_data["data"][field] == value


def test_delete_artist(client, artist, token, sample_data):
    delete_res = client.delete("api/albums/1",
                               headers={
                                   "Authorization": f"Bearer {token}"
                               })
    assert delete_res.status_code == 200
    get_res = client.get("api/albums/1")
    assert get_res.status_code == 404