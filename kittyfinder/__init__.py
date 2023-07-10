#!/home/shming/.cache/pypoetry/virtualenvs/kittyfinder-nqEBsQIc-py3.11/bin/python
import os
from pathlib import Path

#import webbrowser
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class Page:
    def __init__(self, url):
        self.url = url
        self.soup = self.getPage(url)

    def getPage(self, url, capture = False):
        page = requests.get(url)
        if capture:
            dt = datetime.now().strftime('%Y%m%d')
            file = Path(os.getcwd()) / f'kittypage.{dt}.html'
            with file.open('w') as p:
                    p.write(page.text)
        return BeautifulSoup(page.content, "html.parser")

class KittyListPage(Page):
    """
    This is the page that contains all the kitties
    """
    def __init__(self, url):
        super().__init__(url)
        self.kittyPages = self.getKittyPages()

    def getKittyPages(self):
        kittyPages = []
        anchors = self.soup.find_all("a")
        for url in [anchor.get("href", "") for anchor in anchors]:
            print(".", end="")
            if self.isKittyPage(url):
                kittyPage = KittyPage(url)
                if kittyPage.goodWithDoggie:
                    print("+")
                    kittyPages.append(kittyPage)    
        return kittyPages

    def isKittyPage(self, url):
        return '/pet/' in url

class KittyPage(Page):

    @property
    def kittyName(self):
        h1s = self.soup.find_all('h1')
        for h1 in h1s:
            t = h1.text
            if "My name is" in h1.text.strip():
                return h1.text.strip()
        return "No Name?"

    @property
    def goodWithDoggie(self):
        spans = self.soup.find_all("span")
        for span in spans:
            phrase = span.text.strip()
            if phrase == "Good with dogs":
                return True
        return False

    def __str__(self):
        return f'<li><a href="{self.url}">{self.kittyName}</a></li>'


def file(kittyPages):
    dt = datetime.now().strftime('%Y%m%d')
    file = Path(os.getcwd()) / f'mypage.{dt}.html'
    with file.open('w') as p:
        p.write("<html><body>\n")
        p.write(f'<h2>Kitties that are good with doggies found today: {dt}</h2>\n')
        p.write(f'<ul>\n')
        for kittyPage in kittyPages:
            p.write(kittyPage + "\n")
        p.write("</ul>")
        p.write("</body></html>")
    return file


def web(kittyPages):
    kittyList = ""
    for kittyPage in kittyPages:
        kittyList += f"""{kittyPage}
"""

    STYLE = """
<link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css">
<style>
* {font-family: sans}
</style>
"""
    HTML = f"""Content-type: text/html

<html>
<head>
{STYLE}
</head>
<body>
<h1>I found some kittyPages for you!</h1>
<ul>
{kittyList}
</ul>
</body>
"""

    print(HTML)
