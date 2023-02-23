import requests 
from helpers import GenericImages as GI

def getLiveGameInfo(region, summonerID, api_key, version):
    endpoint = f"https://{region}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summonerID}"
    response = requests.get(endpoint, params={'api_key': api_key})
    
    if response.status_code != 200:
        print("The summoner is not currently in a live game.")
        return []

    data = response.json()
    players_info = []

    for player in data['participants']:
        player_data = {}

        player_data['PlayerName'] = player['summonerName']

        player_data['Winrate'] = getWinRate(player['summonerID'], api_key)
        
        player_data['ChampionID'] = player['championId']
        champList = []
        champList.append(player_data['ChampionID'])
        champInfo = getChampsInfo(version, champList)
        player_data['ChampionName'] = champInfo[0]['ChampionName']
        player_data['ChampionImage'] = GI.getChampImage(player_data['ChampionName'], version)

        player_data['PlayerTeam'] = 'Blue' if player['teamId'] == 100 else 'Red'

        player_data['Keystone'] = GI.getRuneImage(player["perks"]["perkIds"][0], version)
        player_data['SecondaryRune'] = GI.getRuneImage(player["perks"]["perkSubStyle"], version)

        player_data['Summoner1'] = GI.getSummonerSpellImage(player['spell1Id'], version)
        player_data['Summoner2'] = GI.getSummonerSpellImage(player['spell2Id'], version)

        players_info.append(player_data)

    return players_info


def getChampsInfo(version, champID):
    url = f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
    response = requests.get(url)
    response = response.json()

    ChampInfo = []
    for champ in response['data']:
        if int(response['data'][champ]['key']) in champID:
            ChampDetails = {}
            ChampDetails['ChampionName'] = response['data'][champ]['id']
            ChampInfo.append(ChampDetails)
    print(ChampInfo)
    return ChampInfo

def getWinRate(summonerID, api):
    url = f"https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summonerID}"
    response = requests.get(url, params={'api_key': api})

    for queue in response.json():
        if queue["queueType"] == "RANKED_SOLO_5x5":
            wins = queue["wins"]
            losses = queue["losses"]
            winrate = wins / (wins + losses)

    return winrate
