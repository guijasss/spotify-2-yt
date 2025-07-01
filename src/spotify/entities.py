from typing import TypedDict, List, Optional


class ExternalURLs(TypedDict):
    spotify: str


class Image(TypedDict):
    height: int
    url: str
    width: int


class Owner(TypedDict):
    display_name: str
    external_urls: ExternalURLs
    href: str
    id: str
    type: str
    uri: str


class PlaylistTrack(TypedDict):
    id: str
    name: str
    artists: List[str]


class Playlist(TypedDict):
    id: str
    name: str
    description: str
