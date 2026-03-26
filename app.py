from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

# In-memory datasets (intentionally empty at startup).
songs = [
    {"id": 1, "title": "Ocean Eyes", "artist_id": 1},
    {"id": 2, "title": "Blinding Lights", "artist_id": 2},
    {"id": 3, "title": "Levitating", "artist_id": 3},
]
artists = [
    {"id": 1, "name": "Billie Eilish"},
    {"id": 2, "name": "The Weeknd"},
    {"id": 3, "name": "Dua Lipa"},
]


def _find_song(song_id):
    """Find one song in memory by its numeric ID."""
    return next((song for song in songs if song["id"] == song_id), None)


def _find_artist(artist_id):
    """Find one artist in memory by its numeric ID."""
    return next((artist for artist in artists if artist["id"] == artist_id), None)


def _enrich_song_with_artist(song):
    """Add artist name to song object."""
    artist = _find_artist(song["artist_id"])
    return {
        **song,
        "artist_name": artist["name"] if artist else "Unknown"
    }


# Get all songs endpoint
@app.route("/songs", methods=["GET"])
def get_all_songs():
    """Return all songs currently stored in memory."""
    enriched_songs = [_enrich_song_with_artist(song) for song in songs]
    return jsonify({"songs": enriched_songs, "count": len(enriched_songs)})


# Get song by ID endpoint
@app.route("/songs/<int:song_id>", methods=["GET"])
def get_song_by_id(song_id):
    """Return a single song by ID, or 404 when it does not exist."""
    song = _find_song(song_id)
    if song is None:
        return jsonify({"error": "Song not found"}), 404
    return jsonify(_enrich_song_with_artist(song))


# Create song endpoint
@app.route("/songs", methods=["POST"])
def create_song():
    """Create a new song from JSON input and assign the next available ID."""
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()
    artist_id = data.get("artist_id")

    if not title:
        return jsonify({"error": "Field 'title' is required"}), 400
    if artist_id is None:
        return jsonify({"error": "Field 'artist_id' is required"}), 400

    new_id = max((song["id"] for song in songs), default=0) + 1
    new_song = {
        "id": new_id,
        "title": title,
        "artist_id": artist_id,
    }
    songs.append(new_song)
    return jsonify(new_song), 201


# Get all artists endpoint
@app.route("/artists", methods=["GET"])
def get_all_artists():
    """Return all artists currently stored in memory."""
    return jsonify({"artists": artists, "count": len(artists)})


# Create artist endpoint
@app.route("/artists", methods=["POST"])
def create_artist():
    """Create a new artist from JSON input and assign the next available ID."""
    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()

    if not name:
        return jsonify({"error": "Field 'name' is required"}), 400

    new_id = max((artist["id"] for artist in artists), default=0) + 1
    new_artist = {
        "id": new_id,
        "name": name,
    }
    artists.append(new_artist)
    return jsonify(new_artist), 201


# Search songs by keyword endpoint
@app.route("/songs/search", methods=["GET"])
def search_songs_by_keyword():
    """Search songs by a keyword in the title (case-insensitive)."""
    keyword = request.args.get("keyword", "").strip().lower()
    if not keyword:
        return jsonify({"error": "Query parameter 'keyword' is required"}), 400

    matched = [song for song in songs if keyword in song.get("title", "").lower()]
    return jsonify({"songs": matched, "count": len(matched)})


# Serve home page
@app.route("/", methods=["GET"])
def home_page():
    """Serve the landing page for the music app UI."""
    return send_from_directory("template", "index.html")


# Serve songs page
@app.route("/ui/songs", methods=["GET"])
def songs_page():
    """Serve the songs page with list/create/get-by-id controls."""
    return send_from_directory("template", "songs.html")


# Serve artists page
@app.route("/ui/artists", methods=["GET"])
def artists_page():
    """Serve the artists/search page."""
    return send_from_directory("template", "artists.html")


# Serve UI assets (CSS, JS)
@app.route("/assets/<filename>", methods=["GET"])
def ui_assets(filename):
    """Serve CSS/JS assets for the UI pages."""
    return send_from_directory("template", filename)


if __name__ == "__main__":
    app.run(debug=True)