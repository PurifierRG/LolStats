import requests
from helpers import cache

#------------------------------------------------------------------------------------------------------

def getUser(api, username, region):
    url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{username}'
    response = requests.get(url, params={'api_key':api})

    if response.status_code == 200:
        resp = response.json()
        return {
            'id': resp['id'],
            'accountId': resp['accountId'],
            'puuid': resp['puuid'],
            'name': resp['name']
        }
    elif response.status_code == 404:
        raise ValueError('Username Not Found')
    else:
        raise ValueError('API call failed')


def getRank(api, id, region):
    rankUrl = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{id}"
    rankResponse = requests.get(rankUrl, params={'api_key':api})

    if rankResponse.status_code != 200:
        raise ValueError('API call failed')
    
    rankResp = rankResponse.json()
    soloTier = 'Unranked'
    soloRank = ''
    flexTier = 'Unranked'
    flexRank = ''

    for entry in rankResp:
        if entry['queueType'] == 'RANKED_SOLO_5x5':
            soloTier = entry['tier']
            soloRank = entry['rank']
        elif entry['queueType'] == 'RANKED_FLEX_SR':
            flexTier = entry['tier']
            flexRank = entry['rank']

    soloUrl = constructRankUrl(soloRank)
    flexUrl = constructRankUrl(flexRank)

    # flexTier = rankResp[0]['tier']
    # flexRank = rankResp[0]['rank']
    # soloTier = rankResp[1]['tier']
    # soloRank = rankResp[1]['rank']

    # rankResp = {'SoloTier': soloTier, 'SoloRank': soloRank, 'FlexTier': flexTier, 'FlexRank': flexRank}
    # url = {
    #     'SoloUrl': f"https://leagueoflegends.fandom.com/wiki/Rank_(League_of_Legends)?file=Season_2022_-_{rankResp['SoloRank']}.png",
    #     'FlexUrl': f"https://leagueoflegends.fandom.com/wiki/Rank_(League_of_Legends)?file=Season_2022_-_{rankResp['FlexRank']}.png"
    # }
    # return url

    return {'SoloTier': soloTier, 'SoloRank': soloRank, 'SoloUrl': soloUrl, 'FlexTier': flexTier, 'FlexRank': flexRank, 'FlexUrl': flexUrl}


def constructRankUrl(rank):
    if not rank:
        return ''

    return f"https://leagueoflegends.fandom.com/wiki/Rank_(League_of_Legends)?file=Season_2022_-_{rank}.png"
#------------------------------------------------------------------------------------------------------