from requests import get, post
from typing import Optional


def create_youtube_playlist(access_token: str, playlist_name: str, description: str = "") -> str:
    url = "https://www.googleapis.com/youtube/v3/playlists"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    params = {
        "part": "snippet,status"  # Obrigatório informar quais partes do recurso estamos enviando
    }
    data = {
        "snippet": {
            "title": playlist_name,
            "description": description
        },
        "status": {
            "privacyStatus": "private"  # Ou "public", "unlisted"
        }
    }

    response = post(url, headers=headers, params=params, json=data)
    print(f"🔧 Status: {response.status_code}, Conteúdo: {response.text}")  # Log para depuração
    response.raise_for_status()
    playlist_id = response.json()["id"]
    print(f"✅ Playlist criada: {playlist_name} (ID: {playlist_id})")
    return playlist_id


def search_youtube_video(access_token: str, query: str) -> Optional[str]:
    url = "https://www.googleapis.com/youtube/v3/search"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 1
    }

    response = get(url, headers=headers, params=params)
    response.raise_for_status()
    items = response.json().get("items", [])

    if not items:
        print(f"⚠️ Nenhum vídeo encontrado para: {query}")
        return None

    video_id = items[0]["id"]["videoId"]
    print(f"🎬 Vídeo encontrado: https://youtu.be/{video_id}")
    return video_id


def add_video_to_playlist(access_token: str, playlist_id: str, video_id: str):
    url = "https://www.googleapis.com/youtube/v3/playlistItems"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    params = {
        "part": "snippet,status"  # Obrigatório informar quais partes do recurso estamos enviando
    }
    data = {
        "snippet": {
            "playlistId": playlist_id,
            "resourceId": {
                "kind": "youtube#video",
                "videoId": video_id
            }
        }
    }

    response = post(url, headers=headers, params=params, json=data)
    response.raise_for_status()
    print(f"🎶 Vídeo adicionado à playlist: https://youtu.be/{video_id}")
