"""
Tests for artist model.
"""

import pytest


def test_get_artists_no_records(client):
    res = client.get("api/artists")
    expected_result = {
            "success": True,
            "data": [],
            "number_of_records": 0,
            "pagination": {
                "total_pages": 0,
                "total_records": 0,
                "current_page": "/api/artists?page=1"
        }
    }
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"
    assert res.get_json() == expected_result


def test_get_artists(client, sample_data):
    res = client.get("api/artists")
    res_data = res.get_json()
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"
    assert res_data["success"] == True
    assert res_data["number_of_records"] == 5
    assert len(res_data["data"]) == 5
    assert res_data["pagination"] == {
        "total_pages": 2,
        "total_records": 7,
        "current_page": "/api/artists?page=1",
        "next_page": "/api/artists?page=2",
    }


def test_get_artists_with_params(client, sample_data):
    res = client.get("api/artists?fields=name&sort=-id&page=2&limit=2")
    res_data = res.get_json()
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"
    assert res_data["success"] == True
    assert res_data["number_of_records"] == 2
    assert len(res_data["data"]) == 2
    assert res_data["pagination"] == {
        "total_pages": 4,
        "total_records": 7,
        "current_page": "/api/artists?page=2&fields=name&sort=-id&limit=2",
        "next_page": "/api/artists?page=3&fields=name&sort=-id&limit=2",
        "previous_page": "/api/artists?page=1&fields=name&sort=-id&limit=2"
    }
    assert res_data["data"] == [
        {
            "name": "PeeRZet"
        },
        {
            "name": "Oxon"
        }
    ]


def test_get_single_autor(client, sample_data):
    res = client.get("/api/artists/3")
    res_data = res.get_json()
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"
    assert res_data["success"] == True
    assert res_data["data"]["name"] == "Eripe"
    assert res_data["data"]["label"] == "Patokalipsa"
    assert len(res_data["data"]["albums"]) == 2


def test_get_single_autor_not_found(client):
    res = client.get("/api/artists/53")
    res_data = res.get_json()
    assert res.status_code == 404
    assert res.headers["Content-Type"] == "application/json"
    assert res_data["success"] == False
    assert "data" not in res_data


def test_create_artist(client, token, artist):
    res = client.post("api/artists",
                      json=artist,
                      headers={
                          "Authorization": f"Bearer {token}"
                      }
                      )
    res_data = res.get_json()
    expected_result = {
        "success": True,
        "data": {
            **artist,
            "id": 1,
            "albums": []
        }
    }
    assert res.status_code == 201
    assert res.headers["Content-Type"] == "application/json"
    assert res_data == expected_result


@pytest.mark.parametrize(
    "data, missing_field",
    [
        ({"name": "Quebonafide", "label": "QueQuality"}, "birth_date"),
        ({"label": "test", "birth_date": "07-07-1991"}, "name"),
        ({"name": "Quebonafide", "birth_date": "07-07-1991"}, "label"),
    ]
)
def test_create_artist_invalid_data(client, token, data, missing_field):
    res = client.post("api/artists",
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


def test_create_artist_invalid_content_type(client, token, artist):
    res = client.post("api/artists",
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
    res = client.post("api/artists",
                      json=artist,
                      )
    res_data = res.get_json()
    assert res.status_code == 401
    assert res.headers["Content-Type"] == "application/json"
    assert res_data["success"] is False
    assert "data" not in res_data


def test_update_artist(client, artist, token, sample_data):
    updated_data = {
        "name": "Flojd",
        "birth_date": "21-03-1990",
        "label": "DNB"
    }
    res = client.put("api/artists/1",
                       json=updated_data,
                       headers={
                           "Authorization": f"Bearer {token}"
                       })
    res_data = res.get_json()
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"

    for field, value in updated_data.items():
        assert res_data["data"][field] == value


def test_update_artist_missing_data(client, artist, token, sample_data):
    updated_data = {
        "name": "Flojd",
        "birth_date": "21-03-1990",
    }
    res = client.put("api/artists/1",
                       json=updated_data,
                       headers={
                           "Authorization": f"Bearer {token}"
                       })
    res_data = res.get_json()
    assert res.status_code == 400
    assert res.headers["Content-Type"] == "application/json"
    assert "data" not in res_data

    get_res = client.get("api/artists/1")
    get_res_data = get_res.get_json()["data"]
    assert get_res_data["name"] == "VNM"
    assert get_res_data["label"] == "DNB"
    assert get_res_data["birth_date"] == "25-01-1984"


def test_delete_artist(client, artist, token, sample_data):
    delete_res = client.delete("api/artists/1",
                               headers={
                                   "Authorization": f"Bearer {token}"
                               })
    assert delete_res.status_code == 200
    get_res = client.get("api/artists/1")
    assert get_res.status_code == 404