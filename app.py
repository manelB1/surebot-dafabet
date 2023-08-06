import json
import os
from datetime import datetime
import pytz
from dateutil import parser
import requests
from flask import Flask
from flask import request, Response
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from playwright.sync_api import sync_playwright, Page
from playwright_stealth import stealth_sync


app = Flask(__name__)

user_dir = '/tmp/playwright'
if not os.path.exists(user_dir):
    os.makedirs(user_dir)

MARKETS = {
    "HANDICAP": "Handicap Asiático - Tempo Regular ",
    "TOTAL": "Match-bet and Totals -",
    "MONEY": "Vitória/Empate/Vitória",
    "HANDICAP_EURO": "Handicap Europeu - Tempo Regular ",
    "1x2": "Vitória/Empate/Vitória",
    "BOTH_TO_SCORE": "Vitória/Empate/Vitória",
    
}


def authenticate(authorization):
    data = {
        'username': authorization.get('username'),
        'password': authorization.get('password')
    }

    
    
    
    if (not authorization.get('validate') or not authorization.get('token')) or datetime.strptime(authorization.get('validate'), "%Y-%m-%dT%H:%M:%S") < datetime.now():
    
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


    
@app.route("/api/v1/bot/check_game/", methods=["POST"])
def start_bet():
    tip = json.loads(request.data)
    print(tip)

    success = False

    with sync_playwright() as p:
        data = {
            "payout": None,
            
        }

        home = tip.get('homeTeam')
        away = tip.get('awayTeam')
        stake = float(tip.get('stake'))  
        market = tip.get('market')
        market_type = tip.get('marketType')
        point = tip.get('point')
        
        game_url: str = tip.get('gameUrl')
        
        browser = p.chromium.launch(headless=False)
        
        page: Page = browser.new_page()
        stealth_sync(page)
        page.goto(game_url)
        page.set_default_timeout(60000)  

        page.wait_for_timeout(1000)

        page.locator('#market_group_all').click()

        if point is not None:
            translated_market = MARKETS.get(market)
            print(translated_market)
            if translated_market:
                titleMarkets = page.locator('.event_path-title.ellipsis').all()
                for element in titleMarkets:
                    textTitle = element.inner_text()
                    print(textTitle)
                    if translated_market == textTitle:
                        print("dsfdafddsf >>>>>>>>>")
                        element.click()

        formatted_price_elements = page.locator('span.formatted_price.price').all()
                       
        for elementPrice in formatted_price_elements:
            textPrice = elementPrice.inner_text()
            if textPrice == point:
                elementPrice.click()                
                                

        page.wait_for_timeout(2000)    

        inputValue = page.locator('input.stake')
        payout = page.locator('#betslip > div > div > div.rollup-content.betslip-content > section.betslip-selections > ul > li > div > h3 > ul > li.last.bet-input-container.text-md.border-btm-light > div.first > div > span > span')

        inputValue.fill(str(stake))  
        
        payout_value = float(payout.inner_text())
        data['payout'] = round(payout_value * stake)        

        page.wait_for_timeout(3000)

        titleEvent = page.locator('.event-header-description').inner_text()
        
        if home in titleEvent or away in titleEvent:
            success = True

        return Response(str(data["payout"]), status=200 if success else 400)





@app.route("/api/v1/bot/balance/", methods=["POST"])
def get_balance():
    
    
    authorization = json.loads(request.data).get('authorization')

    authorization = authenticate(authorization)
    coockiesData = authorization.get('coockies')
    headersData = authorization.get('headers')
    
    print(coockiesData)
    print(headersData)
    response_hash = authorization.get('hash')
    
   
    url = f"https://m.dafabet.com/pt/api/plugins/module/route/balance/balances?authenticated=true&hash={response_hash}"
    
    response = requests.get(url, headers=headersData, cookies=coockiesData)

    print(response.text)
    
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
    
