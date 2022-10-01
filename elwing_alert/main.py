import requests
from bs4 import BeautifulSoup

elwing_url = "https://elwingboards.com/collections/powerkit-replacement-parts"
webhook_discord = "https://discord.com/api/webhooks/1025867563437146173/hQNMuzkFP72paAh0k3RSDnvMzHnXTqy5HID9JzSpEzQvj-s1lRa_KaNoTcA-ovhhZDUN"

product_targets = ["Moteur Powerkit V2", "Moteur Powerkit V1"]

def send_discord_notification():
    message = "je suis content"
    requests.post(webhook_discord, json={"content": message})

def main():
    res = requests.get(elwing_url)
    soup = BeautifulSoup(res.text, 'html.parser')

    products = soup.find_all("div", "grid-product__content")
    for p in products:
        title = p.find("div", "grid-product__title")
        if title.string in product_targets:

            sold_out = p.find("div", "grid-product__tag grid-product__tag--sold-out")

            print(title.string + ", sold out = " + str(sold_out != None))
    
    send_discord_notification()

