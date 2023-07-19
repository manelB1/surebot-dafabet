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


  
@app.route("/api/v1/bot/sports/", methods=["POST"])
def sports():
    

    cookies = {
    'mhlanguage': 'pt',
    'gtm-currency': 'BRL',
    'dafaUrl[mobileUrl]': 'https%3A%2F%2Fm.dafabet.com%2Fpt',
    'dafaUrl[login]': 'https%3A%2F%2Fm.dafabet.com%2Fpt%2Flogin%3Fproduct%3Dsports-df',
    'dafaUrl[logout]': 'https%3A%2F%2Fm.dafabet.com%2Fpt%2Flogout',
    'dafaUrl[registration]': 'https%3A%2F%2Fwww.dafabet.com%2Fpt%2Fjoin%2Fsports-df%3Fregvia%3D26',
    'dafaUrl[desktopUrl]': 'https%3A%2F%2Fwww.dafabet.com%2Fpt',
    'visid_incap_2519778': 'boSm49ZeR5aBs3eQwdaLQ3V4tWQAAAAAQUIPAAAAAADTVXQdjbCjhVzNp+xvDqck',
    'nlbi_2519778': 'OzizHbAHnmy5vO5DzdO2rAAAAAA5Rk326avoGORd7MjZyLhN',
    'betslip_menu': 'single',
    'user_accept_higher_odds': 'true',
    'site_version': 'web',
    'X_DEVICE_VIEW': 'desktop',
    'visid_incap_2267509': 'Kaq2K6BuTIOOYpPfERqvBgF7tWQAAAAAQUIPAAAAAACmJ2qO50qsrqE3JAi/GlQJ',
    'incap_ses_1354_2267509': 'penhKn4iAQUYqYsal2DKEgF7tWQAAAAAvZfBub30hp2VdLaxF5q96w==',
    'currency': 'BRL',
    'PHPSESSID': '0rr54kemusacgkrhsahd5o94gr',
    'extCurrency': 'BRL',
    'wbcToken': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFmdGVyYmV0IiwicGxheWVySWQiOjIyNjQyMzEyLCJzZXNzaW9uVG9rZW4iOiJhMjFlZDYzMS0yODYzLTQ2NjUtODZkOC0xNWMwNjY2OWJhNDgiLCJpc3MiOiJ3ZWJjb21wb3NlciIsImF1ZCI6IndlYmNvbXBvc2VyIiwiZXhwIjoxNjg5NzAzMDczfQ.TynqWxZtL3lYtnHXAuA_VckHGDUJ6FdLDC4RZd8iRjY',
    'extToken': 'eyJhbGlhcyI6ImRhZmFiZXQuY29tIiwiYWxnIjoiUlNBLU9BRVAiLCJlbmMiOiJBMjU2R0NNIn0.REZKEvj7r4Hp3pTtxQ14-5Mc-qbc-Hk57aUl8t3eQJJLGzn6zt_h8WNgYZRS42Hzv01IhQELPPBfhG-0Itc3FQxpCX4GL_6F2NFJf1GU66DbQfNIwDn6sDddsxOFhp8HhAr152olT8FA0wDmQedXkeAC9BPc3aCeK8K28XfZDOw9orGVasMtGr1hqmBYngh2FOuioFnSxMDS8f7gGl9BZlWDcZb7XPDo4BMrWUJyUPgmC0HL52UOsQrcPq2r854H5KH-bBqG6GyogYK946bUj3R1CqUFopkkMvIC6qQqHkC7efZKN7dQT9xxL9ImSBAIN5lQHEVgWDYC5lUSO67ZrQ.e7H4GgY7-qg9Cqy1.9b8EksSj6NUtasD0WBDaKsmBJHVEibWOpbjlwiSFfxDeWZgIzqLZdEOUqWNkaaEFrYQJEfSUJ_SNHfG7_DeAPSglMQDIfAKAeiN1b3xRbAH36Jvn0Xaq44Ni5xeoshYx4Qh69ahD7afsslGLXDX_M4MVNdsIPXqH5fKsQ0Pn9Mm7e9mJc8O1eqL8OxfZP4dCEdE5dRf8HP-ybjzTK7sQlxt4MSiOXy7aL82KfU1MQO1xy3bhLodDdaeNvOEwRbICpp1znPeQAJRnVYA69qHGqxVnoAKlzimjtFKpohAV_9vMV4FVfvRgNIfFGECJiniYkSG0cBiSbCzC.r31GK9zkPl3AHgWptW6Ctg',
    'gtm-username': 'afterbet',
    'gtm-userid': '22642312',
    'dafaUrl[cashierDeposit]': 'https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%2Falsports%2Ftransaction%2Fdeposit%3Fticket%3Da21ed631-2863-4665-86d8-15c06669ba48',
    'dafaUrl[cashierTransfer]': 'https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%2Falsports%2Ftransaction%2Ftransfer%3Fticket%3Da21ed631-2863-4665-86d8-15c06669ba48',
    'dafaUrl[cashierCashPoints]': 'https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%2Falsports%2Ftransaction%2Fcashpoints%3Fticket%3Da21ed631-2863-4665-86d8-15c06669ba48',
    'dafaUrl[cashierWithdrawal]': 'https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%2Falsports%2Ftransaction%2Fwithdrawal%3Fticket%3Da21ed631-2863-4665-86d8-15c06669ba48',
    'dafaUrl[cashier]': 'https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%3Fticket%3Da21ed631-2863-4665-86d8-15c06669ba48',
    'ADRUM': 's=1689616679465&r=https%3A%2F%2Fm.dafabet.com%2Fpt%3F0',
    'previous_username': 'afterbet',
    'incap_ses_1354_2519778': 'mJwgfZ9quz5emZYal2DKEryJtWQAAAAAIMxln0ZC9kGfioCaRuCKUA==',
    '_session': 'WW50SnY5ejU5Nm1xVmxla1BpZ0lsa1duN1hVNXNTVG1hSDBVUFJSYmNORzNGWHZZTEtQWTlNVjIwV0ZudWU1RUNJNEFRTmp2QllndW53S1dEVVM1cGlSdUJuS09Ka3lFbHpQSjVkR1N6TWNlMzZseUcrSUVidVBxeHBnVHFtOGlVMHNreWZ0N0RxMlRPZHM0L215cURMWER3Q2toWWFNa0kyNFZSY1c1OEdYdG8rdGtzREs1TXR6MForZ29sUjZkMGg5V0gwbEVGMGdVSkRGUEpzaGNwdVNLOTdSUU1HZFJlUUFjT001RmJ1aGJ4YVpRd1VzTkN1TXMwcnBXQ3pqTy9xK2JSbktIYVNyLzNlLzE0MERnRDF4SGdXT1I0ZnIrUlVyV1pGVGRZUTNlYWFJbElsblZnY1l1VVA1Q25SSjlOd2MvSG1xYWRsZjdNbUtSd2hHcTVzNVgyUHBHMHdLbGR6dHZPY3JBTzdGa1NwMEhYY25jeENnY1M5a3JoOTZrL0Q1S3ptVTVzT28rMHQvUDlOSDgzZFg5dllNOEw5RUFYeFBQNmpIUkZrOHZ5T0Q5YnNsWk5ESTY3NGpXeUtNeDZhdUppSnFybDlIV0JxdnJFWU93S0swWGYrY3lxUUFCZG12VDhzSW54T3k1TUNUQjhkd29QM0MvOFAzdkdrY1NPeUVuZDZLS2t5NHJVNUtta3U5SHVSSE5WODZEVFU1WWxIdEFpUVlSRlNwNnhCUllNK2tXNmI1b29rYVJhNTZKWkp6UUdGRHhqcG1LRzI0cGQvLzl5R1NtQkkvVG51V3cyaDVRZHNvZHNmdW1KRlA0Zkk5VCtwZFFMK0xWVWIwZDcybmljSGVUZ3FSNk9kZDJsMHhoQlF5ZWtsV0hHZGY3VVNDZ3M5MFh0WnVNd0hJQVVNTEZUYzhrQmtCWHh5c0pMSitZWWtTMmpIbThZeGxjRnphT3hCVTc5WVlHLzV0VHBJY2V6T1JXVDNOekN2YlM1cEpNa29UTk96eGpwSWFRLS1YMWR0aTFUNVNCdWlLSE1yeVlsSjJnPT0%3D--538d7303cb62eb201e9acce3620d11f4bbe177f4',
    'nlbi_2519778_2147483392': 'Kg4LZqBWZkzGJ8upzdO2rAAAAAAEY772V7s5AAaMMgVBlSym',
    'reese84': '3:i5SAPo6ELlzNOBI/RZjPWg==:OmQIw4dbGNAa/RZvJqOJ/DBWteyvrjK8X92MIVJmUOXF5iLjGRoO2ympFprZ008Ll+rl9j/OAY5BoIRvqebxIzUplRKKkd+COMEeCJG+XP6Wd+DS096peBUZXX+YDF066+J42oufsGImQiy/sMFMFFkuEYtcPazl0iGv4sLrQOIhwHslXMQzsGcQXPDT95CBhv/YJfafW03IllP7VWZ6C2WRPTFqT1BrzgRqt0/X2rPVZsYbF1jzcxfo67iBUbBBvi56h4hyg58NhvS5bcY0nR6abgpB/tYsRvTgVi7WFIpYDejX9xwl8KJ9LrskGqaCyEmVRemFs98M/9wwsd8ZpJTnMdi7ug/ZvElOuHFQSyFHcKfxmZU8SKIwb3Ao7DpRFIRfhavTlO8HtjNMQmRLTBgY78rjQQRAKSh5775vGOkr4dpyhhsFa2HeTpkpuw1JcsEi6btKknG1iYmJWOo7LhJ7qoBEn08brRvmssE32/g=:y/NBXs+K0I5mG0OlAgEnc8kkCBQuTaqrV01Pvf6svls=',
}

    headers = {
    'authority': 'als.dafabet.com',
    'accept': 'application/json',
    'accept-language': 'pt-BR',
    # 'cookie': 'mhlanguage=pt; gtm-currency=BRL; dafaUrl[mobileUrl]=https%3A%2F%2Fm.dafabet.com%2Fpt; dafaUrl[login]=https%3A%2F%2Fm.dafabet.com%2Fpt%2Flogin%3Fproduct%3Dsports-df; dafaUrl[logout]=https%3A%2F%2Fm.dafabet.com%2Fpt%2Flogout; dafaUrl[registration]=https%3A%2F%2Fwww.dafabet.com%2Fpt%2Fjoin%2Fsports-df%3Fregvia%3D26; dafaUrl[desktopUrl]=https%3A%2F%2Fwww.dafabet.com%2Fpt; visid_incap_2519778=boSm49ZeR5aBs3eQwdaLQ3V4tWQAAAAAQUIPAAAAAADTVXQdjbCjhVzNp+xvDqck; nlbi_2519778=OzizHbAHnmy5vO5DzdO2rAAAAAA5Rk326avoGORd7MjZyLhN; betslip_menu=single; user_accept_higher_odds=true; site_version=web; X_DEVICE_VIEW=desktop; visid_incap_2267509=Kaq2K6BuTIOOYpPfERqvBgF7tWQAAAAAQUIPAAAAAACmJ2qO50qsrqE3JAi/GlQJ; incap_ses_1354_2267509=penhKn4iAQUYqYsal2DKEgF7tWQAAAAAvZfBub30hp2VdLaxF5q96w==; currency=BRL; PHPSESSID=0rr54kemusacgkrhsahd5o94gr; extCurrency=BRL; wbcToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFmdGVyYmV0IiwicGxheWVySWQiOjIyNjQyMzEyLCJzZXNzaW9uVG9rZW4iOiJhMjFlZDYzMS0yODYzLTQ2NjUtODZkOC0xNWMwNjY2OWJhNDgiLCJpc3MiOiJ3ZWJjb21wb3NlciIsImF1ZCI6IndlYmNvbXBvc2VyIiwiZXhwIjoxNjg5NzAzMDczfQ.TynqWxZtL3lYtnHXAuA_VckHGDUJ6FdLDC4RZd8iRjY; extToken=eyJhbGlhcyI6ImRhZmFiZXQuY29tIiwiYWxnIjoiUlNBLU9BRVAiLCJlbmMiOiJBMjU2R0NNIn0.REZKEvj7r4Hp3pTtxQ14-5Mc-qbc-Hk57aUl8t3eQJJLGzn6zt_h8WNgYZRS42Hzv01IhQELPPBfhG-0Itc3FQxpCX4GL_6F2NFJf1GU66DbQfNIwDn6sDddsxOFhp8HhAr152olT8FA0wDmQedXkeAC9BPc3aCeK8K28XfZDOw9orGVasMtGr1hqmBYngh2FOuioFnSxMDS8f7gGl9BZlWDcZb7XPDo4BMrWUJyUPgmC0HL52UOsQrcPq2r854H5KH-bBqG6GyogYK946bUj3R1CqUFopkkMvIC6qQqHkC7efZKN7dQT9xxL9ImSBAIN5lQHEVgWDYC5lUSO67ZrQ.e7H4GgY7-qg9Cqy1.9b8EksSj6NUtasD0WBDaKsmBJHVEibWOpbjlwiSFfxDeWZgIzqLZdEOUqWNkaaEFrYQJEfSUJ_SNHfG7_DeAPSglMQDIfAKAeiN1b3xRbAH36Jvn0Xaq44Ni5xeoshYx4Qh69ahD7afsslGLXDX_M4MVNdsIPXqH5fKsQ0Pn9Mm7e9mJc8O1eqL8OxfZP4dCEdE5dRf8HP-ybjzTK7sQlxt4MSiOXy7aL82KfU1MQO1xy3bhLodDdaeNvOEwRbICpp1znPeQAJRnVYA69qHGqxVnoAKlzimjtFKpohAV_9vMV4FVfvRgNIfFGECJiniYkSG0cBiSbCzC.r31GK9zkPl3AHgWptW6Ctg; gtm-username=afterbet; gtm-userid=22642312; dafaUrl[cashierDeposit]=https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%2Falsports%2Ftransaction%2Fdeposit%3Fticket%3Da21ed631-2863-4665-86d8-15c06669ba48; dafaUrl[cashierTransfer]=https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%2Falsports%2Ftransaction%2Ftransfer%3Fticket%3Da21ed631-2863-4665-86d8-15c06669ba48; dafaUrl[cashierCashPoints]=https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%2Falsports%2Ftransaction%2Fcashpoints%3Fticket%3Da21ed631-2863-4665-86d8-15c06669ba48; dafaUrl[cashierWithdrawal]=https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%2Falsports%2Ftransaction%2Fwithdrawal%3Fticket%3Da21ed631-2863-4665-86d8-15c06669ba48; dafaUrl[cashier]=https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%3Fticket%3Da21ed631-2863-4665-86d8-15c06669ba48; ADRUM=s=1689616679465&r=https%3A%2F%2Fm.dafabet.com%2Fpt%3F0; previous_username=afterbet; incap_ses_1354_2519778=mJwgfZ9quz5emZYal2DKEryJtWQAAAAAIMxln0ZC9kGfioCaRuCKUA==; _session=WW50SnY5ejU5Nm1xVmxla1BpZ0lsa1duN1hVNXNTVG1hSDBVUFJSYmNORzNGWHZZTEtQWTlNVjIwV0ZudWU1RUNJNEFRTmp2QllndW53S1dEVVM1cGlSdUJuS09Ka3lFbHpQSjVkR1N6TWNlMzZseUcrSUVidVBxeHBnVHFtOGlVMHNreWZ0N0RxMlRPZHM0L215cURMWER3Q2toWWFNa0kyNFZSY1c1OEdYdG8rdGtzREs1TXR6MForZ29sUjZkMGg5V0gwbEVGMGdVSkRGUEpzaGNwdVNLOTdSUU1HZFJlUUFjT001RmJ1aGJ4YVpRd1VzTkN1TXMwcnBXQ3pqTy9xK2JSbktIYVNyLzNlLzE0MERnRDF4SGdXT1I0ZnIrUlVyV1pGVGRZUTNlYWFJbElsblZnY1l1VVA1Q25SSjlOd2MvSG1xYWRsZjdNbUtSd2hHcTVzNVgyUHBHMHdLbGR6dHZPY3JBTzdGa1NwMEhYY25jeENnY1M5a3JoOTZrL0Q1S3ptVTVzT28rMHQvUDlOSDgzZFg5dllNOEw5RUFYeFBQNmpIUkZrOHZ5T0Q5YnNsWk5ESTY3NGpXeUtNeDZhdUppSnFybDlIV0JxdnJFWU93S0swWGYrY3lxUUFCZG12VDhzSW54T3k1TUNUQjhkd29QM0MvOFAzdkdrY1NPeUVuZDZLS2t5NHJVNUtta3U5SHVSSE5WODZEVFU1WWxIdEFpUVlSRlNwNnhCUllNK2tXNmI1b29rYVJhNTZKWkp6UUdGRHhqcG1LRzI0cGQvLzl5R1NtQkkvVG51V3cyaDVRZHNvZHNmdW1KRlA0Zkk5VCtwZFFMK0xWVWIwZDcybmljSGVUZ3FSNk9kZDJsMHhoQlF5ZWtsV0hHZGY3VVNDZ3M5MFh0WnVNd0hJQVVNTEZUYzhrQmtCWHh5c0pMSitZWWtTMmpIbThZeGxjRnphT3hCVTc5WVlHLzV0VHBJY2V6T1JXVDNOekN2YlM1cEpNa29UTk96eGpwSWFRLS1YMWR0aTFUNVNCdWlLSE1yeVlsSjJnPT0%3D--538d7303cb62eb201e9acce3620d11f4bbe177f4; nlbi_2519778_2147483392=Kg4LZqBWZkzGJ8upzdO2rAAAAAAEY772V7s5AAaMMgVBlSym; reese84=3:i5SAPo6ELlzNOBI/RZjPWg==:OmQIw4dbGNAa/RZvJqOJ/DBWteyvrjK8X92MIVJmUOXF5iLjGRoO2ympFprZ008Ll+rl9j/OAY5BoIRvqebxIzUplRKKkd+COMEeCJG+XP6Wd+DS096peBUZXX+YDF066+J42oufsGImQiy/sMFMFFkuEYtcPazl0iGv4sLrQOIhwHslXMQzsGcQXPDT95CBhv/YJfafW03IllP7VWZ6C2WRPTFqT1BrzgRqt0/X2rPVZsYbF1jzcxfo67iBUbBBvi56h4hyg58NhvS5bcY0nR6abgpB/tYsRvTgVi7WFIpYDejX9xwl8KJ9LrskGqaCyEmVRemFs98M/9wwsd8ZpJTnMdi7ug/ZvElOuHFQSyFHcKfxmZU8SKIwb3Ao7DpRFIRfhavTlO8HtjNMQmRLTBgY78rjQQRAKSh5775vGOkr4dpyhhsFa2HeTpkpuw1JcsEi6btKknG1iYmJWOo7LhJ7qoBEn08brRvmssE32/g=:y/NBXs+K0I5mG0OlAgEnc8kkCBQuTaqrV01Pvf6svls=',
    'if-none-match': '"-293116691"',
    'referer': 'https://als.dafabet.com/proxy?master=www.dafabet.com?bv=169.1.1',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Brave";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'x-accept-language': 'pt-BR',
    'x-custom-lb-geoip-country': 'BR',
    'x-lvs-hstoken': 'J6wlh8uDphieDzTTY6vsNNxO2YWAcCY-G0y5nmE2nfD6sbItrNyoKYiZ8tZTSgDnyYph5oJN7LfqU1vaS1owbkNbnG863PCqxsKNcYC0n5jIE_-9gfwZKv64pAB3nGUG',
    'x-requested-with': 'XMLHttpRequest',
    'x-sb-brand': 'DAFABET',
    'x-sb-origin': 'WEB',
    'x-sb-portalid': '22',
}

    params = {
    'marketStatuses': 'OPEN,SUSPENDED',
    'includeAboutToStart': 'true',
    'excludeLongTermSuspended': 'true',
    'allBettableEvents': 'true',
    'lightWeightResponse': 'false',
    'sportGroups': 'REGULAR',
    'maxMarketsPerEvent': '0',
    'l': 'pt',
}

    response = requests.get('https://als.dafabet.com/xapi/rest/live/events', params=params, cookies=cookies, headers=headers)
    if response.status_code <= 300:
        responseData = response.json()
        print(responseData)

    else: {
         "error": response.status_code
    }   
         
    return {
        "sports": responseData
    }

  
