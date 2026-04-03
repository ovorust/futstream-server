# server.py

import re
import html as html_module
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="StreamPicker API")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # libera geral (teste)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "https://multicanaishd.deals/futebol/"
GAME_URL_RE = re.compile(r"assistir-.+-x-.+ao-vivo", re.IGNORECASE)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

# ── Scraping ─────────────────────────────────────────────────────

def fetch_games():
    try:
        resp = requests.get(BASE_URL, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    soup = BeautifulSoup(resp.text, "html.parser")

    games, seen = [], set()

    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        text = a.get_text(strip=True).replace("\n", " ")

        if (
            href not in seen
            and href.startswith("http")
            and GAME_URL_RE.search(href)
            and text
        ):
            seen.add(href)
            games.append({
                "title": text[:90],
                "url": href
            })

    return games


def fetch_players(game_url: str):
    try:
        resp = requests.get(game_url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    soup = BeautifulSoup(resp.text, "html.parser")

    players, seen = [], set()

    for el in soup.select("[data-url]"):
        raw = el.get("data-url", "").strip()
        url = html_module.unescape(raw)
        text = el.get_text(strip=True) or el.get("title", "").strip()

        if url and url not in seen:
            seen.add(url)
            players.append({
                "name": text or "Player",
                "url": url
            })

    return players


# ── Endpoints ────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/games")
def get_games():
    return {"games": fetch_games()}


@app.get("/players")
def get_players(url: str = Query(...)):
    return {"players": fetch_players(url)}
