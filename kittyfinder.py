import requests
from bs4 import BeautifulSoup

URL = "https://www.adoptapet.com/pet-search?age[0]=kitten&age[1]=young&speciesId=2&radius=15&postalCode=90278"

def getPage(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, "html.parser")

def goodWithDoggie(soup):
    spans = soup.find_all("span")
    for span in spans:
        phrase = span.text.strip()
        if phrase == "Good with dogs":
            return True
    return False

def getKitties(soup):
    anchors = soup.find_all("a")
    for anchor in anchors:
        href = anchor.get("href", "")
        if '/pet/' in href:
            kittySoup = getPage(href)
            if goodWithDoggie(kittySoup):
                print(f'Good with doggies! {href}')

kittyPage = URL
getKitties(getPage(kittyPage))
# print(soup)




