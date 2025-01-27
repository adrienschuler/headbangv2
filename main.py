import os
from urllib.parse import urlencode

import httpx
import requests

from fastapi import FastAPI, Query, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="perplexity")

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SCOPES = "user-read-private user-read-email user-library-read"

@app.get("/login")
async def login():
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES
    }
    auth_url = f"{SPOTIFY_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(url=auth_url)

@app.get("/callback")
async def callback(request: Request, code: str = Query(None)):
    if not code:
        return {"error": "Authorization code not found"}

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(SPOTIFY_TOKEN_URL, data=data)

    if response.status_code == 200:
        token_data = response.json()
        request.session["access_token"] = token_data["access_token"]
        return {"access_token": token_data["access_token"]}
    else:
        return {"error": "Failed to retrieve access token"}

async def get_session_token(request: Request):
    token = request.session.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Access token not found in session")
    return token

@app.get("/saved-tracks")
async def get_saved_tracks(token: str = Depends(get_session_token), limit: int = 20, offset: int = 0):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    params = {
        "limit": min(limit, 50),  # Spotify API allows max 50 tracks per request
        "offset": offset
    }

    response = requests.get(
        "https://api.spotify.com/v1/me/tracks",
        headers=headers,
        params=params
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch saved tracks")
