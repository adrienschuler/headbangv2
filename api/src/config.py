from pydantic import KafkaDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    spotify_client_id: str
    spotify_client_secret: str
    spotify_redirect_uri: str = "http://localhost:8080/callback"
    spotify_auth_url: str = "https://accounts.spotify.com/authorize"
    spotify_token_url: str = "https://accounts.spotify.com/api/token"
    spotify_scopes: str = "user-read-private user-read-email user-library-read"

    # kafka_broker: KafkaDsn = "localhost:30092"
    # kafka_topic = "spotify_saved_tracks"

    model_config = SettingsConfigDict(env_file=".env")
