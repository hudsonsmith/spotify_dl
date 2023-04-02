import requests
from bs4 import BeautifulSoup
import re
from os import system
import yt_dlp as youtube_dl 
from os import system

playlist_url: str = input("Spotify Playlist Url: ")

song_html: str = requests.get(playlist_url)
song_page = BeautifulSoup(song_html.text, "html.parser")

songs: list = []


# Get the songs.
for song in song_page.find_all(attrs={"data-testid": "entity-row-v2-button"}):
    song_text: str = song.text

    # Get the number in the song to remove.
    i: int = 0
    char_found: bool = False

    while char_found is False:
        for char in song_text:
            if char in "1234567890":
                i += 1

            else:
                char_found = True

    song_text = song_text[i:]

    songs.append(song_text)


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
