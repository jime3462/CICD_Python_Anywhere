# WaveRoom Music API & UI

A simple Flask-based music API and web UI for managing songs and artists. Features include:

- List, create, and search songs
- List and create artists
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

## Project Structure

- `app.py` — Flask backend (API & static file serving)
- `requirements.txt` — Python dependencies
- `template/` — Frontend HTML, CSS, JS
    - `index.html`, `songs.html`, `artists.html` — UI pages
    - `style.css` — Styles
    - `app-ui.js` — UI logic

## Notes
- Data is not persistent; restarting the app resets all songs/artists.
- For development only. Not production-ready.
- Github Repo: https://github.com/jime3462/CICD_Python_Anywhere
- Python App: https://jime3462.pythonanywhere.com/

---

© 2026 WaveRoom Project
