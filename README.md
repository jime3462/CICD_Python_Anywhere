# WaveRoom Music API & UI

A simple Flask-based music API and web UI for managing songs and artists. Features include:

- List, create, and search songs
- List and create artists
- Header search bar on all UI pages
- Dedicated search results page with table output
- Modern, responsive UI (HTML/CSS/JS)
- In-memory data storage (no database required)

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the app:**
   ```bash
   python app.py
   ```
3. **Open in browser:**
   - Home: [http://localhost:5000/](http://localhost:5000/)
   - Songs UI: [http://localhost:5000/ui/songs](http://localhost:5000/ui/songs)
   - Artists UI: [http://localhost:5000/ui/artists](http://localhost:5000/ui/artists)
   - Search Results UI: [http://localhost:5000/ui/search-results](http://localhost:5000/ui/search-results)

## API Endpoints

- `GET /songs` — list all songs
- `GET /songs/<id>` — get one song by numeric ID
- `POST /songs` — create song (`title`, `artist_id` required)
- `GET /songs/search?keyword=<text>` — search songs by title keyword
- `GET /artists` — list all artists
- `POST /artists` — create artist (`name` required)
- `POST /gitpull` — signed webhook endpoint for deployment

## UI Pages

- `/` — home page with auto-loaded songs table
- `/ui/songs` — song by ID + create song tools
- `/ui/artists` — list/create artist tools
- `/ui/search-results` — table of search matches

Search behavior:
- The search form appears in the header on every page.
- Submitting search navigates to `/ui/search-results?keyword=<term>`.

## Project Structure

- `app.py` — Flask backend (API & static file serving)
- `requirements.txt` — Python dependencies
- `template/` — Frontend HTML, CSS, JS
   - `index.html`, `songs.html`, `artists.html`, `search-results.html` — UI pages
    - `style.css` — Styles
    - `app-ui.js` — UI logic


## Notes
- Data is not persistent; restarting the app resets all songs/artists.
- For development only. Not production-ready.
- python-test yml pass.
- deploy yml hasn't passed.
- Github Repo: https://github.com/jime3462/CICD_Python_Anywhere
- Python App: https://jime3462.pythonanywhere.com/

---

© 2026 WaveRoom Project
