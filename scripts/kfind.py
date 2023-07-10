# kfind.py
import sys
import os
from pathlib import Path

from kittyfinder import KittyListPage, web

def main():
    sys.stderr = open(Path(os.getcwd(), 'myerrors.log'), "w+")
    KITTY_PAGE = "https://www.adoptapet.com/pet-search?age[0]=kitten&age[1]=young&speciesId=2&radius=15&postalCode=90278"
    page = KittyListPage(KITTY_PAGE)
    web(page.kittyPages)

if __name__ == "__main__":
    main()