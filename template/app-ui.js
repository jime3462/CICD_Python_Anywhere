function renderSongsTable(songs) {
  if (!Array.isArray(songs) || songs.length === 0) {
    return "No songs found.";
  }
  
  let html = "<table style='width:100%; border-collapse:collapse;'>";
  html += "<tr style='background:#16c1f3; color:#081018; font-weight:bold;'>";
  html += "<th style='padding:8px; text-align:left; border:1px solid #555;'>Song Name</th>";
  html += "<th style='padding:8px; text-align:left; border:1px solid #555;'>Artist</th>";
  html += "<th style='padding:8px; text-align:left; border:1px solid #555;'>Artist ID</th>";
  html += "</tr>";
  
  songs.forEach(song => {
    html += "<tr>";
    html += `<td style='padding:8px; border:1px solid #555;'>${song.title || "N/A"}</td>`;
    html += `<td style='padding:8px; border:1px solid #555;'>${song.artist_name || "Unknown"}</td>`;
    html += `<td style='padding:8px; border:1px solid #555;'>${song.artist_id || "N/A"}</td>`;
    html += "</tr>";
  });
  
  html += "</table>";
  return html;
}

function renderArtistTable(artist) {
  let html = "<table style='width:100%; border-collapse:collapse;'>";
  html += "<tr style='background:#16c1f3; color:#081018; font-weight:bold;'>";
  html += "<th style='padding:8px; text-align:left; border:1px solid #555;'>ID</th>";
  html += "<th style='padding:8px; text-align:left; border:1px solid #555;'>Name</th>";
  html += "</tr>";
  html += "<tr>";
  html += `<td style='padding:8px; border:1px solid #555;'>${artist.id || "N/A"}</td>`;
  html += `<td style='padding:8px; border:1px solid #555;'>${artist.name || "N/A"}</td>`;
  html += "</tr>";
  html += "</table>";
  return html;
}

function renderResult(targetId, payload, ok = true) {
  const node = document.getElementById(targetId);
  if (!node) {
    return;
  }
  node.className = `result ${ok ? "ok" : "error"}`;
  
  if (!ok) {
    node.textContent = JSON.stringify(payload, null, 2);
    return;
  }
  
  // Check if payload has songs array (from GET /songs)
  if (payload.songs && Array.isArray(payload.songs)) {
    node.innerHTML = renderSongsTable(payload.songs);
    return;
  }
  
  // Check if payload is a single song (from GET /songs/:id or POST /songs)
  if (payload.title !== undefined && payload.artist_id !== undefined) {
    node.innerHTML = renderSongsTable([payload]);
    return;
  }
  
  // Check if payload has artists array (from GET /artists)
  if (payload.artists && Array.isArray(payload.artists)) {
    let html = "<table style='width:100%; border-collapse:collapse;'>";
    html += "<tr style='background:#16c1f3; color:#081018; font-weight:bold;'>";
    html += "<th style='padding:8px; text-align:left; border:1px solid #555;'>ID</th>";
    html += "<th style='padding:8px; text-align:left; border:1px solid #555;'>Name</th>";
    html += "</tr>";
    
    payload.artists.forEach(artist => {
      html += "<tr>";
      html += `<td style='padding:8px; border:1px solid #555;'>${artist.id || "N/A"}</td>`;
      html += `<td style='padding:8px; border:1px solid #555;'>${artist.name || "N/A"}</td>`;
      html += "</tr>";
    });
    
    html += "</table>";
    node.innerHTML = html;
    return;
  }
  
  // Check if payload is a single artist (from POST /artists)
  if (payload.name !== undefined && payload.id !== undefined && !payload.title) {
    node.innerHTML = renderArtistTable(payload);
    return;
  }
  
  // Default: show as JSON
  node.textContent = JSON.stringify(payload, null, 2);
}

async function callApi(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  let body = {};
  try {
    body = await response.json();
  } catch (_err) {
    body = { error: "Server did not return JSON" };
  }

  if (!response.ok) {
    throw body;
  }

  return body;
}

function initSongsPage() {
  const songByIdForm = document.getElementById("songByIdForm");
  const createSongForm = document.getElementById("createSongForm");

  if (songByIdForm) {
    songByIdForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const songId = document.getElementById("songIdInput").value;
      try {
        const data = await callApi(`/songs/${songId}`);
        renderResult("songByIdResult", data);
      } catch (err) {
        renderResult("songByIdResult", err, false);
      }
    });
  }

  if (createSongForm) {
    createSongForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const title = document.getElementById("newSongTitle").value;
      const artistName = document.getElementById("newSongArtistName").value;

      try {
        // First, create the artist
        const artistData = await callApi("/artists", {
          method: "POST",
          body: JSON.stringify({ name: artistName }),
        });
        const artistId = artistData.id;

        // Then, create the song with that artist ID
        const songData = await callApi("/songs", {
          method: "POST",
          body: JSON.stringify({ title, artist_id: artistId }),
        });
        renderResult("createSongResult", songData);
      } catch (err) {
        renderResult("createSongResult", err, false);
      }
    });
  }
}

function initArtistsPage() {
  const btnAllArtists = document.getElementById("btnAllArtists");
  const createArtistForm = document.getElementById("createArtistForm");

  if (btnAllArtists) {
    btnAllArtists.addEventListener("click", async () => {
      try {
        const data = await callApi("/artists");
        renderResult("allArtistsResult", data);
      } catch (err) {
        renderResult("allArtistsResult", err, false);
      }
    });
  }

  if (createArtistForm) {
    createArtistForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const name = document.getElementById("newArtistName").value;
      try {
        const data = await callApi("/artists", {
          method: "POST",
          body: JSON.stringify({ name }),
        });
        renderResult("createArtistResult", data);
        document.getElementById("newArtistName").value = "";
      } catch (err) {
        renderResult("createArtistResult", err, false);
      }
    });
  }

}

function initSearchResultsPage() {
  const summary = document.getElementById("searchSummary");
  const resultNode = document.getElementById("searchPageResult");
  if (!summary || !resultNode) {
    return;
  }

  const params = new URLSearchParams(window.location.search);
  const keyword = (params.get("keyword") || "").trim();
  const keywordInput = document.getElementById("resultsKeyword");
  if (keywordInput) {
    keywordInput.value = keyword;
  }

  if (!keyword) {
    summary.textContent = "Enter a keyword in the header search bar to see results.";
    resultNode.className = "result";
    resultNode.textContent = "No search keyword provided.";
    return;
  }

  summary.textContent = `Showing matches for: "${keyword}"`;

  callApi(`/songs/search?keyword=${encodeURIComponent(keyword)}`)
    .then((data) => {
      renderResult("searchPageResult", data);
    })
    .catch((err) => {
      renderResult("searchPageResult", err, false);
    });
}

function initHomeSongs() {
  const homeSongsResult = document.getElementById("homeSongsResult");
  if (!homeSongsResult) {
    return;
  }

  callApi("/songs")
    .then((data) => {
      const sortedSongs = Array.isArray(data.songs)
        ? [...data.songs].sort((a, b) =>
            (a.title || "").localeCompare(b.title || "", undefined, { sensitivity: "base" })
          )
        : [];
      renderResult("homeSongsResult", {
        songs: sortedSongs,
        count: sortedSongs.length,
      });
    })
    .catch((err) => {
      renderResult("homeSongsResult", err, false);
    });
}

initSongsPage();
initArtistsPage();
initSearchResultsPage();
initHomeSongs();
