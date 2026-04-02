"""
server.py - Backend FastAPI para FutStream
Fornece APIs para scraping de jogos e players
"""

import re
import html as html_module
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

# ── Configuração ──────────────────────────────────────────────────────────────
BASE_URL    = "https://multicanaishd.deals/futebol/"
GAME_URL_RE = re.compile(r"assistir-.+-x-.+ao-vivo", re.IGNORECASE)

# ── Models ────────────────────────────────────────────────────────────────────
class GameDTO(BaseModel):
    title: str
    url: str

class PlayerDTO(BaseModel):
    label: str
    url: str

# ── FastAPI App ───────────────────────────────────────────────────────────────
app = FastAPI(title="FutStream API", version="1.0.0")

# Configurar CORS para permitir requisições do frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Scraping Functions ────────────────────────────────────────────────────────

def _make_browser():
    """Cria e retorna um contexto do Playwright"""
    pw      = sync_playwright().start()
    browser = pw.chromium.launch(headless=True)
    ctx     = browser.new_context(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        viewport={"width": 1280, "height": 800},
    )
    page = ctx.new_page()
    return pw, browser, page


def fetch_games() -> List[GameDTO]:
    """Fetch lista de jogos ao vivo"""
    pw, browser, page = _make_browser()
    try:
        page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30_000)
        page.wait_for_timeout(2500)
        games, seen = [], set()
        
        for a in page.query_selector_all("a[href]"):
            href = (a.get_attribute("href") or "").strip()
            text = (a.inner_text() or "").strip().replace("\n", " ")
            if (
                href and href not in seen
                and href.startswith("http")
                and GAME_URL_RE.search(href)
                and text
            ):
                seen.add(href)
                games.append(GameDTO(title=text[:90], url=href))
        
        return games
    finally:
        browser.close()
        pw.stop()


def fetch_players(game_url: str) -> List[PlayerDTO]:
    """Fetch lista de players para um jogo específico"""
    pw, browser, page = _make_browser()
    try:
        page.goto(game_url, wait_until="domcontentloaded", timeout=30_000)
        page.wait_for_timeout(3000)
        players, seen = [], set()
        
        for el in page.query_selector_all("[data-url]"):
            raw = (el.get_attribute("data-url") or "").strip()
            url = html_module.unescape(raw)
            text = (el.inner_text() or el.get_attribute("title") or "").strip()
            if url and url not in seen:
                seen.add(url)
                players.append(PlayerDTO(label=text or "Player", url=url))
        
        return players
    finally:
        browser.close()
        pw.stop()

# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/api/health")
def health_check():
    """Verifica se a API está online"""
    return {"status": "ok"}


@app.get("/api/games", response_model=List[GameDTO])
def get_games():
    """Retorna lista de jogos ao vivo"""
    try:
        games = fetch_games()
        return games
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar jogos: {str(e)}")


@app.get("/api/players", response_model=List[PlayerDTO])
def get_players(game_url: str):
    """Retorna lista de players para um jogo específico"""
    if not game_url:
        raise HTTPException(status_code=400, detail="game_url é obrigatório")
    
    try:
        players = fetch_players(game_url)
        return players
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar players: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
