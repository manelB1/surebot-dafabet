import json
import requests
from playwright.sync_api import sync_playwright
from flask import Flask
from flask import request
from datetime import datetime, timedelta


app = Flask(__name__)

def authenticate(authorization):
    data = {
        'username': authorization.get('Username'),
        'password': authorization.get('Password'),
    }

    response = requests.post('https://m.dafabet.com/pt/api/plugins/component/route/header_login/authenticate?authenticated=true', json=data)

    if response.status_code <= 300:
        response_data = response.json()
        print("🚀 FUI NA CASA E ME AUTENTIQUEI:")
        print(response_data)

        token = response_data.get('token')
        player_id = response_data.get('user', {}).get('playerId')
        date_header = response.headers.get('Date')
        expires_header = response.headers.get('Expires')
        response_hash = response_data.get('hash')
        response_authenticate = response_data.get('authenticated')

        expires_header = datetime.now() + timedelta(minutes=30)

        print("Expire:", expires_header)
        print("Date", date_header)

        authorization['date_header'] = date_header
        authorization['validate'] = expires_header
        authorization['token'] = token
        authorization['player_id'] = player_id
        authorization['hash'] = response_hash
        authorization['authenticated'] = response_authenticate

        return authorization
    else:
        print(response.status_code)

    return {}  

def balance(authorization):

    token = authorization.get('token')
    response_hash = authorization.get('hash')
    response_authenticate = authorization.get('authenticated')

    params = {
    'authenticated': response_authenticate,
    'hash': response_hash,
}
    response = requests.get('https://m.dafabet.com/pt/api/plugins/module/route/balance/balances', params=params)

    if response.status_code == 200:
        balance_data = response.json()
        print(balance_data)
        response_balance = balance_data.get('balance')

        authorization['balance'] = response_balance

        return authorization

@app.route("/api/v1/bot/bets/")
def bets():
    
    return [
        {
            "amount": 19990,
        },
        {
            "amount": 89123849,
        },
        {
            "amount": 3,
        },
        {
            "amount": 90192,
        },
    ]
    
@app.route("/api/v1/bot/start_bet/", methods=["POST"])
def start_bet():
    
    aposta = {
        'timea': 'TIME A', 
        'timeb': 'TIME B',
        'amount': 1000,
        'date': '2023-06-02 15:00',
        'event': '',
        'page_title': '',
    }
    

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        page.goto("https://betway.com/pt/sports")
        
        page.wait_for_timeout(3000)
        
        page.goto("https://betway.com/pt/sports")
        
        aposta['page_title'] = page.title()
        
        page.wait_for_timeout(5000)
        
        browser.close()
    
    return aposta


@app.route("/api/v1/bot/get_balance/", methods=["POST"])
def get_balance():
    authorization = json.loads(request.data).get('authorization')

    authorization = balance(authorization)

    return authorization




@app.route("/api/v1/bot/check_authentication/", methods=["POST"])
def check_authentication():
    
    authorization = json.loads(request.data).get('authorization')

    authorization = authenticate(authorization)
    
    # validate = datetime.strptime(authorization.get('validate'), '%Y-%m-%dT%H:%M:%S.%f%z') if authorization.get('validate') else None
    
    # if not validate or (validate <= datetime.now()):
    return {
        
        'token': authorization.get('token'),
        'validate': authorization.get('validate'),
        'playerId': authorization.get('playerId'),
        'dateHeader': authorization.get('date_header'),
        'hash': authorization.get('hash'),
        'authenticated': authorization.get('authenticated')
    }
    
