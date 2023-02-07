import requests, os
from dotenv import load_dotenv

api = os.getenv('API_KEY')

def getUser(username):
    if username != '':
        url = f'https://sg2.api.riotgames.com/lol/summoner/v4/summoners/by-name/{username}'
        response = requests.get(url, params={'api_key':api})
        resp = response.json()
        id = resp['id']
        accountId = resp['accountId']
        puuid = resp['puuid']
        resp = {'id': id, 'accountId': accountId, 'puuid': puuid}
        return resp
    else:
        return "please fill the username"

