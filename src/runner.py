from src.spotify.auth import spotify_authenticate
from src.spotify.playlists import fetch_user_playlists, fetch_playlist_tracks
from src.youtube.auth import youtube_authenticate
from src.youtube.videos import create_youtube_playlist, search_youtube_video, add_video_to_playlist

spotify_token = spotify_authenticate()["access_token"]
yt_token = youtube_authenticate()["access_token"]

playlist = fetch_user_playlists(spotify_token)[0]
tracks = fetch_playlist_tracks(spotify_token, playlist["id"])

playlist_name = playlist["name"]
playlist_description = playlist["description"]

print(playlist)
print(tracks)

playlist_id = create_youtube_playlist(yt_token, playlist_name, playlist_description)

for track in tracks:
    video_id = search_youtube_video(yt_token, f"{track["name"]} {' '.join(track['artists'])}")
    if video_id:
        add_video_to_playlist(yt_token, playlist_id, video_id)
