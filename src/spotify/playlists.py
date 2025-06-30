from typing import List
from requests import get, HTTPError

from src.spotify.auth import authenticate
from src.spotify.entities import Playlist

def fetch_user_playlists(access_token) -> List[Playlist]:
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

    print(playlists)
    return playlists

if __name__ == "__main__":
    try:
        tokens = authenticate()
        playlists = fetch_user_playlists(tokens["access_token"])

        print("\n🎵 Your Playlists:")
        for playlist in playlists:
            print(f"- {playlist['name']} (ID: {playlist['id']})")

    except HTTPError as e:
        print(f"\n⚠️ HTTP Error: {e.response.status_code} - {e.response.text}\n")

    except Exception as e:
        print(f"\n⚠️ Unexpected error: {e}\n")