@app.route("/api/v1/bot/check_bets/", methods=["POST"])
def bets():

    authorization = json.loads(request.data).get('authorization')

    authorization = authenticate(authorization)
    response_hash = authorization.get('hash')
   
    print(response_hash)

    cookies = {
        'mhlanguage': 'pt',
        'gtm-currency': 'BRL',
        'dafaUrl[mobileUrl]': 'https%3A%2F%2Fm.dafabet.com%2Fpt',
        'dafaUrl[login]': 'https%3A%2F%2Fm.dafabet.com%2Fpt%2Flogin%3Fproduct%3Dsports-df',
        'dafaUrl[logout]': 'https%3A%2F%2Fm.dafabet.com%2Fpt%2Flogout',
        'dafaUrl[registration]': 'https%3A%2F%2Fwww.dafabet.com%2Fpt%2Fjoin%2Fsports-df%3Fregvia%3D26',
        'dafaUrl[desktopUrl]': 'https%3A%2F%2Fwww.dafabet.com%2Fpt',
        'visid_incap_2519778': 'boSm49ZeR5aBs3eQwdaLQ3V4tWQAAAAAQUIPAAAAAADTVXQdjbCjhVzNp+xvDqck',
        'incap_ses_1354_2519778': 'GbPPVLfciVDf0okal2DKEnV4tWQAAAAAHAWGNiSeAexS0+ocbF/egw==',
        'reese84': '3:S4e6QYFYYOCRsqzfH4SDSA==:50UJpCZrFKTZ6+Ap5yLU2Km3ul7UsCRpZTPixnmYzXVSfmMFsgXl5Q1k92d3xZGPNfd5Nc274FfEwTbT3dA3TPNE4WPNMeO3smk4IaLkedqISIAaA77Q3M80e9PUYNUWkMAPxjg6+to9D1wU5LqWwezL2sH/TRIGjBAIU2iuvRHEzj4hR//TGkft5jfnUFAJ9CKWqs0RIFbDo0QfYZiXAZWnHzrc/Pnaiu94Zjc2WNylqDVA81Q/hrwuFeRvg4kfyhAkokjjSCYdzQgltahAgsbeQ4lhBaK0H0ChUl0PsGMCQ7+ZoRuEsk72t/cYKfWxannHsLuUqx1B4vIAS/mTOCfe3Cf3a+8gIEr1I5+5OH5htA0qz0DIcM4tL9yBMzJMgl2lUJvjR0GpdJ1KYziVmD+Ibpcrs+5e+VnKMs6uKSLxiFDzp2syaOF4GK2Webu6JhXHDw4JPXckJZLmfXNNtmOlxLCteSzLbueOzTMtqy4=:zEfjqHbjoJP1bz2cKyFJg5DU7ZjjhjMYWeAH5BVnAwI=',
        'nlbi_2519778': 'OzizHbAHnmy5vO5DzdO2rAAAAAA5Rk326avoGORd7MjZyLhN',
        'betslip_menu': 'single',
        'user_accept_higher_odds': 'true',
        'site_version': 'web',
        'PHPSESSID': '3ten3ul1oe3q7ql22rc5qevok3',
        'wbcToken': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IkJyTWFudWNhIiwicGxheWVySWQiOjIyNDY5ODU5LCJzZXNzaW9uVG9rZW4iOiJkNGZjMjYzYy0zZTgxLTRjNWYtODk3YS0wM2M2ZmE0ZGE4Y2IiLCJpc3MiOiJ3ZWJjb21wb3NlciIsImF1ZCI6IndlYmNvbXBvc2VyIiwiZXhwIjoxNjg5NzAwOTY5fQ.Xj7aleotHufmHkpQyuRrMXBpHJJTPnk_RI-R50YBDYw',
        'gtm-username': 'BrManuca',
        'gtm-userid': '22469859',
        'dafaUrl[cashierDeposit]': 'https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%2Falsports%2Ftransaction%2Fdeposit%3Fticket%3Dd4fc263c-3e81-4c5f-897a-03c6fa4da8cb',
        'dafaUrl[cashierTransfer]': 'https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%2Falsports%2Ftransaction%2Ftransfer%3Fticket%3Dd4fc263c-3e81-4c5f-897a-03c6fa4da8cb',
        'dafaUrl[cashierCashPoints]': 'https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%2Falsports%2Ftransaction%2Fcashpoints%3Fticket%3Dd4fc263c-3e81-4c5f-897a-03c6fa4da8cb',
        'dafaUrl[cashierWithdrawal]': 'https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%2Falsports%2Ftransaction%2Fwithdrawal%3Fticket%3Dd4fc263c-3e81-4c5f-897a-03c6fa4da8cb',
        'dafaUrl[cashier]': 'https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%3Fticket%3Dd4fc263c-3e81-4c5f-897a-03c6fa4da8cb',
        'nlbi_2519778_2147483392': '+hOvF9ENQl1+7NmdzdO2rAAAAABZqSMXkOPIQdV9GvtMzVKN',
        'previous_username': 'brmanuca',
        'X_DEVICE_VIEW': 'desktop',
        'visid_incap_2267509': 'Kaq2K6BuTIOOYpPfERqvBgF7tWQAAAAAQUIPAAAAAACmJ2qO50qsrqE3JAi/GlQJ',
        'incap_ses_1354_2267509': 'penhKn4iAQUYqYsal2DKEgF7tWQAAAAAvZfBub30hp2VdLaxF5q96w==',
        'currency': 'BRL',
        'ADRUM': 's=1689615503752&r=https%3A%2F%2Fwww.dafabet.com%2Fpt%2F%3F601935764',
        '_session': 'SXpoY2xmWVNnZWZ5RE80VWJCejYyczFZcXFxclMyWGNva1EyOWxlRzRQalFNNmY2V3luaFJyc3FGazluckgxMjVpRHllVi9WZ2tLRThiMW93bHRtcUd1RUJBOHJJeGlEN3U2aVpjMVpKWmZvcUF5Z0VLNVYxNE5DbjBwbTh2ZFZ3VXE4cWxxd3MwVWx2N0pEU0dVQTl5VTErZ0JiQkJjWC9VekpPUG1lSTY5cGw1QU9tS2FuUk1uWU5LY1VQbFNneDZueHJiSkRPKzZmMW1RbTlsWkJUWFBYS2lxK0ladHVyUC9KMXRrQmFxNElaYnNCYWszbUJpWkk2YkY5RTR5c0drcW8rUUhnUzNOMUhyNmJTRnZYVEpYejZXMi9FV1RxSmNwTDFjOHhnQWxxZmM3aVNpR2hmM0JpUmlOSGVnL2pKbHp3d0lFV01JNDRWSzZFcUhXRGNWM2JxSWlKT0FpRU1tNy9yNTlFdGlDRW5pOUtOTmhsWUtqcS92YmIyY1JiZkpWNWpIbWlBZWJzR281dklRS1BycFRRMkZnSDZQUWxtRkk1R1ZTeEs4ZDBLdVg2ZEFWRXg3b3ozdVZtZWsvMDVrTGtHTGZjUkIxOVRZNDNjbG1YVSs3OUg0b0RxNUIybVIxRjdudFZnZi9EZ1NTaFowY0R4cnd5TGpvYlhGYStYdG9pR2dDcTduZVcrM09Lc3ZZSzVSbk5VQVpsUzY1QitvdzNEdFdWZytEaUpJQUxjQ1JBZUQzNWM4enQzWlBmUFFQbFpZM0pidVI3bUVZcW1HV0NPMU9MTGZ1TXVWeUUyb2g0SjJLUSttR2pZR3pwVjNzVkV1SEk2RlBXSnZKeVhFWUdMTEZvN0pmMFZpM3V2M1BFeFdTQTZtTjVJOHhDZkZIRWJiSDhnVDhNeklBc2VlQWFKd2lwN09Xa08vK2VVNFdtVVU3aDBXTitNLzlFdStLeWZsU1RFWDY3UEF2S3hNS0I5NXBBdmY5WFJoeGc5TUhpWjZweEU1M0dBQ2s1LS1ESkRPbEh5ODZOSWY5cVdKUjkxaGtRPT0%3D--ad7282287401f97c57b8d76f4217d10dd2cd3f96',
    }

    headers = {
        'authority': 'als.dafabet.com',
        'accept': 'application/json',
        'accept-language': 'pt-BR',
        'content-type': 'application/json',
        # 'cookie': 'mhlanguage=pt; gtm-currency=BRL; dafaUrl[mobileUrl]=https%3A%2F%2Fm.dafabet.com%2Fpt; dafaUrl[login]=https%3A%2F%2Fm.dafabet.com%2Fpt%2Flogin%3Fproduct%3Dsports-df; dafaUrl[logout]=https%3A%2F%2Fm.dafabet.com%2Fpt%2Flogout; dafaUrl[registration]=https%3A%2F%2Fwww.dafabet.com%2Fpt%2Fjoin%2Fsports-df%3Fregvia%3D26; dafaUrl[desktopUrl]=https%3A%2F%2Fwww.dafabet.com%2Fpt; visid_incap_2519778=boSm49ZeR5aBs3eQwdaLQ3V4tWQAAAAAQUIPAAAAAADTVXQdjbCjhVzNp+xvDqck; incap_ses_1354_2519778=GbPPVLfciVDf0okal2DKEnV4tWQAAAAAHAWGNiSeAexS0+ocbF/egw==; reese84=3:S4e6QYFYYOCRsqzfH4SDSA==:50UJpCZrFKTZ6+Ap5yLU2Km3ul7UsCRpZTPixnmYzXVSfmMFsgXl5Q1k92d3xZGPNfd5Nc274FfEwTbT3dA3TPNE4WPNMeO3smk4IaLkedqISIAaA77Q3M80e9PUYNUWkMAPxjg6+to9D1wU5LqWwezL2sH/TRIGjBAIU2iuvRHEzj4hR//TGkft5jfnUFAJ9CKWqs0RIFbDo0QfYZiXAZWnHzrc/Pnaiu94Zjc2WNylqDVA81Q/hrwuFeRvg4kfyhAkokjjSCYdzQgltahAgsbeQ4lhBaK0H0ChUl0PsGMCQ7+ZoRuEsk72t/cYKfWxannHsLuUqx1B4vIAS/mTOCfe3Cf3a+8gIEr1I5+5OH5htA0qz0DIcM4tL9yBMzJMgl2lUJvjR0GpdJ1KYziVmD+Ibpcrs+5e+VnKMs6uKSLxiFDzp2syaOF4GK2Webu6JhXHDw4JPXckJZLmfXNNtmOlxLCteSzLbueOzTMtqy4=:zEfjqHbjoJP1bz2cKyFJg5DU7ZjjhjMYWeAH5BVnAwI=; nlbi_2519778=OzizHbAHnmy5vO5DzdO2rAAAAAA5Rk326avoGORd7MjZyLhN; betslip_menu=single; user_accept_higher_odds=true; site_version=web; PHPSESSID=3ten3ul1oe3q7ql22rc5qevok3; wbcToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IkJyTWFudWNhIiwicGxheWVySWQiOjIyNDY5ODU5LCJzZXNzaW9uVG9rZW4iOiJkNGZjMjYzYy0zZTgxLTRjNWYtODk3YS0wM2M2ZmE0ZGE4Y2IiLCJpc3MiOiJ3ZWJjb21wb3NlciIsImF1ZCI6IndlYmNvbXBvc2VyIiwiZXhwIjoxNjg5NzAwOTY5fQ.Xj7aleotHufmHkpQyuRrMXBpHJJTPnk_RI-R50YBDYw; gtm-username=BrManuca; gtm-userid=22469859; dafaUrl[cashierDeposit]=https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%2Falsports%2Ftransaction%2Fdeposit%3Fticket%3Dd4fc263c-3e81-4c5f-897a-03c6fa4da8cb; dafaUrl[cashierTransfer]=https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%2Falsports%2Ftransaction%2Ftransfer%3Fticket%3Dd4fc263c-3e81-4c5f-897a-03c6fa4da8cb; dafaUrl[cashierCashPoints]=https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%2Falsports%2Ftransaction%2Fcashpoints%3Fticket%3Dd4fc263c-3e81-4c5f-897a-03c6fa4da8cb; dafaUrl[cashierWithdrawal]=https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%2Falsports%2Ftransaction%2Fwithdrawal%3Fticket%3Dd4fc263c-3e81-4c5f-897a-03c6fa4da8cb; dafaUrl[cashier]=https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%3Fticket%3Dd4fc263c-3e81-4c5f-897a-03c6fa4da8cb; nlbi_2519778_2147483392=+hOvF9ENQl1+7NmdzdO2rAAAAABZqSMXkOPIQdV9GvtMzVKN; previous_username=brmanuca; X_DEVICE_VIEW=desktop; visid_incap_2267509=Kaq2K6BuTIOOYpPfERqvBgF7tWQAAAAAQUIPAAAAAACmJ2qO50qsrqE3JAi/GlQJ; incap_ses_1354_2267509=penhKn4iAQUYqYsal2DKEgF7tWQAAAAAvZfBub30hp2VdLaxF5q96w==; currency=BRL; ADRUM=s=1689615503752&r=https%3A%2F%2Fwww.dafabet.com%2Fpt%2F%3F601935764; _session=SXpoY2xmWVNnZWZ5RE80VWJCejYyczFZcXFxclMyWGNva1EyOWxlRzRQalFNNmY2V3luaFJyc3FGazluckgxMjVpRHllVi9WZ2tLRThiMW93bHRtcUd1RUJBOHJJeGlEN3U2aVpjMVpKWmZvcUF5Z0VLNVYxNE5DbjBwbTh2ZFZ3VXE4cWxxd3MwVWx2N0pEU0dVQTl5VTErZ0JiQkJjWC9VekpPUG1lSTY5cGw1QU9tS2FuUk1uWU5LY1VQbFNneDZueHJiSkRPKzZmMW1RbTlsWkJUWFBYS2lxK0ladHVyUC9KMXRrQmFxNElaYnNCYWszbUJpWkk2YkY5RTR5c0drcW8rUUhnUzNOMUhyNmJTRnZYVEpYejZXMi9FV1RxSmNwTDFjOHhnQWxxZmM3aVNpR2hmM0JpUmlOSGVnL2pKbHp3d0lFV01JNDRWSzZFcUhXRGNWM2JxSWlKT0FpRU1tNy9yNTlFdGlDRW5pOUtOTmhsWUtqcS92YmIyY1JiZkpWNWpIbWlBZWJzR281dklRS1BycFRRMkZnSDZQUWxtRkk1R1ZTeEs4ZDBLdVg2ZEFWRXg3b3ozdVZtZWsvMDVrTGtHTGZjUkIxOVRZNDNjbG1YVSs3OUg0b0RxNUIybVIxRjdudFZnZi9EZ1NTaFowY0R4cnd5TGpvYlhGYStYdG9pR2dDcTduZVcrM09Lc3ZZSzVSbk5VQVpsUzY1QitvdzNEdFdWZytEaUpJQUxjQ1JBZUQzNWM4enQzWlBmUFFQbFpZM0pidVI3bUVZcW1HV0NPMU9MTGZ1TXVWeUUyb2g0SjJLUSttR2pZR3pwVjNzVkV1SEk2RlBXSnZKeVhFWUdMTEZvN0pmMFZpM3V2M1BFeFdTQTZtTjVJOHhDZkZIRWJiSDhnVDhNeklBc2VlQWFKd2lwN09Xa08vK2VVNFdtVVU3aDBXTitNLzlFdStLeWZsU1RFWDY3UEF2S3hNS0I5NXBBdmY5WFJoeGc5TUhpWjZweEU1M0dBQ2s1LS1ESkRPbEh5ODZOSWY5cVdKUjkxaGtRPT0%3D--ad7282287401f97c57b8d76f4217d10dd2cd3f96',
        'origin': 'https://als.dafabet.com',
        'referer': 'https://als.dafabet.com/proxy?master=www.dafabet.com?bv=169.1.1',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Brave";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'x-accept-language': 'pt-BR',
        'x-custom-lb-geoip-country': 'BR',
        'x-lvs-hstoken': 'J6wlh8uDphieDzTTY6vsNNxO2YWAcCY-G0y5nmE2nfD6sbItrNyoKYiZ8tZTSgDnyYph5oJN7LfqU1vaS1owbkNbnG863PCqxsKNcYC0n5jIE_-9gfwZKv64pAB3nGUG',
        'x-requested-with': 'XMLHttpRequest',
        'x-sb-brand': 'DAFABET',
        'x-sb-origin': 'WEB',
        'x-sb-portalid': '22',
    }

    params = {
        'hash': response_hash,
        'l': 'pt',
    }

    json_data = {
        'bettable': True,
        'marketStatus': 'OPEN',
        'periodType': 'PRE_MATCH',
        'includeMarkets': True,
        'includeHiddenOutcomes': True,
        'includeHiddenMarkets': False,
        'maxMarketPerEvent': 100,
        'lightWeightResponse': True,
        'sportGroups': 'REGULAR',
        'allBettableEvents': True,
        'marketFilter': 'GAME',
        'eventType': 'GAME',
        'excludeMarketByOpponent': True,
        'marketTypeIds': '1',
        'periodIds': '100,200,232,233',
        'maxMarketsPerMarketType': 100,
        'sortMarketsByPriceDifference': True,
        'includeLiveEvents': True,
        'sportCodes': 'FOOT,TENN,BASK,BASE,VOLL,BADM,ICEH,AMFB,RUGL,RUGU,TABL,SNOO,DART,CRIC,HAND,SQUA,EFOT,EBSK,VICR,FUTS,BEVO',
        'liveMarketStatus': 'OPEN,SUSPENDED',
        'liveAboutToStart': True,
        'liveExcludeLongTermSuspended': True,
        'eventPathIds': '18756495,18756498,18756458,18756502,18756500,18756506,18756504,18756508,212108,37234773,529271,529275,529277,529273,529279,529282,211990,25716420,2393159,36901305,18374985,36944134,358288,19205963,19205966,19205965,19205991,19205973,19205969,19205981,19205971,19205985,19205993,19205989,19205987,19205975,19205982,36822438,19198731,39153912,19362675,37646333,209674,177547,177554,183963,177552,177550,177546,177553,177551,23104,32249605,31687139,39319946,31906398,31940920,31940915,31940333,31940916,31918009,31940919,31940924,211846,20531211,145729,26500,26502,26491,24284,26505,26513,23714,26516,37690940,17919565,208449,36829027,145730,43647,46323,43430,29117,44690,23343,23715,42818,43401,44709,23717,44837,17960992,37690950,208121,39153510,35455253,36829038,32453257,36619774,3772161,300312,17777473,240486,240488,240510,240512,240514,240516,240544,240547,240549,31409883,119675,37692009,18008523,45068,45049,44839,45069,44851,45050,44856,45048,45051,22337637,22980,39130934,23034,23132,32076128,23454,39261601,211721,23405,218228,23169,44152,37691291,29855,43800,105245,99090,43606,43721,83579,24267,28571,217811,23031,217818,23716,18499302,217850,217979,23925,23428,23489,31229191,31229190,23410,23818,18146877,217793,24045,23421371,23421372,24047046,23131,18507499,31950283,18205606,2831312,18643221,28964,17964292,17036041,17036049,17036058,17036066,17036075,17036084,17033333,17036094,149858,19183288,30907278,30907276,24244,31006459,31006457,18205655,171856,217615,23926879,23926882,22937,29241,18659864,16609736,26047,17006762,31770182,168610,23309,23115,25881011,26085044,25175,23952,23058,217952,23522,217906,23026,27057,66647,19869874,149137,23221,24920,154667,23151,486230,30989141,30988458,23289,26139,218447,218472,24865,24925,23271,24121998,23819,25176,26827,16700685,16700687,16201750,18136812,17076306,17076307,23009,30914987,30983962,209280,23234,22934,18136778,23333,22977,23311,25019,23404,23980,114051,207317,23022,28970,23332,24821,23363,24041,24414,24601,28961,3170436,1858471,23070,17907965,23647,22926,24536,133442,24062,25575076,3600418,25910806,25064,18907371,28732,23500,25637,22896,23114,25098,24046,22935,23508,132797,23016,17187178,23744,16419934,16521942,23094,24762,36826181,22749604,23505,23470,22940,25445,23308,24280,26053,22925,63885,23519,2382105,23113,17080026,24129,63804,23168,18846446,152927,24563,104625,22744273,24125,27167,3571834,23399,23292,42394,25096,29512,25373,62253,23025,23623,23109,24276169,22914,25202,25884,25572,23375,24517,23460,3168745,23861,2839201,23869,24822,152373,24636,29637,160973,26194,31427469,63953,2655517,17147539,16313501,25249,25901,31270012,158529,22915,1102784,24617959,25017,25454899,23924,25660101,25802274,3122025,31553381,208181,23771,63123,23293,24038,25122,63702,27073,24708,23150,23288,23719,24370,24169,16823956,23544,16919717,154986,25403654,23086,76839,23347,25252,137767,22894,36586125,117220,22941,42604,23817,44125,18080822,16729839,572745,3593973,1316444,23732,25965493,23847,26620,23954,63166,28893,24452,23008,149950,209805,17783976,25927021,252919,26052337,240',
        'sortByEventpath': True,
        'sortByEventpathIds': '18756495,18756498,18756458,18756502,18756500,18756506,18756504,18756508,212108,37234773,529271,529275,529277,529273,529279,529282,211990,25716420,2393159,36901305,18374985,36944134,358288,19205963,19205966,19205965,19205991,19205973,19205969,19205981,19205971,19205985,19205993,19205989,19205987,19205975,19205982,36822438,19198731,39153912,19362675,37646333,209674,177547,177554,183963,177552,177550,177546,177553,177551,23104,32249605,31687139,39319946,31906398,31940920,31940915,31940333,31940916,31918009,31940919,31940924,211846,20531211,145729,26500,26502,26491,24284,26505,26513,23714,26516,37690940,17919565,208449,36829027,145730,43647,46323,43430,29117,44690,23343,23715,42818,43401,44709,23717,44837,17960992,37690950,208121,39153510,35455253,36829038,32453257,36619774,3772161,300312,17777473,240486,240488,240510,240512,240514,240516,240544,240547,240549,31409883,119675,37692009,18008523,45068,45049,44839,45069,44851,45050,44856,45048,45051,22337637,22980,39130934,23034,23132,32076128,23454,39261601,211721,23405,218228,23169,44152,37691291,29855,43800,105245,99090,43606,43721,83579,24267,28571,217811,23031,217818,23716,18499302,217850,217979,23925,23428,23489,31229191,31229190,23410,23818,18146877,217793,24045,23421371,23421372,24047046,23131,18507499,31950283,18205606,2831312,18643221,28964,17964292,17036041,17036049,17036058,17036066,17036075,17036084,17033333,17036094,149858,19183288,30907278,30907276,24244,31006459,31006457,18205655,171856,217615,23926879,23926882,22937,29241,18659864,16609736,26047,17006762,31770182,168610,23309,23115,25881011,26085044,25175,23952,23058,217952,23522,217906,23026,27057,66647,19869874,149137,23221,24920,154667,23151,486230,30989141,30988458,23289,26139,218447,218472,24865,24925,23271,24121998,23819,25176,26827,16700685,16700687,16201750,18136812,17076306,17076307,23009,30914987,30983962,209280,23234,22934,18136778,23333,22977,23311,25019,23404,23980,114051,207317,23022,28970,23332,24821,23363,24041,24414,24601,28961,3170436,1858471,23070,17907965,23647,22926,24536,133442,24062,25575076,3600418,25910806,25064,18907371,28732,23500,25637,22896,23114,25098,24046,22935,23508,132797,23016,17187178,23744,16419934,16521942,23094,24762,36826181,22749604,23505,23470,22940,25445,23308,24280,26053,22925,63885,23519,2382105,23113,17080026,24129,63804,23168,18846446,152927,24563,104625,22744273,24125,27167,3571834,23399,23292,42394,25096,29512,25373,62253,23025,23623,23109,24276169,22914,25202,25884,25572,23375,24517,23460,3168745,23861,2839201,23869,24822,152373,24636,29637,160973,26194,31427469,63953,2655517,17147539,16313501,25249,25901,31270012,158529,22915,1102784,24617959,25017,25454899,23924,25660101,25802274,3122025,31553381,208181,23771,63123,23293,24038,25122,63702,27073,24708,23150,23288,23719,24370,24169,16823956,23544,16919717,154986,25403654,23086,76839,23347,25252,137767,22894,36586125,117220,22941,42604,23817,44125,18080822,16729839,572745,3593973,1316444,23732,25965493,23847,26620,23954,63166,28893,24452,23008,149950,209805,17783976,25927021,252919,26052337,240',
        'dateFrom': '2023-07-17T03:00:00.000+00:00',
        'dateTo': '2023-07-18T10:59:59.999+00:00',
        'page': 1,
        'eventsPerPage': 70,
    }

    response = requests.post('https://als.dafabet.com/xapi/rest/events', params=params, cookies=cookies, headers=headers, json=json_data)
    print(response.text)
    if response.status_code <= 300:
        responseData = response.json()
        print(responseData)

    else:
        {
            "error": response.status_code
        }    
    return {
        "bets": responseData
    }

