import requests
from helpers import GenericImages as GI

#------------------------------------------------------------------------------------------------------

def getMatchIDs(api, shard, puuid):   
    url = f"https://{shard}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    response = requests.get(url, params={'api_key':api, 'count':10})
    resp = response.json()
    return resp


def getMatchDetails(api, shard, matchID):
    result = []
    
    for id in matchID:
        url = f"https://{shard}.api.riotgames.com/lol/match/v5/matches/{id}"
        response = requests.get(url, params={'api_key':api})
        resp = response.json()
        result.append(resp)
    
    return result

#------------------------------------------------------------------------------------------------------

def getMatchInfo(data):
    match_info_list = []

    for key in data:
        match_info = {}
        match_info['GameMode'] = key['info']['gameMode']
        match_info['GameType'] = key['info']['gameType']
        match_info['GameDuration'] = key['info']['gameDuration']
        match_info['GameTime'] = f"{int(key['info']['gameDuration']/60)}m {key['info']['gameDuration']%60}s"
        match_info_list.append(match_info)
        match_info = {}
    
    return match_info_list


def getMatchPlayersDetails(data, version):
    match_info = getMatchInfo(data)
    match_players_info = []

    for i in range(len(data)):
        players_info = []
        player_data = {}

        for player in data[i]['info']['participants']:
            player_data['PlayerName'] = player['summonerName']
            player_data['Champion'] = player['championName']
            player_data['DamageToChampions'] = player['totalDamageDealtToChampions']
            player_data['DamageTaken'] = player['totalDamageTaken']
            player_data['LaneMinionsKilled'] = player['totalMinionsKilled']
            player_data['NeutralMinionsKilled'] = player['neutralMinionsKilled']
            player_data['TotalMinionsKilled'] = player_data['NeutralMinionsKilled'] + player_data['LaneMinionsKilled']
            player_data['CSPerMinute'] = round(player_data['TotalMinionsKilled'] / ((match_info[i]['GameDuration'])/60), 2)
            player_data['Kills'] = player['kills']
            player_data['Deaths'] = player['deaths']
            player_data['Assists'] = player['assists']
            player_data['Win'] = player['win']

            if player_data['Deaths'] == 0:
                player_data['KDA'] = "Perfect"
            else:
                player_data['KDA'] = round(((player['kills'] + player['assists']) / player_data['Deaths']), 2)
            
            player_data['ChampionImage'] = GI.getChampImage(player['championName'], version)
            
            player_data['Keystone'] = GI.getRuneImage(player["perks"]["styles"][0]["selections"][0]["perk"], version)
            player_data['SecondaryRune'] = GI.getRuneImage(player["perks"]["styles"][1]['style'], version)

            player_data['Item0'] = GI.getItemImage(player['item0'], version)
            player_data['Item1'] = GI.getItemImage(player['item1'], version)
            player_data['Item2'] = GI.getItemImage(player['item2'], version)
            player_data['Item3'] = GI.getItemImage(player['item3'], version)
            player_data['Item4'] = GI.getItemImage(player['item4'], version)
            player_data['Item5'] = GI.getItemImage(player['item5'], version)
            player_data['Item6'] = GI.getItemImage(player['item6'], version)

            player_data['Summoner1'] = GI.getSummonerSpellImage(player['summoner1Id'], version)
            player_data['Summoner2'] = GI.getSummonerSpellImage(player['summoner2Id'], version)

            players_info.append(player_data)
            player_data = {}
        
        match_players_info.append(players_info)

    return match_players_info

#------------------------------------------------------------------------------------------------------