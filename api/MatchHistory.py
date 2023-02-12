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
    return resp


def getMatchPlayersDetails(data):
    players_info = []
    player_data = {}
    match_info = getMatchInfo(data)

    for player in data['info']['participants']:
        player_data['Player Name'] = player['summonerName']
        url = f"http://ddragon.leagueoflegends.com/cdn/13.3.1/img/champion/{player['championName']}.png"
        player_data['Champion Image'] = url
        player_data['Champion'] = player['championName']
        player_data['Damage To Champions'] = player['totalDamageDealtToChampions']
        player_data['Damage Taken'] = player['totalDamageTaken']
        player_data['Lane Minions Killed'] = player['totalMinionsKilled']
        player_data['Neutral Minions Killed'] = player['neutralMinionsKilled']
        player_data['Total Minions Killed'] = player_data['Neutral Minions Killed'] + player_data['Lane Minions Killed']
        player_data['CS Per Minute'] = round((player_data['Total Minions Killed'] / match_info['Game Duration']), 2)
        player_data['Kills'] = player['kills']
        player_data['Deaths'] = player['deaths']
        player_data['Assists'] = player['assists']
        if player_data['Deaths'] == 0:
            player_data['KDA'] = "Perfect KDA"
        else:
            player_data['KDA'] = round(((player['kills'] + player['assists']) / player_data['Deaths']), 2)
        player_data['Win'] = player['win']
        players_info.append(player_data)
        player_data = {}

    return players_info


def getMatchInfo(data):
    match_info = {}
    match_info['Game Mode'] = data['info']['gameMode']
    match_info['Game Type'] = data['info']['gameType']
    match_info['Game Duration'] = data['info']['gameDuration']/60
    return match_info