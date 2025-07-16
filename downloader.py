import yt_dlp
import os
from banner import styled_banner
from paths import get_downloads_folder
from colorama import Fore, Style, init

init(autoreset=True)

def show_progress(text):
    print(text)

def search_track(query, max_results=5):
    styled_banner("🔍 SEARCHING")
    yt_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True
    }

    with yt_dlp.YoutubeDL(yt_opts) as ydl:
        results = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)

    tracks = results.get("entries", [])
    for idx, track in enumerate(tracks, 1):
        print(f"{idx}. {track.get('title')}")
    return tracks

def search_soundcloud(query, max_results=5):
    styled_banner("🔍 SEARCHING")
    yt_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,
    }

    with yt_dlp.YoutubeDL(yt_opts) as ydl:
        results = ydl.extract_info(f"scsearch{max_results}:{query}", download=False)

    tracks = results.get("entries", [])
    for idx, track in enumerate(tracks, 1):
        print(f"{idx}. {track.get('title')} - {track.get('uploader')}")
    return tracks

def download_youtube_audio(video_url, format="mp3"):
    styled_banner(f"🎧 DOWNLOADING {format.upper()}")
    download_path = get_downloads_folder()
    os.makedirs(download_path, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio[ext=m4a]' if format == "m4a" else 'bestaudio/best',
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',
        'quiet': False
    }

    if format == "mp3":
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

def download_youtube_video(video_url):
    styled_banner("DOWNLOADING VIDEO")
    download_path = get_downloads_folder()
    os.makedirs(download_path, exist_ok=True)

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'quiet': False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

def download_soundcloud_mp3(sc_url):
    styled_banner("🎧 DOWNLOADING MP3...")
    download_path = get_downloads_folder()
    os.makedirs(download_path, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([sc_url])

def main_menu():
    while True:
        print(Fore.CYAN + "\nMain Menu:")
        print(Fore.YELLOW + "[1.]" + Fore.WHITE + " Search and Download videos ")
        print(Fore.YELLOW + "[2.]" + Fore.WHITE + " Search and Download MP3")
        print(Fore.YELLOW + "[3.]" + Fore.WHITE + " Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            query = input("Enter artist or song name: ")
            results = search_track(query)

            if not results:
                print(Fore.RED + "No results found.")
                continue

            try:
                index = int(input("\n🎵 Select a track number to download: ")) - 1
                if 0 <= index < len(results):
                    selected = results[index]
                    print(Fore.GREEN + f"\nYou selected: {selected['title']}")

                    print(Fore.YELLOW + "\n[1]" + Fore.WHITE + " Download as MP3")
                    print(Fore.YELLOW + "[2]" + Fore.WHITE + " Download as Video")
                    print(Fore.YELLOW + "[3]" + Fore.WHITE + " Download as M4A")
                    format_choice = input("Choose format: ")

                    if format_choice == "1":
                        download_youtube_audio(selected['url'], format="mp3")
                    elif format_choice == "2":
                        download_youtube_video(selected['url'])
                    elif format_choice == "3":
                        download_youtube_audio(selected['url'], format="m4a")
                    else:
                        print(Fore.RED + "Invalid format option.")

                    print(Fore.GREEN + "\nDownload complete. Returning to menu...")
                else:
                    print(Fore.RED + "Invalid track number.")
            except ValueError:
                print(Fore.RED + "Please enter a valid number.")

        elif choice == "2":
            query = input("Enter song or artist name: ")
            results = search_soundcloud(query)

            if not results:
                print(Fore.RED + "No results found.")
                continue

            try:
                index = int(input("\nSelect a track number to download: ")) - 1
                if 0 <= index < len(results):
                    selected = results[index]
                    print(Fore.GREEN + f"\n You selected: {selected['title']}")
                    download_soundcloud_mp3(selected['url'])
                    print(Fore.GREEN + "\n download complete.")
                else:
                    print(Fore.RED + "Invalid track number.")
            except ValueError:
                print(Fore.RED + "Please enter a valid number.")

        elif choice == "3":
            print(Fore.CYAN + "Exiting. Come back soon!")
            break

        else:
            print(Fore.RED + "Invalid choice. Please select from the menu.")

main_menu()
