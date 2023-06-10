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
    
    # validate = datetime.strptime(authorization.get('validate'), '%Y-%m-%dT%H:%M:%S.%f%z') if authorization.get('validate') else None
    
    # if not validate or (validate <= datetime.now()):
    cookies = {
        'mhlanguage': 'pt',
        'ADRUM': 's=1686332899621&r=https%3A%2F%2Fm.dafabet.com%2Fpt%2Fpromotions%2Fdf-first-deposit-bonus%3F0',
        'gtm-username': 'BrManuca',
        'gtm-userid': '22469859',
        'gtm-currency': 'BRL',
        'frosmo_quickContext': '%7B%22VERSION%22%3A%221.1.0%22%2C%22UID%22%3A%225q09eo.liov1wny%22%2C%22origin%22%3A%22m_dafabet_com%22%2C%22lastDisplayTime%22%3A%7B%223111%22%3A1686333237%7D%2C%22lastRevisionId%22%3A%7B%223111%22%3A1%7D%2C%22lastPageView%22%3A%7B%22time%22%3A1686332903892%7D%2C%22states%22%3A%7B%22session%22%3A%7B%7D%7D%7D',
        'ga_userid': 'BrManuca',
        'ga_sessionid': '1686334852006.8a7dxlg',
        'PHPSESSID': 'mo53va14nsfoho558fh41kr4g5',
        'ADRUM_BT': 'R%3A58%7Cg%3A08597763-c471-48c0-a96e-3368ef25d5109547%7Cn%3Acustomer1_49a8be7d-1247-453d-8b9d-eefa04fc150a%7Ci%3A8579%7Cd%3A91%7Ce%3A86',
    }

    headers = {
        'Accept': 'application/json, text/javascript',
        'Accept-Language': 'pt-BR,pt;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Cookie': 'mhlanguage=pt; ADRUM=s=1686332899621&r=https%3A%2F%2Fm.dafabet.com%2Fpt%2Fpromotions%2Fdf-first-deposit-bonus%3F0; gtm-username=BrManuca; gtm-userid=22469859; gtm-currency=BRL; frosmo_quickContext=%7B%22VERSION%22%3A%221.1.0%22%2C%22UID%22%3A%225q09eo.liov1wny%22%2C%22origin%22%3A%22m_dafabet_com%22%2C%22lastDisplayTime%22%3A%7B%223111%22%3A1686333237%7D%2C%22lastRevisionId%22%3A%7B%223111%22%3A1%7D%2C%22lastPageView%22%3A%7B%22time%22%3A1686332903892%7D%2C%22states%22%3A%7B%22session%22%3A%7B%7D%7D%7D; ga_userid=BrManuca; ga_sessionid=1686334852006.8a7dxlg; PHPSESSID=mo53va14nsfoho558fh41kr4g5; ADRUM_BT=R%3A58%7Cg%3A08597763-c471-48c0-a96e-3368ef25d5109547%7Cn%3Acustomer1_49a8be7d-1247-453d-8b9d-eefa04fc150a%7Ci%3A8579%7Cd%3A91%7Ce%3A86',
        'Origin': 'https://m.dafabet.com',
        'Referer': 'https://m.dafabet.com/pt/promotions/df-first-deposit-bonus',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Brave";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'authenticated': authorization.get('authenticated'),
    }

    data = {
        'username': authorization.get('Username'),
        'password': authorization.get('Password'),
    }

    response = requests.post('https://m.dafabet.com/pt/api/plugins/component/route/header_login/authenticate?authenticated=false', cookies=cookies, headers=headers, json=data)
    responsee_data = response.text
    print(responsee_data)
    
    if response.status_code <= 300:
        response_data = response.text      
        print("🚀 FUI NA CASA E ME AUTENTIQUEI:", response_data)

        
       
        # authorization['token'] = data.get('sessionToken')
        # authorization['playerId'] = data.get('customerId')
        # authorization['validate'] = datetime.now() + timedelta(minutes=30)
        
        # TODO: Implementar código para ir no SUREBOT e atualizar os dados de token para o bot específico.
        
        return authorization
    
    else:
        print(response.status_code)

    return authorization