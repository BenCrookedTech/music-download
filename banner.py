import pyfiglet
from termcolor import colored

colors = ['blue', 'cyan']

def colorful_banner(text):
    banner = pyfiglet.figlet_format(text)
    color = colors[0] 
    print(colored(banner, color))

def styled_banner(text):
    border = "=" * (len(text) + 10)
    print(colored(border, colors[1]))  
    colorful_banner(text)
    print(colored(border, colors[1]))

styled_banner("MUSIC DOWNLOAD")
