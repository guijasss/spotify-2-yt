import http.server
import socketserver
import urllib.parse
import webbrowser
import base64
import requests
from os import getenv

from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = getenv("CLIENT_ID")
CLIENT_SECRET = getenv("CLIENT_SECRET")
REDIRECT_URI = getenv("REDIRECT_URI")
SCOPE = "playlist-read-private playlist-read-collaborative"

_auth_code = None


class SpotifyAuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global _auth_code
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)

        if "code" in params:
            _auth_code = params["code"][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Authentication successful! You can close this window.")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Error: Authorization code not found.")


def build_authorization_url():
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE
    }
    return f"https://accounts.spotify.com/authorize?{urllib.parse.urlencode(params)}"


def encode_credentials():
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    return base64.b64encode(credentials.encode()).decode()


def start_local_server():
    with socketserver.TCPServer(("", 8000), SpotifyAuthHandler) as httpd:
        print("🌐 Waiting for Spotify authentication...")
        while _auth_code is None:
            httpd.handle_request()


def exchange_code_for_token(code):
    headers = {
        "Authorization": f"Basic {encode_credentials()}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    response.raise_for_status()
    return response.json()


def authenticate():
    global _auth_code
    _auth_code = None  # Reset authorization code

    auth_url = build_authorization_url()
    print(f"\n🔗 Opening browser for Spotify authentication...\n{auth_url}\n")
    webbrowser.open(auth_url)

    start_local_server()

    print(f"\n✅ Authorization code received: {_auth_code}\n")
    tokens = exchange_code_for_token(_auth_code)
    print(tokens)
    return tokens
