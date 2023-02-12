import requests

def getMatchIDs(api, shard, puuid):   
    url = f"https://{shard}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    response = requests.get(url, params={'api_key':api})
    resp = response.json()
    return resp[0]


def getMatchDetails(api, shard, matchID):
    url = f"https://{shard}.api.riotgames.com/lol/match/v5/matches/{matchID}"
    response = requests.get(url, params={'api_key':api})
    resp = response.json()
    players_info = []
    player_data = {}
    
    for player in resp['info']['participants']:
        player_data['Player Name'] = player['summonerName']
        player_data['Champion'] = player['championName']
        player_data['Kills'] = player['kills']
        player_data['Deaths'] = player['deaths']
        player_data['Assists'] = player['assists']
        player_data['Win'] = player['win']
        players_info.append(player_data)
        player_data = {}

    return players_info
            