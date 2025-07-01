from typing import cast, List
from requests import get, HTTPError

from src.spotify.auth import authenticate
from src.spotify.entities import Playlist, PlaylistTrack


def fetch_user_playlists(access_token: str) -> List[Playlist]:
    url = "https://api.spotify.com/v1/me/playlists"
    headers = {"Authorization": f"Bearer {access_token}"}
    playlists = []
    params = {"limit": 50}

    while url:
        response = get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        playlists.extend(data.get("items", []))
        url = data.get("next")

    return cast(List[Playlist], [{
        "id": p.get("id"),
        "name": p.get("name")
    } for p in playlists])

def fetch_playlist_tracks(access_token: str, playlist_id: str) -> List[PlaylistTrack]:
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {"Authorization": f"Bearer {access_token}"}
    tracks = []
    params = {"limit": 100}  # Máximo permitido por requisição

    while url:
        response = get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        tracks.extend(data.get("items", []))
        url = data.get("next")  # Paginação

    return cast(List[PlaylistTrack], [{
        "id": p.get("track").get("id"),
        "name": p.get("track").get("name"),
        "artists": [artist.get("name") for artist in p.get("track").get("artists")]
    } for p in tracks])

if __name__ == "__main__":
    try:
        tokens = authenticate()
        playlists = fetch_user_playlists(tokens["access_token"])

        data = fetch_playlist_tracks(tokens["access_token"], playlists[0]["id"])

        print(data)

        # print("\n🎵 Your Playlists:")
        # for playlist in playlists:
        #     print(f"- {playlist['name']} (ID: {playlist['id']})")

    except HTTPError as e:
        print(f"\n⚠️ HTTP Error: {e.response.status_code} - {e.response.text}\n")

    except Exception as e:
        print(f"\n⚠️ Unexpected error: {e}\n")
