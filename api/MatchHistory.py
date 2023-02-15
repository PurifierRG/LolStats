import requests

#------------------------------------------------------------------------------------------------------
def getShard(region):
    region_to_shard = {
    'na1': 'AMERICAS',
    'br1': 'AMERICAS',
    'la1': 'AMERICAS',
    'la2': 'AMERICAS',
    'oc1': 'AMERICAS',
    'jp1': 'ASIA',
    'kr': 'ASIA',
    'eun1': 'EUROPE',
    'euw1': 'EUROPE',
    'ru': 'EUROPE',
    'tr1': 'EUROPE',
    'sg2': 'SEA',
    'vn2': 'SEA',
    'tr1': 'SEA',
    'th2': 'SEA',
    'ph2': 'SEA',
    'pbe1': 'PBE'
    }
    shard = region_to_shard.get(region, None)

    if shard:
        return shard
    else:
        print(f"Unable to find shard for region: {region}")


def getVersion(api, region):
    versionRegion = ''.join((x for x in region if not x.isdigit()))
    response = requests.get(f"https://ddragon.leagueoflegends.com/realms/{versionRegion}.json", params={'api_key':api})
    if response.status_code == 200:
        data = response.json()
        version = data['v']
        return str(version)
    else:
        print(f"Error getting current version, status code: {response.status_code}")

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

    
def getRank(api, id, region):
    rankUrl = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{id}"
    rankResponse = requests.get(rankUrl, params={'api_key':api})
    rankResp = rankResponse.json()
    flexTier = rankResp[0]['tier']
    flexRank = rankResp[0]['rank']
    soloTier = rankResp[1]['tier']
    soloRank = rankResp[1]['rank']
    rankResp = {'soloTier': soloTier, 'soloRank': soloRank, 'flexTier': flexTier, 'flexRank': flexRank}
    url = {
        'soloUrl': f"https://leagueoflegends.fandom.com/wiki/Rank_(League_of_Legends)?file=Season_2022_-_{rankResp['soloRank']}.png",
        'flexUrl': f"https://leagueoflegends.fandom.com/wiki/Rank_(League_of_Legends)?file=Season_2022_-_{rankResp['flexRank']}.png"
    }
    return url


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

def getItem(itemId, version):
    if itemId == 0:
        itemUrl = "http://ddragon.leagueoflegends.com/cdn/5.5.1/img/ui/champion.png"
    else:
        itemUrl = f"http://ddragon.leagueoflegends.com/cdn/{version}/img/item/{itemId}.png"
    return itemUrl

SPELL_MAP = {
    1: "SummonerBoost",
    3: "SummonerExhaust",
    4: "SummonerFlash",
    6: "SummonerHaste",
    7: "SummonerHeal",
    11: "SummonerSmite",
    12: "SummonerTeleport",
    13: "SummonerMana",
    14: "SummonerDot",
    21: "SummonerBarrier",
    30: "SummonerPoroRecall",
    31: "SummonerPoroThrow",
    32: "SummonerSnowball",
    39: "SummonerSnowURFSnowball_Mark",
    54: "Summoner_UltBookPlaceholder",
    55: "Summoner_UltBookSmitePlaceholder"
}

def getSummonerSpell(spellId, version):
    spellName = SPELL_MAP.get(spellId, "None")
    spellUrl = f"http://ddragon.leagueoflegends.com/cdn/{version}/img/spell/{spellName}.png"
    return spellUrl

def getChampImage(champName, version):
    url = f"http://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{champName}.png"
    return url

def getRuneImage(rune_id, version):
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/runesReforged.json"
    
    response = requests.get(url)
    rune_data = response.json()

    for tree in rune_data:
        if tree['id'] == rune_id:
            rune_image = f"http://ddragon.leagueoflegends.com/cdn/img/{tree['icon']}"
            return rune_image
        for slot in tree['slots']:
            for rune in slot['runes']:
                if rune['id'] == rune_id:
                    rune_image = f"https://ddragon.leagueoflegends.com/cdn/img/{rune['icon']}"
                    return rune_image


def getMatchPlayersDetails(data, version):
    match_info = getMatchInfo(data)
    match_players_info = []

    # print(data[0]['info']['participants'])

    for i in range(len(data)):
        players_info = []
        player_data = {}

        for player in data[i]['info']['participants']:
            player_data['Player Name'] = player['summonerName']
            player_data['Champion Image'] = getChampImage(player['championName'], version)
            player_data['Champion'] = player['championName']
            player_data['keystone'] = getRuneImage(player["perks"]["styles"][0]["selections"][0]["perk"], version)
            player_data['secondaryStyle'] = getRuneImage(player["perks"]["styles"][1]['style'], version)
            player_data['item0'] = getItem(player['item0'], version)
            player_data['item1'] = getItem(player['item1'], version)
            player_data['item2'] = getItem(player['item2'], version)
            player_data['item3'] = getItem(player['item3'], version)
            player_data['item4'] = getItem(player['item4'], version)
            player_data['item5'] = getItem(player['item5'], version)
            player_data['item6'] = getItem(player['item6'], version)
            player_data['summoner1'] = getSummonerSpell(player['summoner1Id'], version)
            player_data['summoner2'] = getSummonerSpell(player['summoner2Id'], version)
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
