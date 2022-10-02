import logging
import os
import sys
import requests
from bs4 import BeautifulSoup

elwing_url = "https://elwingboards.com"
elwing_parts_url = elwing_url + "/collections/powerkit-replacement-parts"
webhook_discord = os.getenv("WEBHOOK_DISCORD")

product_targets = ["Moteur Powerkit V2", "Moteur Powerkit V1", "Chargeur Standard"]

logging.basicConfig(format="%(asctime)s %(message)s", stream=sys.stdout, level=logging.INFO)

def send_discord_notification(message):
    requests.post(webhook_discord, json={"content": message})
    

def create_status_message(status):
    message = "🖐️ Hello <@421801671237042176>\n\n" 
    for s in status:
        status_text = "unavailable" if s["sold_out"] else "available"
        message += f"🟢 \"{s['title']}\" is **{status_text}**\n"
    
    message += f"\n👉 [Elwing parts page link]({elwing_parts_url})"
        
    return message

def main():
    res = requests.get(elwing_parts_url)
    logging.info(f"message=\"Load elwing page\" status_code=\"{res.status_code}\"")

    soup = BeautifulSoup(res.text, 'html.parser')

    products = soup.find_all("div", "grid-product__content")
    status = []
    for p in products:
        title = p.find("div", "grid-product__title")

        if title.string not in product_targets:
            continue

        # link = p.find("a")
        # link = elwing_url + link["href"]
        sold_out = p.find("div", "grid-product__tag grid-product__tag--sold-out")
        sold_out = sold_out != None
        logging.info(f"product=\"{title.string}\" sold_out={sold_out}")

        if not sold_out:
            status.append(dict(title=title.string, sold_out=sold_out))
    
    if status:
        message = create_status_message(status)
        message_str = message.replace('\n', '\\n')
        logging.info(f"message=\"Send message to discord\" content=\"{message_str}\"")
        send_discord_notification(message)
    else: 
        logging.info("message=\"No product are available, no message send\"")

