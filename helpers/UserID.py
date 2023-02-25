import requests
from helpers import cache

#------------------------------------------------------------------------------------------------------

def getUser(api, region, username):
    url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{username}'
    response = requests.get(url, params={'api_key':api})

    if response.status_code == 200:
        resp = response.json()
        return {
            'summonerID': resp['id'],
            'accountID': resp['accountId'],
            'puuID': resp['puuid'],
            'name': resp['name']
        }
    elif response.status_code == 404:
        raise ValueError('Username Not Found')
    else:
        raise ValueError('API call failed')


def getRankInfo(api, region, summonerID):
    rankUrl = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summonerID}"
    rankResponse = requests.get(rankUrl, params={'api_key':api})

    if rankResponse.status_code != 200:
        raise ValueError('API call failed')
    
    rankResp = rankResponse.json()
    soloRank = {'rank': 'Unranked', 'division': '', 'lp': 0, 'losses': 0, 'wins': 0, 'winRate': ''}
    flexRank = {'rank': 'Unranked', 'division': '', 'lp': 0, 'losses': 0, 'wins': 0, 'winRate': ''}

    for queue in rankResp:
        if queue['queueType'] == 'RANKED_SOLO_5x5':
            soloRank['rank'] = queue['tier']
            soloRank['division'] = queue['rank']
            soloRank['lp'] = queue['leaguePoints']
            soloRank['wins'] = queue['wins']
            soloRank['losses'] = queue['losses']
            soloRank['winRate'] = round((soloRank['wins'] / (soloRank['wins'] + soloRank['losses'])) * 100, 2)
            soloRank['rankIMG'] = constructRankUrl(soloRank['rank'])
        elif queue['queueType'] == 'RANKED_FLEX_SR':
            flexRank['rank'] = queue['tier']
            flexRank['division'] = queue['rank']
            flexRank['lp'] = queue['leaguePoints']
            flexRank['wins'] = queue['wins']
            flexRank['losses'] = queue['losses']
            flexRank['winRante'] = round((flexRank['wins'] / (flexRank['wins'] + flexRank['losses'])) * 100, 2)
            flexRank['rankIMG'] = constructRankUrl(flexRank['rank'])

    return {'Solo': soloRank, 'Flex': flexRank}


def constructRankUrl(rank): # not working properly for now
    if not rank:
        return ''

    return f"https://leagueoflegends.fandom.com/wiki/Rank_(League_of_Legends)?file=Season_2022_-_{rank}.png"

#------------------------------------------------------------------------------------------------------