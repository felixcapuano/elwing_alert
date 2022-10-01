import requests
from bs4 import BeautifulSoup

elwing_url = "https://elwingboards.com/collections/powerkit-replacement-parts"
product_targets = ["Moteur Powerkit V2", "Moteur Powerkit V1"]

def send_notification():
    pass

def main():
    res = requests.get(elwing_url)
    soup = BeautifulSoup(res.text, 'html.parser')

    products = soup.find_all("div", "grid-product__content")
    for p in products:
        title = p.find("div", "grid-product__title")
        if title.string in product_targets:

            sold_out = p.find("div", "grid-product__tag grid-product__tag--sold-out")

            print(title.string + ", sold out = " + str(sold_out != None))

