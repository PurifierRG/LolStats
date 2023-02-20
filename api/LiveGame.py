import requests
from helpers import GenericImages as GI

def getLiveGameInfo(region, account_id, api_key, version):
    endpoint = f"https://{region}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{account_id}"
    response = requests.get(endpoint, params={'api_key': api_key})
    
    if response.status_code != 200:
        print("The summoner is not currently in a live game.")
        return []

    data = response.json()
    players_info = []

    for player in data['participants']:
        player_data = {}
        player_data['PlayerName'] = player['summonerName']
        player_data['ChampionId'] = player['championId']
        player_data['PlayerTeam'] = 'Blue' if player['teamId'] == 100 else 'Red'

        player_data['Keystone'] = GI.getRuneImage(player["perks"]["perkIds"][0], version)
        player_data['SecondaryRune'] = GI.getRuneImage(player["perks"]["perkSubStyle"], version)

        player_data['Summoner1'] = GI.getSummonerSpellImage(player['spell1Id'], version)
        player_data['Summoner2'] = GI.getSummonerSpellImage(player['spell2Id'], version)

        players_info.append(player_data)

    return players_info