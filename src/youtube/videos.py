from requests import get
from typing import Optional
from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Sua chave de API gerada no Google Cloud
API_KEY = getenv("YOUTUBE_API_KEY")


def search_video(query: str, max_results: int = 1) -> Optional[str]:
    """
    Busca um vídeo no YouTube e retorna o ID do primeiro resultado encontrado.
    """
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": API_KEY,
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results
    }

    response = get(url, params=params)
    response.raise_for_status()
    results = response.json().get("items", [])

    if not results:
        print(f"⚠️ Nenhum vídeo encontrado para: {query}")
        return None

    video_id = results[0]["id"]["videoId"]
    print(f"🎬 Vídeo encontrado: https://youtu.be/{video_id}")
    return video_id


if __name__ == "__main__":
    while True:
        query = input("\n🔎 Digite o nome da música e artista para buscar no YouTube (ou 'sair'): ").strip()
        if query.lower() == "sair":
            break
        search_video(query)
