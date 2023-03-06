import requests
from helpers import GenericImages as GI
from helpers import cache
import concurrent.futures

#------------------------------------------------------------------------------------------------------

def getMatchIDs(api, shard, puuid):   
    url = f"https://{shard}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    response = requests.get(url, params={'api_key':api, 'count':20})
    resp = response.json()
    return resp

#------------------------------------------------------------------------------------------------------

def getAllMatchDetails(api, shard, matchID):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = executor.map(getMatchDetails, [api]*len(matchID), [shard]*len(matchID), matchID)
    return list(result)


def getMatchDetails(api, shard, id):
    url = f"https://{shard}.api.riotgames.com/lol/match/v5/matches/{id}"
    response = requests.get(url, params={'api_key':api})
    resp = response.json()
    return(resp)

#------------------------------------------------------------------------------------------------------

def getMatchInfo(data):
    match_info_list = []

    for key in data:
        match_info = {}
        match_info['QueueID'] = key['info']['queueId']
        match_info['QueueType'] = 'Other'

        if match_info['QueueID'] == 420:
            match_info['QueueType'] = 'Ranked Solo'
        elif match_info['QueueID'] == 440:
            match_info['QueueType'] = 'Ranked Flex'
        elif match_info['QueueID'] == 430:
            match_info['QueueType'] = 'Normal Blind'
        elif match_info['QueueID'] == 400:
            match_info['QueueType'] = 'Normal Draft'
        elif match_info['QueueID'] == 450:
            match_info['QueueType'] = 'ARAM'
        elif match_info['QueueID'] == 830:
            match_info['QueueType'] = 'Co-op [Intro]'
        elif match_info['QueueID'] == 840:
            match_info['QueueType'] = 'Co-op [Beginner]'
        elif match_info['QueueID'] == 850:
            match_info['QueueType'] = 'Co-op [Intermediate]'

        match_info['GameDuration'] = key['info']['gameDuration']
        match_info['GameTime'] = f"{int(key['info']['gameDuration']/60)}m {key['info']['gameDuration']%60}s"
        match_info_list.append(match_info)
        match_info = {}
    
    return match_info_list


def getMatchPlayersDetails(version, data):
    match_info = getMatchInfo(data)
    match_players_info = []

    for i in range(len(data)):
        players_info = []
        player_data = {}

        for player in data[i]['info']['participants']:
            # General
            player_data['PlayerName'] = player['summonerName']
            player_data['PlayerLevel'] = player['champLevel']
            player_data['Champion'] = player['championName']
            player_data['PlayerTeam'] = 'Blue' if player['teamId'] == 100 else 'Red'
            player_data['Win'] = player['win'] if match_info[i]['GameDuration'] > 240 else 'Remake'
            # KDA
            player_data['Kills'] = player['kills']
            player_data['Deaths'] = player['deaths']
            player_data['Assists'] = player['assists']
            player_data['KDA'] = "Perfect" if player_data['Deaths'] == 0 else round(((player['kills'] + player['assists']) / player_data['Deaths']), 2)          
            # CS
            player_data['LaneMinionsKilled'] = player['totalMinionsKilled']
            player_data['NeutralMinionsKilled'] = player['neutralMinionsKilled']
            player_data['TotalMinionsKilled'] = player_data['NeutralMinionsKilled'] + player_data['LaneMinionsKilled']
            player_data['CSPerMinute'] = round(player_data['TotalMinionsKilled'] / ((match_info[i]['GameDuration'])/60), 2)
            # Vision
            player_data['VisionScore'] = player['visionScore']
            player_data['ControlWards'] = player['visionWardsBoughtInGame']
            player_data['WardsPlaced'] = player['wardsPlaced']
            player_data['WardsDestroyed'] = player['wardsKilled']
            # Damage
            player_data['DamageToChampions'] = player['totalDamageDealtToChampions']
            player_data['DamageTaken'] = player['totalDamageTaken']
            # Images
            player_data['ChampionImage'] = GI.getChampImage(version, player['championName'])           
            player_data['Keystone'] = GI.getRuneImage(version, player["perks"]["styles"][0]["selections"][0]["perk"])
            player_data['SecondaryRune'] = GI.getRuneImage(version, player["perks"]["styles"][1]['style'])
            player_data['Item0'] = GI.getItemImage(version, player['item0'])
            player_data['Item1'] = GI.getItemImage(version, player['item1'])
            player_data['Item2'] = GI.getItemImage(version, player['item2'])
            player_data['Item3'] = GI.getItemImage(version, player['item3'])
            player_data['Item4'] = GI.getItemImage(version, player['item4'])
            player_data['Item5'] = GI.getItemImage(version, player['item5'])
            player_data['Item6'] = GI.getItemImage(version, player['item6'])
            player_data['Summoner1'] = GI.getSummonerSpellImage(version, player['summoner1Id'])
            player_data['Summoner2'] = GI.getSummonerSpellImage(version, player['summoner2Id'])

            players_info.append(player_data)
            player_data = {}
        
        match_players_info.append(players_info)

    return match_players_info

#------------------------------------------------------------------------------------------------------