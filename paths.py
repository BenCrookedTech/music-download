import os
import platform

def get_downloads_folder():
    if "ANDROID_ROOT" in os.environ or "com.termux" in os.environ.get("HOME", ""):
        return os.path.join(os.environ["HOME"], "storage", "downloads")

    system = platform.system()

    if system == "Windows":
        return os.path.join(os.environ["USERPROFILE"], "Downloads")
    elif system in ["Linux", "Darwin"]:
        return os.path.join(os.environ["HOME"], "Music")
    else:
        return os.getcwd()
