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


class TracksInfo(TypedDict):
    href: str
    total: int


class Playlist(TypedDict):
    collaborative: bool
    description: str
    external_urls: ExternalURLs
    href: str
    id: str
    images: List[Image]
    name: str
    owner: Owner
    primary_color: Optional[str]
    public: bool
    snapshot_id: str
    tracks: TracksInfo
    type: str
    uri: str
