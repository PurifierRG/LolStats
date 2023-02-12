import requests

def getMatchIDs(api, shard, puuid):   
    url = f"https://{shard}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    response = requests.get(url, params={'api_key':api})
    resp = response.json()
    print(resp)
    return resp[0]


def getMatchDetails(api, shard, matchID, type):
    url = f"https://{shard}.api.riotgames.com/lol/match/v5/matches/{matchID}"
    response = requests.get(url, params={'api_key':api})
    resp = response.json()

    if type == 'test':
        return resp

    players_info = []
    player_data = {}
    match_info = {}
    match_info['Game Mode'] = resp['info']['gameMode']
    match_info['Game Duration'] = resp['info']['gameDuration']/60

    for player in resp['info']['participants']:
        player_data['Player Name'] = player['summonerName']
        player_data['Champion'] = player['championName']
        player_data['Damage To Champions'] = player['totalDamageDealtToChampions']
        player_data['Damage Taken'] = player['totalDamageTaken']
        player_data['Lane Minions Killed'] = player['totalMinionsKilled']
        player_data['Neutral Minions Killed'] = player['neutralMinionsKilled']
        player_data['Total Minions Killed'] = player_data['Neutral Minions Killed'] + player_data['Lane Minions Killed']
        player_data['CS Per Minute'] = player_data['Total Minions Killed'] / match_info['Game Duration']
        player_data['Kills'] = player['kills']
        player_data['Deaths'] = player['deaths']
        player_data['Assists'] = player['assists']
        if player_data['Deaths'] == 0:
            player_data['KDA_Deaths'] = 1
        else:
            player_data['KDA_Deaths'] = player_data['Deaths']
        player_data['KDA'] = (player['kills'] + player['assists']) / player_data['KDA_Deaths']
        player_data['Win'] = player['win']
        players_info.append(player_data)
        player_data = {}

    return players_info
            