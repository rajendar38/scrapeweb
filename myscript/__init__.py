import logging
import requests
import json
from bs4 import BeautifulSoup
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import azure.functions as func

# Configuration
URL = 'https://cortland.com/apartments/the-palmer-at-las-colinas/available-apartments'
FLOORS_TO_ALERT = {'1', '2'}

# 🔒 Sensitive values masked for public sharing
SENDGRID_API_KEY = 'your_sendgrid_api_key_here'
SENDER_EMAIL = 'your_verified_sender@example.com'
RECIPIENT_EMAIL = [
    'recipient1@example.com',
    'recipient2@example.com',
    'recipient3@example.com'
]

def fetch_apartments():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    matching_units = []

    floor_divs = soup.find_all("div", class_="apartments__card")
    for card in floor_divs:
        btn = card.find('button', attrs={'data-event-extra': True})
        if not btn:
            continue

        try:
            meta = json.loads(btn['data-event-extra'])
        except json.JSONDecodeError:
            continue

        bedrooms = meta.get('bedrooms')
        unit_number = meta.get('unit')
        floorplan = meta.get('floor_plan_name')
        price = meta.get('starting_at_price')
        community = meta.get('community_name')
        neighborhood = meta.get('neighborhood')

        floor_info = card.select_one('.apartments__card-info--location')
        if floor_info:
            floor_text = floor_info.get_text(strip=True)
            floor_num = floor_text.replace('Floor', '').strip()
        else:
            floor_num = None

        if bedrooms == '2' and floor_num in FLOORS_TO_ALERT:
            matching_units.append({
                'unit': unit_number,
                'bedrooms': bedrooms,
                'floor': floor_num,
                'floorplan': floorplan,
                'price': price,
                'community': community,
                'neighborhood': neighborhood,
            })

    return matching_units

def send_email(apartments):
    body = '\n\n'.join(
        f"Unit: {a['unit']}\n"
        f"Floor: {a['floor']}\n"
        f"Bedrooms: {a['bedrooms']}\n"
        f"Plan: {a['floorplan']}\n"
        f"Price: ${a['price']}\n"
        f"Community: {a['community']}, {a['neighborhood']}"
        for a in apartments
    )

    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=RECIPIENT_EMAIL,
        subject='🚨 New 2-Bedroom Apartment Available!',
        plain_text_content=body
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        logging.info(f"✅ Email sent! Status Code: {response.status_code}")
    except Exception as e:
        logging.error(f"❌ Failed to send email: {e}")

def main(mytimer: func.TimerRequest) -> None:
    logging.info('Timer function triggered.')
    apartments = fetch_apartments()
    if apartments:
        logging.info(f"✔ Found {len(apartments)} matching units.")
        send_email(apartments)
    else:
        logging.info("❌ No matching apartments found.")
