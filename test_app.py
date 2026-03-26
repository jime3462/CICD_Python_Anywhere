import pytest

from app import app, artists, songs


@pytest.fixture
def test_client():
    app.config["TESTING"] = True
    songs.clear()
    artists.clear()
    with app.test_client() as test_client:
        yield test_client
    songs.clear()
    artists.clear()


def test_get_all_songs_returns_empty_list_initially(test_client):
    response = test_client.get("/songs")

    assert response.status_code == 200
    assert response.get_json() == {"songs": [], "count": 0}


def test_get_song_by_id_returns_404_for_missing_song(test_client):
    response = test_client.get("/songs/1")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Song not found"


def test_create_song_success(test_client):
    payload = {"title": "Yellow Submarine", "artist_id": 1}

    response = test_client.post("/songs", json=payload)

    assert response.status_code == 201
    assert response.get_json()["title"] == "Yellow Submarine"
    assert response.get_json()["artist_id"] == 1


def test_create_song_requires_title(test_client):
    response = test_client.post("/songs", json={"artist_id": 1})

    assert response.status_code == 400
    assert response.get_json()["error"] == "Field 'title' is required"


def test_create_song_requires_artist_id(test_client):
    response = test_client.post("/songs", json={"title": "No Artist"})

    assert response.status_code == 400
    assert response.get_json()["error"] == "Field 'artist_id' is required"


def test_get_song_by_id_returns_created_song(test_client):
    create_response = test_client.post("/songs", json={"title": "Numb", "artist_id": 7})
    song_id = create_response.get_json()["id"]

    response = test_client.get(f"/songs/{song_id}")

    assert response.status_code == 200
    assert response.get_json() == {
        "id": song_id,
        "title": "Numb",
        "artist_id": 7,
        "artist_name": "Unknown",
    }


def test_get_all_artists_returns_empty_list_initially(test_client):
    response = test_client.get("/artists")

    assert response.status_code == 200
    assert response.get_json() == {"artists": [], "count": 0}


def test_search_songs_requires_keyword(test_client):
    response = test_client.get("/songs/search")

    assert response.status_code == 400
    assert response.get_json()["error"] == "Query parameter 'keyword' is required"


def test_search_songs_by_keyword_matches_titles_case_insensitive(test_client):
    test_client.post("/songs", json={"title": "Bohemian Rhapsody", "artist_id": 1})
    test_client.post("/songs", json={"title": "Rhapsody in Blue", "artist_id": 2})
    test_client.post("/songs", json={"title": "Imagine", "artist_id": 3})

    response = test_client.get("/songs/search?keyword=RHAP")

    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] == 2
    assert [song["title"] for song in data["songs"]] == [
        "Bohemian Rhapsody",
        "Rhapsody in Blue",
    ]


def test_create_song_with_new_artist(test_client):
    new_song = {"title": "Test Song", "artist_id": 1}
    create_resp = test_client.post("/songs", json=new_song)
    assert create_resp.status_code == 201

    created = create_resp.get_json()
    assert created["title"] == "Test Song"
    assert created["artist_id"] == 1
    assert "id" in created
