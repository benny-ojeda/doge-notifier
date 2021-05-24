import os
import requests
from twilio.rest import Client
import time
from keep_alive import keep_alive

keep_alive()

# Twilio session
account_sid = os.environ['account_sid']
auth_token = os.environ['auth_token']
client = Client(account_sid, auth_token)

pn = os.environ['pn']
tpn = os.environ['tpn']

initial_price = 0.38
change = 0.05

while True:
    time.sleep(5)
    print(f'Initial price: {initial_price}')
    # DOGE API price request
    response = requests.get('https://sochain.com//api/v2/get_price/DOGE/USD')
    if response.status_code == 200:
        content = response.json()
        current_price = float(content['data']['prices'][1]['price'][:4])
        print(f'Current price: {current_price}')
        if current_price >= (initial_price + change):
            # Twilio send msg
            client.api.account.messages.create(
            to=pn, 
            from_=tpn,
            body=f'DOGE up {change} cents: {current_price}')
            initial_price = current_price
        elif current_price <= (initial_price - change):
            # Twilio send msg
            client.api.account.messages.create(
            to=pn, 
            from_=tpn,
            body=f'DOGE down {change} cents: {current_price}')
            initial_price = current_price


