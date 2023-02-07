import requests

api = 'RGAPI-34730d3b-1f44-4198-be68-ccc25e8eb469'

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


def getStats(user):
    pass