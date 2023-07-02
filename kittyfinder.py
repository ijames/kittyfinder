#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import webbrowser
import os
from pathlib import Path
from datetime import datetime

KITTY_PAGE = "https://www.adoptapet.com/pet-search?age[0]=kitten&age[1]=young&speciesId=2&radius=15&postalCode=90278"

def getPage(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, "html.parser")

def kittyName(soup):
    h1s = soup.find_all("h1")
    for h1 in h1s:
        t = h1.text
        # print(t)
        # import pdb; pdb.set_trace()
        if "My name is" in h1.text.strip():
            return h1.text.strip()
    return "No Name?"

def goodWithDoggie(soup):
    spans = soup.find_all("span")
    for span in spans:
        phrase = span.text.strip()
        if phrase == "Good with dogs":
            return True
    return False

def getKitties(soup):
    kitties = []
    anchors = soup.find_all("a")
    for anchor in anchors:
        print(".", end="")
        href = anchor.get("href", "")
        if '/pet/' in href:
            kittySoup = getPage(href)
            if goodWithDoggie(kittySoup):
                name = kittyName(soup)
                kitties.append({'name': name, 'url': href})
                print(href, name)
                # break
    return kitties

kitties = getKitties(getPage(KITTY_PAGE))

dt = datetime.now().strftime('%Y%m%d')
file = Path(os.getcwd()) / f'mypage.{dt}.html'
with file.open('w') as p:
    p.write("<html><body>\n")
    p.write(f'<h2>Kitties that are good with doggies found today: {dt}</h2>\n')
    p.write(f'<ul>\n')
    for kitty in kitties:
        p.write(f'<li><a href="{kitty["url"]}">{kitty["url"]}: {kitty["name"]}</a></li>\n')
    # p.write(f'<iframe id="kitties" style="width:800px;height:800px"/>\n')
    p.write("</ul>")
    p.write("</body></html>")
webbrowser.open(f'file://{file}')
print("Content-type: text/html\n\n")
print(f'file://{file}')




