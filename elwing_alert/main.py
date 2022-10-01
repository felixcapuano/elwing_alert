import requests
from bs4 import BeautifulSoup

elwing_url = "https://elwingboards.com"
elwing_parts_url = elwing_url + "/collections/powerkit-replacement-parts"
webhook_discord = "https://discord.com/api/webhooks/1025867563437146173/hQNMuzkFP72paAh0k3RSDnvMzHnXTqy5HID9JzSpEzQvj-s1lRa_KaNoTcA-ovhhZDUN"

product_targets = ["Moteur Powerkit V2", "Moteur Powerkit V1", "Paire de gommes de roue motrice V2"]

def send_discord_notification(message):
    requests.post(webhook_discord, json={"content": message})
    

def create_status_message(status):
    message = "Hello <@421801671237042176>\n" 
    for s in status:
        status_text = "unavailable" if s["sold_out"] else "available"
        message += f"\"{s['title']}\" is [**{status_text}**]({s['link']})\n"
        
    return message

def main():
    res = requests.get(elwing_parts_url)
    soup = BeautifulSoup(res.text, 'html.parser')

    products = soup.find_all("div", "grid-product__content")
    status = []
    for p in products:
        title = p.find("div", "grid-product__title")

        if title.string not in product_targets:
            continue

        link = p.find("a")
        link = elwing_url + link["href"]
        sold_out = p.find("div", "grid-product__tag grid-product__tag--sold-out")
        sold_out = sold_out != None

        if not sold_out:
            status.append(dict(title=title.string, sold_out=sold_out, link=link))
    
    if status:
        message = create_status_message(status)
        send_discord_notification(message)

