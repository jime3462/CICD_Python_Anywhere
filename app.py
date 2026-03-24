from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory datasets (intentionally empty at startup).
songs = []
artists = []


# Find one song in memory by its numeric ID.
def _find_song(song_id):
    return next((song for song in songs if song["id"] == song_id), None)


# Return all songs currently stored in memory.
@app.route("/songs", methods=["GET"])
def get_all_songs():
    return jsonify({"songs": songs, "count": len(songs)})


# Return a single song by ID, or 404 when it does not exist.
@app.route("/songs/<int:song_id>", methods=["GET"])
def get_song_by_id(song_id):
    song = _find_song(song_id)
    if song is None:
        return jsonify({"error": "Song not found"}), 404
    return jsonify(song)


# Create a new song from JSON input and assign the next available ID.
@app.route("/songs", methods=["POST"])
def create_song():
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


# Return all artists currently stored in memory.
@app.route("/artists", methods=["GET"])
def get_all_artists():
    return jsonify({"artists": artists, "count": len(artists)})


# Search songs by a keyword in the title (case-insensitive).
@app.route("/songs/search", methods=["GET"])
def search_songs_by_keyword():
    keyword = request.args.get("keyword", "").strip().lower()
    if not keyword:
        return jsonify({"error": "Query parameter 'keyword' is required"}), 400

    matched = [song for song in songs if keyword in song.get("title", "").lower()]
    return jsonify({"songs": matched, "count": len(matched)})


if __name__ == "__main__":
    app.run(debug=True)