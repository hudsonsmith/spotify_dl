import spotipy
from spotipy.oauth2 import SpotifyOAuth

import json
from bs4 import BeautifulSoup
import requests
import re
from os import system
import yt_dlp as youtube_dl 

spotify_username: str = input("Enter Spotify Username: ")

scope: str = "user-library-read"
sp: spotipy.Spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

playlists = sp.user_playlists(spotify_username)
playlist_uris: list = []

while playlists:
    for i, playlist in enumerate(playlists["items"], start=1):
        print(f"{i}. {playlist['name']}")
        playlist_uris.append(playlist["uri"])

    if playlists["next"]:
        playlists = sp.next(playlists)

    else:
        playlists = None


playlist_uri: str = ""

while True:
    try:
        selected_uri: int = int(input("Select a playlist to download: ")) - 1
        playlist_uri = playlist_uris[selected_uri]

        break

    except (ValueError, IndexError):
        print("Invalid option.")

print(f"Selected Playlist: {playlist_uri}")
playlist_items = sp.playlist_items(playlist_uri)


songs: list = []

for item in playlist_items["items"]:
    songs.append(f"{item['track']['name']} \"{item['track']['album']['artists'][0]['name']}\"")

headers: dict = {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}

system("mkdir music")

for song in songs:
    youtube_html: str = requests.get(f"https://www.youtube.com/results", headers=headers, params={"search_query": song})
    youtube_page = BeautifulSoup(youtube_html.text, "html.parser")

    pattern: str = r'\/watch\?v=[\w-]{11}'
    url: str = re.findall(pattern, youtube_html.text)

    print(f"{song}: https://www.youtube.com{url[0]}")

    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"https://www.youtube.com{url[0]}"])

system("mv *.mp3 ./music")