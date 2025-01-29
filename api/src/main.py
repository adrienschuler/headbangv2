from urllib.parse import urlencode
from functools import lru_cache
import httpx
# import json
import requests

from fastapi import FastAPI, Query, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from typing_extensions import Annotated
# from kafka import KafkaProducer

from . import config


app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="perplexity")

@lru_cache
def get_settings():
    return config.Settings()

# producer = KafkaProducer(
#     bootstrap_servers=KAFKA_BROKER,
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )

@app.get("/login")
async def login(settings: Annotated[config.Settings, Depends(get_settings)]):
    params = {
        "client_id": settings.spotify_client_id,
        "response_type": "code",
        "redirect_uri": settings.spotify_redirect_uri,
        "scope": settings.spotify_scopes,
    }
    auth_url = f"{settings.spotify_auth_url}?{urlencode(params)}"
    return RedirectResponse(url=auth_url)

@app.get("/callback")
async def callback(
    settings: Annotated[config.Settings, Depends(get_settings)],
    request: Request,
    code: str = Query(None)):

    if not code:
        return {"error": "Authorization code not found"}

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.spotify_redirect_uri,
        "client_id": settings.spotify_client_id,
        "client_secret": settings.spotify_client_secret,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(settings.spotify_token_url, data=data)

    if response.status_code == 200:
        token_data = response.json()
        request.session["access_token"] = token_data["access_token"]
        return {"access_token": token_data["access_token"]}
    else:
        return {"error": "Failed to retrieve access token"}

async def get_access_token(request: Request):
    token = request.session.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Access token not found in session")
    return token

def fetch_saved_tracks(access_token: str, limit: int = 50, offset: int = 0):
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"limit": limit, "offset": offset}
    response = requests.get("https://api.spotify.com/v1/me/tracks", headers=headers, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()

# def send_to_kafka(topic: str, data: dict):
#     producer.send(topic, data)
#     producer.flush()

# @app.get("/saved-tracks")
# async def get_saved_tracks(token: str = Depends(get_access_token), limit: int = 50, offset: int = 0):
#     while True:
#         data = fetch_saved_tracks(token, limit=limit, offset=offset)
#         if not data['items']:
#             break

#         for item in data['items']:
#             track_info = {
#                 "track_id": item['track']['id'],
#                 "track_name": item['track']['name'],
#                 "artist_name": [artist['name'] for artist in item['track']['artists']],
#                 "album_name": item['track']['album']['name']
#             }
#             send_to_kafka(KAFKA_TOPIC, track_info)

#         offset += 50

#     return {"message": "Tracks ingested successfully"}
