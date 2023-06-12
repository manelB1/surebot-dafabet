import json
import requests
from playwright.sync_api import sync_playwright
from flask import Flask
from flask import request
from datetime import datetime, timedelta


app = Flask(__name__)

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
    
@app.route("/api/v1/bot/check_authentication/", methods=["POST"])
def check_authentication():
    
    authorization = json.loads(request.data).get('authorization')
    
    validate = datetime.strptime(authorization.get('validate'), '%Y-%m-%dT%H:%M:%S.%f%z') if authorization.get('validate') else None
    
    if not validate or (validate <= datetime.now()):
  

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

            expires_header = datetime.now() + timedelta(minutes=30)

            print("Expire:", expires_header)
            print("Date", date_header)


            print(token)
            print(player_id)

            authorization['date_header'] = date_header
            authorization['validate'] = expires_header
            authorization['token'] = token
            authorization['player_id'] = player_id

        
            # authorization['token'] = data.get('sessionToken')
            # authorization['playerId'] = data.get('customerId')
            # authorization['validate'] = datetime.now() + timedelta(minutes=30)
            
            # TODO: Implementar código para ir no SUREBOT e atualizar os dados de token para o bot específico.
            
            return authorization
        
        else:
            print(response.status_code)

        return authorization