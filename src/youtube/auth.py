from requests import post
from webbrowser import open
from http.server import SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, urlencode
from os import getenv
from socketserver import TCPServer
from dotenv import load_dotenv

load_dotenv()

# CONFIG
CLIENT_ID = getenv("YOUTUBE_CLIENT_ID")
CLIENT_SECRET = getenv("YOUTUBE_CLIENT_SECRET")
REDIRECT_URI = getenv("YOUTUBE_REDIRECT_URI")
SCOPE = "https://www.googleapis.com/auth/youtube"
_token_data = None


class YouTubeAuthHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        global _token_data
        query = urlparse(self.path).query
        params = parse_qs(query)

        if "code" in params:
            code = params["code"][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Autenticacao concluida! Pode fechar esta aba.")
            _token_data = exchange_code_for_token(code)
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Erro ao obter codigo.")


def build_auth_url():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE,
        "access_type": "offline",
        "prompt": "consent"
    }
    return f"https://accounts.google.com/o/oauth2/auth?{urlencode(params)}"


def exchange_code_for_token(code: str) -> dict:
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    response = post("https://oauth2.googleapis.com/token", data=data)
    response.raise_for_status()
    return response.json()


def youtube_authenticate() -> dict:
    global _token_data
    _token_data = None

    auth_url = build_auth_url()
    print(f"\n🔗 Abrindo navegador para autenticação do YouTube...\n{auth_url}\n")
    open(auth_url)

    with TCPServer(("", 8080), YouTubeAuthHandler) as httpd:
        print("🌐 Aguardando autenticação...")
        while _token_data is None:
            httpd.handle_request()

    print("✅ Token recebido!")
    print(_token_data)
    return _token_data
