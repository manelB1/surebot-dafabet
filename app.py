import json
import requests
from playwright.sync_api import sync_playwright
from flask import Flask
from flask import request
from datetime import datetime, timedelta

requests.packages.urllib3.disable_warnings()


app = Flask(__name__)

def authenticate(authorization):
    data = {
        'username': authorization.get('Username'),
        'password': authorization.get('Password'),
        'is_login': authorization.get('is_login')
    }

    response = requests.post('https://m.dafabet.com/pt/api/plugins/component/route/header_login/authenticate?authenticated=true', json=data)
    get_atribute = []

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

       

        authorization['date_header'] = date_header
        authorization['validate'] = expires_header
        authorization['token'] = token
        authorization['player_id'] = player_id
        authorization['hash'] = response_hash
        authorization['authenticated'] = response_authenticate

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

    authorization = authenticate(authorization)
    
    response_authenticate = authorization.get('authenticated')
    response_hash = authorization.get('hash')
    
    


    headers = {
    'ADRUM': 'isAjax:true',
    'Accept': 'application/json, text/javascript',
    'Accept-Language': 'pt-BR,pt',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Cookie': 'mhlanguage=pt; gtm-username=BrManuca; gtm-userid=22469859; gtm-currency=BRL; PHPSESSID=16g4utkf0otnghr21mi9fr94ku; extCurrency=BRL; wbcToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IkJyTWFudWNhIiwicGxheWVySWQiOjIyNDY5ODU5LCJzZXNzaW9uVG9rZW4iOiJjZDcxYWIzZS0xNWI4LTQ0YjQtOWYyYy04NWE3OTczN2MzYjciLCJpc3MiOiJ3ZWJjb21wb3NlciIsImF1ZCI6IndlYmNvbXBvc2VyIiwiZXhwIjoxNjg2Nzc4NDYwfQ.eSuxeGHIXhQVVN72jhgl4Jj93JWzuZ-HCK60jVYp_-U; extToken=eyJhbGlhcyI6ImRhZmFiZXQuY29tIiwiYWxnIjoiUlNBLU9BRVAiLCJlbmMiOiJBMjU2R0NNIn0.XTV1O7Ywt_cAT8Bt_r-WPMN1cuRCDELH2UhZVsVNQbmifO0uZd8mJlXXhJx9I2mKRZBYQGPBnfF4Zs8KesnoHQdZOuNOSCQhYF4ZE4F1IYLtRYCgohuKiJXu521Pbu_-RiaDDJe_b_iYIBHuk7EogZ_n7jt80oiQNNuEwm7RzeUELfoPt-4r3CAd5aBwnHyLU2m1RbpXDWFH_0afBudeslvcqIisAH9KqP4ITF1F5plNnvGcw334MnWwdMLy0NvO_BHwAJnLkDs1KkoSl8J_clm_76160EiF5vtxS0qkgNxSfvmxj2Uur1j3FhKrFvcfEamiibHic3hTgeHdLbaBxA.z-6h45Joala17y4Z.xayAA2ueljaxvxSZ-zNG6ltwiTDojdqrmsUX0Ezh2tuRm0I2mvJOC9N76UiAcqDmFYppeEWkJ4F9dqP3OSxmUgV03q9Wn3TOHQ5qkpFwTjMbrJxxm8dxtn1IQ4UnwafTDMWQtrJjDbyqqSJxiTkV1q3EO147WdAXvJXBtpSwVQ2SOMWmMsABRa-YWIzJS0x7zX5WjnTSEibWoUQBkoV-HWhW18UXDq0NAM7IgUn_486bBXiba82I-syYrKJve9n5HWAar4DlkQvSNPRTKhYGHnsJ2ZJD2bxPcMGhHdxSLY1sAfFJBB_wA3Gly2xnk7Rtlu7-vlKTfysz.1fLvmOK6rbuSUsqnz6yBIw; username=BrManuca; ga_userid=BrManuca; ga_sessionid=1686692426033.xn0ca7a; frosmo_quickContext=%7B%22VERSION%22%3A%221.1.0%22%2C%22UID%22%3A%225q09eo.liulfxzv%22%2C%22origin%22%3A%22m_dafabet_com%22%2C%22lastDisplayTime%22%3A%7B%223111%22%3A1686692426%7D%2C%22lastRevisionId%22%3A%7B%223111%22%3A1%7D%2C%22lastPageView%22%3A%7B%22time%22%3A1686692426435%7D%2C%22states%22%3A%7B%22session%22%3A%7B%7D%7D%7D; ADRUM=s=1686692722397&r=https%3A%2F%2Fm.dafabet.com%2Fpt%3F0',
    'Referer': 'https://m.dafabet.com/pt',
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

    
    
    
    url = 'https://m.dafabet.com/pt/api/plugins/module/route/balance/balances?authenticated={}&hash={}'.format(response_authenticate, response_hash)
    print(url)
    response = requests.get(url)

    
    if response.status_code <= 300:
        balance_data = response.json()
        print(balance_data)
        balance = balance_data.get('balance')
        
    else:
        print(response.status_code)

    return {
        'balance': authorization.get('balance'),
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
    
