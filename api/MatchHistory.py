import requests

#------------------------------------------------------------------------------------------------------

def getMatchIDs(api, shard, puuid):   
    url = f"https://{shard}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    response = requests.get(url, params={'api_key':api, 'count':5})
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
        match_info['Game Mode'] = key['info']['gameMode']
        match_info['Game Type'] = key['info']['gameType']
        match_info['Game Duration'] = key['info']['gameDuration']
        match_info['Game Time'] = f"{int(key['info']['gameDuration']/60)}m {key['info']['gameDuration']%60}s"
        match_info_list.append(match_info)
        match_info = {}
    
    return match_info_list

def getItem(itemId):
    if itemId == 0:
        itemUrl = "http://ddragon.leagueoflegends.com/cdn/5.5.1/img/ui/champion.png"
    else:
        itemUrl = f"http://ddragon.leagueoflegends.com/cdn/13.3.1/img/item/{itemId}.png"
    return itemUrl

def getSummonerSpell(spellId):
    if spellId == 21:
        spellName = "SummonerBarrier"
    elif spellId == 1:
        spellName = "SummonerBoost"
    elif spellId == 14:
        spellName = "SummonerDot"
    elif spellId == 3:
        spellName = "SummonerExhaust"
    elif spellId == 4:
        spellName = "SummonerFlash"
    elif spellId == 6:
        spellName = "SummonerHaste"
    elif spellId == 7:
        spellName = "SummonerHeal"
    elif spellId == 13:
        spellName = "SummonerMana"
    elif spellId == 30:
        spellName = "SummonerPoroRecall" 
    elif spellId == 31:
        spellName = "SummonerPoroThrow"
    elif spellId == 11:
        spellName = "SummonerSmite"
    elif spellId == 39:
        spellName = "SummonerSnowURFSnowball_Mark"
    elif spellId == 32:
        spellName = "SummonerSnowball"
    elif spellId == 12:
        spellName = "SummonerTeleport"
    elif spellId == 54:
        spellName = "Summoner_UltBookPlaceholder"
    elif spellId == 55:
        spellName = "Summoner_UltBookSmitePlaceholder"
    else:
        spellName = "None"
    print(spellName)
    spellUrl = f"http://ddragon.leagueoflegends.com/cdn/13.3.1/img/spell/{spellName}.png"
    return spellUrl


def getMatchPlayersDetails(data):
    match_info = getMatchInfo(data)
    match_players_info = []

    for i in range(len(data)):
        players_info = []
        player_data = {}

        for player in data[i]['info']['participants']:
            player_data['Player Name'] = player['summonerName']
            url = f"http://ddragon.leagueoflegends.com/cdn/13.3.1/img/champion/{player['championName']}.png"
            player_data['Champion Image'] = url
            player_data['Champion'] = player['championName']
            player_data['item0'] = getItem(player['item0'])
            player_data['item1'] = getItem(player['item1'])
            player_data['item2'] = getItem(player['item2'])
            player_data['item3'] = getItem(player['item3'])
            player_data['item4'] = getItem(player['item4'])
            player_data['item5'] = getItem(player['item5'])
            player_data['item6'] = getItem(player['item6'])
            player_data['summoner1'] = getSummonerSpell(player['summoner1Id'])
            player_data['summoner2'] = getSummonerSpell(player['summoner2Id'])
            player_data['Damage To Champions'] = player['totalDamageDealtToChampions']
            player_data['Damage Taken'] = player['totalDamageTaken']
            player_data['Lane Minions Killed'] = player['totalMinionsKilled']
            player_data['Neutral Minions Killed'] = player['neutralMinionsKilled']
            player_data['Total Minions Killed'] = player_data['Neutral Minions Killed'] + player_data['Lane Minions Killed']
            player_data['CS Per Minute'] = round(player_data['Total Minions Killed'] / ((match_info[i]['Game Duration'])/60), 2)
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
        
        match_players_info.append(players_info)

    return match_players_info
