import requests 
from helpers import GenericImages as GI
from api import Champions as Champs
from helpers import UserID as UID

# Queue IDs --------------------------------------------------------------------------------------------

# Solo Ranked         : 420
# Flex Ranked         : 440

# Normal Blind        : 430
# Normal Draft        : 400

# ARAM                : 450

# Co-op [Intro]       : 830
# Co-op [Beginner]    : 840
# Co-op [Intermediate]: 850

#------------------------------------------------------------------------------------------------------

def getLiveGameInfo(api, region, version, summonerID):
    endpoint = f"https://{region}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summonerID}"
    response = requests.get(endpoint, params={'api_key': api})
    
    if response.status_code != 200:
        print("The summoner is not currently in a live game.")
        return []

    data = response.json()

    players_info = []

    for player in data['participants']:
        player_data = {}

        player_data['PlayerName'] = player['summonerName']
        player_data['PlayerTeam'] = 'Blue' if player['teamId'] == 100 else 'Red'
        
        player_data['ChampionID'] = player['championId']
        champList = []
        champList.append(player_data['ChampionID'])
        champInfo = Champs.getChampsInfo(version, champList)
        player_data['ChampionName'] = champInfo[0]['ChampionName']
        player_data['ChampionImage'] = GI.getChampImage(version, player_data['ChampionName'])

        player_data['Keystone'] = GI.getRuneImage(version, player["perks"]["perkIds"][0])
        player_data['SecondaryRune'] = GI.getRuneImage(version, player["perks"]["perkSubStyle"])

        player_data['Summoner1'] = GI.getSummonerSpellImage(version, player['spell1Id'])
        player_data['Summoner2'] = GI.getSummonerSpellImage(version, player['spell2Id'])

        players_info.append(player_data)

    return players_info