@app.route("/api/v1/bot/allgames/", methods=["POST"])
def allGames():

    cookies = {
        'mhlanguage': 'pt',
        'gtm-currency': 'BRL',
        'dafaUrl[mobileUrl]': 'https%3A%2F%2Fm.dafabet.com%2Fpt',
        'dafaUrl[login]': 'https%3A%2F%2Fm.dafabet.com%2Fpt%2Flogin%3Fproduct%3Dsports-df',
        'dafaUrl[logout]': 'https%3A%2F%2Fm.dafabet.com%2Fpt%2Flogout',
        'dafaUrl[registration]': 'https%3A%2F%2Fwww.dafabet.com%2Fpt%2Fjoin%2Fsports-df%3Fregvia%3D26',
        'dafaUrl[desktopUrl]': 'https%3A%2F%2Fwww.dafabet.com%2Fpt',
        'visid_incap_2519778': 'boSm49ZeR5aBs3eQwdaLQ3V4tWQAAAAAQUIPAAAAAADTVXQdjbCjhVzNp+xvDqck',
        'nlbi_2519778': 'OzizHbAHnmy5vO5DzdO2rAAAAAA5Rk326avoGORd7MjZyLhN',
        'betslip_menu': 'single',
        'user_accept_higher_odds': 'true',
        'site_version': 'web',
        'X_DEVICE_VIEW': 'desktop',
        'visid_incap_2267509': 'Kaq2K6BuTIOOYpPfERqvBgF7tWQAAAAAQUIPAAAAAACmJ2qO50qsrqE3JAi/GlQJ',
        'currency': 'BRL',
        'PHPSESSID': '0rr54kemusacgkrhsahd5o94gr',
        'wbcToken': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFmdGVyYmV0IiwicGxheWVySWQiOjIyNjQyMzEyLCJzZXNzaW9uVG9rZW4iOiJhMjFlZDYzMS0yODYzLTQ2NjUtODZkOC0xNWMwNjY2OWJhNDgiLCJpc3MiOiJ3ZWJjb21wb3NlciIsImF1ZCI6IndlYmNvbXBvc2VyIiwiZXhwIjoxNjg5NzAzMDczfQ.TynqWxZtL3lYtnHXAuA_VckHGDUJ6FdLDC4RZd8iRjY',
        'gtm-username': 'afterbet',
        'gtm-userid': '22642312',
        'dafaUrl[cashierDeposit]': 'https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%2Falsports%2Ftransaction%2Fdeposit%3Fticket%3Da21ed631-2863-4665-86d8-15c06669ba48',
        'dafaUrl[cashierTransfer]': 'https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%2Falsports%2Ftransaction%2Ftransfer%3Fticket%3Da21ed631-2863-4665-86d8-15c06669ba48',
        'dafaUrl[cashierCashPoints]': 'https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%2Falsports%2Ftransaction%2Fcashpoints%3Fticket%3Da21ed631-2863-4665-86d8-15c06669ba48',
        'dafaUrl[cashierWithdrawal]': 'https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%2Falsports%2Ftransaction%2Fwithdrawal%3Fticket%3Da21ed631-2863-4665-86d8-15c06669ba48',
        'dafaUrl[cashier]': 'https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%3Fticket%3Da21ed631-2863-4665-86d8-15c06669ba48',
        'previous_username': 'afterbet',
        'ADRUM': 's=1689622116906&r=https%3A%2F%2Fals.dafabet.com%2Fm%2Fpt%2Flive%2Fsport%2F240-FOOT%3F0',
        '_session': 'WTAvblAvcno4eW5oRGdjV1Nib1lLOEVucGs2RExGcnJxMk95V3Y5cnRLWnVNeEkxdGN0OFRVbTZRYysra0ZwVy8vSm0zeHl4KzVRT1dKZUZMQVlySEpBamF5VU1ac1lZcTBWb254czJzSUxLcmdsUU8xUWFBUXhjb09Zc3FzNThNUHVpdkpDOCt0RkphVTltMEFjSktPcUZEZHJaS2VCNDUxdzhqUUNLTnJJMVVKMHVUKzlWbjBWalZvTXFlTVNiVHRBSlZnSWkrYnlZR3Rhc3dhY2Vxelcyd3ZCc0g1V1dNdmV5c1VNZnBTS2dtb3dlYUZFSjRCUzB6TjNDdmZyYWxTQ0t4b1BNNnBhaHc2dStvKzlyc3dnVlE3UW1DMFBlWHZKVGJHWnlTWnZNaTNOVElJTEZnWVRrSENOaElrOHlONDc4cmNmMURFSUN6SjBuaTVuU3ZSRlhiN1NXcGQ3Z2kvcVNQcXFjV1BiOTAyTVR3WHA0bVc4cEVuOW1vVFBSTHM4QWZCdTBWVjhneWhhN1BxcUNpcmQ1SjAxWTkxM3ZJYXljTHFzd3BBRnZ5YUdjREVadGNVTWRNck52WG1XSndqSy9GOEFwdUl0TEp1MHVJclYyMSttU0VmYW1zMU9udUVUMW5Gbkkra2VyUUFiM0ZZQnNLWGJUK09SbC9hemNwdkRSUGdmb2VTOVBKSkw4YzJrRDU1VHNBbDh4YmhmNjVwaEJrZndlOGZXcXUvNnF6elFHV0ErM0FHYW03SkI4bHRFeHF2OFFvOVdudHQ5TjZacEZ0bW5yZ1RqNVJPa1U4bmRJTWRTTXpoTklYektiOEprUXB4Z2RkYk5qOStjcVJIWFU3S2svRVJBTUVjZHQ1L2NmWDRkNW5MQWRWckVNWWhCaXVyayt6dGRWcFBBZFF2RHRDMk5NdXVueS9KU2R0bGg0RDNSeEQ0OGl1NTRSV0UwbDBMRTBWUkFZa25kSFU4a3E3UVdEQlJ1NkJZR2ExczJ5MzFTZzlJN0JjUnBkLS1JQXROTUk3RXdzWTFqbEJCd3ZqWTRnPT0%3D--75231f6e4205ec7f419f32d37d8b65e9aea388fb',
        'incap_ses_1354_2519778': 'eyWmEPnRISwyVuobl2DKEmgmuGQAAAAABlTpWBVBULPKxFUT4mXUnA==',
        'incap_ses_1354_2267509': 'NHbrQEdF1iAivOobl2DKEugmuGQAAAAANmHH+0/6hynXJE5rNPqdqQ==',
        'nlbi_2519778_2147483392': 'dSOtRuUZMUu+6KEAzdO2rAAAAAArhR/Sh8ye6WMeuJUp67g0',
        'reese84': '3:3U5wSpSffU7Nc7moA5fneQ==:oBX31Hy/uuFZUoXX5QE3F3z/okib1Ixd6nMaur2/o1fciHJP0p59COfloeCbYejztfA853c3bwdRR/OxkhExRVVFWvR+tsuekH524tCi+fdHzzNRREd8lH78SuSA6xTW1XDw+rAeZ2eYwWhpUD+e9QmVx4zosd8Z43Aauo/NsEHi8n/g2z/nnVFz953vUBq7dnNabEEYOMAcImVyfzFgQMzsvh6WK8t2Vs/B053HmEPlgFKtS/gB4u5I28XQqIlnHVQSgRvSOGGb+5QLIZZ+u4/qJ8IawvSJUBABKXKme3okEwZZ+6OfgXm3kTpzpnCJf7LDDoQqAc9LuyPufYyo06CTNZgsFw46TcqZxAC+uzOJaiqjAU3otsHX/joas5DJoteVzt3KFL08MOfjcnockGwMbWPEpca3UvpeYjsZ87ZQm8CubUduf17TqxlF3rEUu74WOjQcZjXNjdgCupNnYDnrfdkERguRnY7/PJojslk=:EIqTwHy3PlIodowNQ+IaNMW5qK+dubxDuOcATM7CZPY=',
    }

    headers = {
        'authority': 'als.dafabet.com',
        'accept': 'application/json',
        'accept-language': 'pt-BR',
        # 'cookie': 'mhlanguage=pt; gtm-currency=BRL; dafaUrl[mobileUrl]=https%3A%2F%2Fm.dafabet.com%2Fpt; dafaUrl[login]=https%3A%2F%2Fm.dafabet.com%2Fpt%2Flogin%3Fproduct%3Dsports-df; dafaUrl[logout]=https%3A%2F%2Fm.dafabet.com%2Fpt%2Flogout; dafaUrl[registration]=https%3A%2F%2Fwww.dafabet.com%2Fpt%2Fjoin%2Fsports-df%3Fregvia%3D26; dafaUrl[desktopUrl]=https%3A%2F%2Fwww.dafabet.com%2Fpt; visid_incap_2519778=boSm49ZeR5aBs3eQwdaLQ3V4tWQAAAAAQUIPAAAAAADTVXQdjbCjhVzNp+xvDqck; nlbi_2519778=OzizHbAHnmy5vO5DzdO2rAAAAAA5Rk326avoGORd7MjZyLhN; betslip_menu=single; user_accept_higher_odds=true; site_version=web; X_DEVICE_VIEW=desktop; visid_incap_2267509=Kaq2K6BuTIOOYpPfERqvBgF7tWQAAAAAQUIPAAAAAACmJ2qO50qsrqE3JAi/GlQJ; currency=BRL; PHPSESSID=0rr54kemusacgkrhsahd5o94gr; wbcToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFmdGVyYmV0IiwicGxheWVySWQiOjIyNjQyMzEyLCJzZXNzaW9uVG9rZW4iOiJhMjFlZDYzMS0yODYzLTQ2NjUtODZkOC0xNWMwNjY2OWJhNDgiLCJpc3MiOiJ3ZWJjb21wb3NlciIsImF1ZCI6IndlYmNvbXBvc2VyIiwiZXhwIjoxNjg5NzAzMDczfQ.TynqWxZtL3lYtnHXAuA_VckHGDUJ6FdLDC4RZd8iRjY; gtm-username=afterbet; gtm-userid=22642312; dafaUrl[cashierDeposit]=https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%2Falsports%2Ftransaction%2Fdeposit%3Fticket%3Da21ed631-2863-4665-86d8-15c06669ba48; dafaUrl[cashierTransfer]=https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%2Falsports%2Ftransaction%2Ftransfer%3Fticket%3Da21ed631-2863-4665-86d8-15c06669ba48; dafaUrl[cashierCashPoints]=https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%2Falsports%2Ftransaction%2Fcashpoints%3Fticket%3Da21ed631-2863-4665-86d8-15c06669ba48; dafaUrl[cashierWithdrawal]=https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%2Falsports%2Ftransaction%2Fwithdrawal%3Fticket%3Da21ed631-2863-4665-86d8-15c06669ba48; dafaUrl[cashier]=https%3A%2F%2Fpay.dafabet.com%2Fc%2Flatam%2Fpt%2Fpayment-options%2Fdeposit%3Fticket%3Da21ed631-2863-4665-86d8-15c06669ba48; previous_username=afterbet; ADRUM=s=1689622116906&r=https%3A%2F%2Fals.dafabet.com%2Fm%2Fpt%2Flive%2Fsport%2F240-FOOT%3F0; _session=WTAvblAvcno4eW5oRGdjV1Nib1lLOEVucGs2RExGcnJxMk95V3Y5cnRLWnVNeEkxdGN0OFRVbTZRYysra0ZwVy8vSm0zeHl4KzVRT1dKZUZMQVlySEpBamF5VU1ac1lZcTBWb254czJzSUxLcmdsUU8xUWFBUXhjb09Zc3FzNThNUHVpdkpDOCt0RkphVTltMEFjSktPcUZEZHJaS2VCNDUxdzhqUUNLTnJJMVVKMHVUKzlWbjBWalZvTXFlTVNiVHRBSlZnSWkrYnlZR3Rhc3dhY2Vxelcyd3ZCc0g1V1dNdmV5c1VNZnBTS2dtb3dlYUZFSjRCUzB6TjNDdmZyYWxTQ0t4b1BNNnBhaHc2dStvKzlyc3dnVlE3UW1DMFBlWHZKVGJHWnlTWnZNaTNOVElJTEZnWVRrSENOaElrOHlONDc4cmNmMURFSUN6SjBuaTVuU3ZSRlhiN1NXcGQ3Z2kvcVNQcXFjV1BiOTAyTVR3WHA0bVc4cEVuOW1vVFBSTHM4QWZCdTBWVjhneWhhN1BxcUNpcmQ1SjAxWTkxM3ZJYXljTHFzd3BBRnZ5YUdjREVadGNVTWRNck52WG1XSndqSy9GOEFwdUl0TEp1MHVJclYyMSttU0VmYW1zMU9udUVUMW5Gbkkra2VyUUFiM0ZZQnNLWGJUK09SbC9hemNwdkRSUGdmb2VTOVBKSkw4YzJrRDU1VHNBbDh4YmhmNjVwaEJrZndlOGZXcXUvNnF6elFHV0ErM0FHYW03SkI4bHRFeHF2OFFvOVdudHQ5TjZacEZ0bW5yZ1RqNVJPa1U4bmRJTWRTTXpoTklYektiOEprUXB4Z2RkYk5qOStjcVJIWFU3S2svRVJBTUVjZHQ1L2NmWDRkNW5MQWRWckVNWWhCaXVyayt6dGRWcFBBZFF2RHRDMk5NdXVueS9KU2R0bGg0RDNSeEQ0OGl1NTRSV0UwbDBMRTBWUkFZa25kSFU4a3E3UVdEQlJ1NkJZR2ExczJ5MzFTZzlJN0JjUnBkLS1JQXROTUk3RXdzWTFqbEJCd3ZqWTRnPT0%3D--75231f6e4205ec7f419f32d37d8b65e9aea388fb; incap_ses_1354_2519778=eyWmEPnRISwyVuobl2DKEmgmuGQAAAAABlTpWBVBULPKxFUT4mXUnA==; incap_ses_1354_2267509=NHbrQEdF1iAivOobl2DKEugmuGQAAAAANmHH+0/6hynXJE5rNPqdqQ==; nlbi_2519778_2147483392=dSOtRuUZMUu+6KEAzdO2rAAAAAArhR/Sh8ye6WMeuJUp67g0; reese84=3:3U5wSpSffU7Nc7moA5fneQ==:oBX31Hy/uuFZUoXX5QE3F3z/okib1Ixd6nMaur2/o1fciHJP0p59COfloeCbYejztfA853c3bwdRR/OxkhExRVVFWvR+tsuekH524tCi+fdHzzNRREd8lH78SuSA6xTW1XDw+rAeZ2eYwWhpUD+e9QmVx4zosd8Z43Aauo/NsEHi8n/g2z/nnVFz953vUBq7dnNabEEYOMAcImVyfzFgQMzsvh6WK8t2Vs/B053HmEPlgFKtS/gB4u5I28XQqIlnHVQSgRvSOGGb+5QLIZZ+u4/qJ8IawvSJUBABKXKme3okEwZZ+6OfgXm3kTpzpnCJf7LDDoQqAc9LuyPufYyo06CTNZgsFw46TcqZxAC+uzOJaiqjAU3otsHX/joas5DJoteVzt3KFL08MOfjcnockGwMbWPEpca3UvpeYjsZ87ZQm8CubUduf17TqxlF3rEUu74WOjQcZjXNjdgCupNnYDnrfdkERguRnY7/PJojslk=:EIqTwHy3PlIodowNQ+IaNMW5qK+dubxDuOcATM7CZPY=',
        'referer': 'https://als.dafabet.com/proxy?master=www.dafabet.com?bv=169.1.1',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Brave";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'x-accept-language': 'pt-BR',
        'x-lvs-hstoken': 'J6wlh8uDphieDzTTY6vsNNxO2YWAcCY-G0y5nmE2nfD6sbItrNyoKYiZ8tZTSgDnyYph5oJN7LfqU1vaS1owbkNbnG863PCqxsKNcYC0n5jIE_-9gfwZKv64pAB3nGUG',
        'x-requested-with': 'XMLHttpRequest',
        'x-sb-brand': 'DAFABET',
        'x-sb-origin': 'WEB',
        'x-sb-portalid': '22',
    }

    params = {
        'periodType': 'PRE_MATCH',
        'includeUnpricedMarkets': 'false',
        'includeMarketTypes': 'false',
        'lightWeightResponse': 'true',
        'eventTypeFilter': 'GAMEEVENT,RANKEVENT',
        'sportGroups': 'REGULAR',
        'l': 'pt',
    }

    response = requests.get('https://als.dafabet.com/xapi/rest/eventpathtree', params=params, cookies=cookies, headers=headers)

    if response.status_code <= 300:
        responseData = response.json()

    else: {
        "error": response.status_code
    }
    return {
        "allGames": responseData
    }
    
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
    
