import json
import os
from datetime import datetime
import pytz
from dateutil import parser
import requests
from flask import Flask
from flask import request
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime


app = Flask(__name__)




def authenticate(authorization):
    data = {
        'username': authorization.get('username'),
        'password': authorization.get('password')
    }

    tokenUser = authorization.get('token')
    print(tokenUser)
    validateDate = parsedate_to_datetime(authorization.get('validate'))
    if not validateDate or validateDate < datetime.now(timezone.utc) or not authorization.get('token'):

        
        response = requests.post('https://m.dafabet.com/pt/api/plugins/component/route/header_login/authenticate?authenticated=true', json=data)
        
        if response.status_code <= 300:
            responseData = response.json()
            print("🚀 FUI NA CASA E ME AUTENTIQUEI:")
            print(responseData)

            cookies = response.cookies
            headers = response.headers
            
                
              
            token = responseData.get('token')
                
            playerId = responseData.get('user', {}).get('playerId')
            dateHeader = response.headers.get('Date')
            expiresHeader = response.headers.get('Expires')
            responseHash = responseData.get('hash')
            responseAuthenticate = responseData.get('authenticated')
            expiresHeader = datetime.now() + timedelta(minutes=30)

            authorization['headers'] = headers
            authorization['coockies'] = cookies
            authorization['date_header'] = dateHeader
            authorization['validate'] = expiresHeader
            authorization['token'] = token
            authorization['player_id'] = playerId
            authorization['hash'] = responseHash
            authorization['authenticated'] = responseAuthenticate

            return authorization
                
            
        else:
            return {       
                
                    response.status_code

                    }

  
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
    
# @app.route("/api/v1/bot/start_bet/", methods=["POST"])
# def start_bet():
    
#     aposta = {
#         'timea': 'TIME A', 
#         'timeb': 'TIME B',
#         'amount': 1000,
#         'date': '2023-06-02 15:00',
#         'event': '',
#         'page_title': '',
#     }
    

#     with sync_playwright() as p:
#         browser = p.chromium.launch()
#         page = browser.new_page()
        
#         page.goto("https://betway.com/pt/sports")
        
#         page.wait_for_timeout(3000)
        
#         page.goto("https://betway.com/pt/sports")
        
#         aposta['page_title'] = page.title()
        
#         page.wait_for_timeout(5000)
        
#         browser.close()
    
#     return aposta


@app.route("/api/v1/bot/balance/", methods=["POST"])
def get_balance():
    
    
    authorization = json.loads(request.data).get('authorization')

    authorization = authenticate(authorization)
    coockiesData = authorization.get('coockies')
    headersData = authorization.get('headers')
    
    response_hash = authorization.get('hash')
    
   
    url = f"https://m.dafabet.com/pt/api/plugins/module/route/balance/balances?authenticated=true&hash={response_hash}"
    
    response = requests.get(url, headers=headersData, cookies=coockiesData)

    
    if response.status_code <= 300:
        balance_data = response.json()
        balance = balance_data.get('balance')
        currency = balance_data.get('currency')       
        
    else:
        print(response.status_code)

    return {
        'balance': balance,
        'currency': currency,
        'hash': authorization.get('hash'),
        'authenticated': authorization.get('authenticated')
    }




@app.route("/api/v1/bot/check_authentication/", methods=["POST"])
def check_authentication():
    
    authorization = json.loads(request.data).get('authorization')

    authorization = authenticate(authorization)
    
    
    # validate = datetime.strptime(authorization.get('validate'), '%Y-%m-%dT%H:%M:%S.%f%z') if authorization.get('validate') else None
    
    # if not validate or (validate <= datetime.now()):
    return {
        
        'token': authorization.get('token'),
        'validate': authorization.get('validate'),
        'playerId': authorization.get('player_id'),
        'dateHeader': authorization.get('date_header'),
       
    }
    
