import requests

def getUser(api, username, region):
    if username != '':
        url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{username}'
        response = requests.get(url, params={'api_key':api})
        resp = response.json()
        name = resp['name']
        id = resp['id']
        accountId = resp['accountId']
        puuid = resp['puuid']
        resp = {'id': id, 'accountId': accountId, 'puuid': puuid, 'name': name}
        return resp
    else:
        return "please fill the username"