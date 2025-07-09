import yt_dlp
import os
from banner import styled_banner
from paths import get_downloads_folder
from colorama import Fore, Style, init

def show_progress(text):
    print(text)

def search_track(query, max_results=5):
    styled_banner("SEARCHING")
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

def download_track(video_url):
    styled_banner("⬇DOWNLOADING")
    download_path = get_downloads_folder()
    os.makedirs(download_path, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',
        'quiet': False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

def main_menu():
    while True:
        print(Fore.CYAN + "\n Main Menu:")
        print(Fore.YELLOW +"[1.]" + Fore.WHITE + "Enter song name or artist ")
        print(Fore.YELLOW +"[2.]" + Fore.WHITE + "Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            query = input("🎧 Enter artist or song name: ")
            results = search_track(query)

            if not results:
                print(Fore.RED + " No results found.")
                continue

            try:
                index = int(input("\n Enter number to download: ")) - 1
                if 0 <= index < len(results):
                    selected = results[index]
                    print(Fore.GREEN + f"\n You selected: {selected['title']}")
                    download_track(selected['url'])
                    print(Fore.GREEN + "\n Download complete. Returning to menu...")
                else:
                    print(Fore.RED + "Invalid choice.")
            except ValueError:
                print(Fore.RED + "Please enter a valid number.")
        elif choice == "2":
            print(Fore.CYAN + "You chose to leave, come again soon!")
            break
        else:
            print(Fore.RED + "Invalid choice. Please choose 1 or 2.")

main_menu()
