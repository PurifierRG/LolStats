import requests

def getMatchIDs(api, puuid, shard):
    url = f"https://{shard}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    response = requests.get(url, params={'api_key':api})
    resp = response.json()
    return resp