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

    soloRank = {}
    flexRank = {}

    for queue in rankResp:
        if queue['queueType'] == 'RANKED_SOLO_5x5':
            soloRank['rank'] = queue['tier']
            soloRank['division'] = queue['rank']
            soloRank['lp'] = queue['leaguePoints']
            soloRank['wins'] = queue['wins']
            soloRank['losses'] = queue['losses']
            soloRank['winRate'] = calculateWinRate(soloRank['wins'], soloRank['losses'])
            soloRank['rankIMG'] = rankImage(soloRank['rank'])
        elif queue['queueType'] == 'RANKED_FLEX_SR':
            flexRank['rank'] = queue['tier']
            flexRank['division'] = queue['rank']
            flexRank['lp'] = queue['leaguePoints']
            flexRank['wins'] = queue['wins']
            flexRank['losses'] = queue['losses']
            flexRank['winRate'] = calculateWinRate(flexRank['wins'], flexRank['losses'])
            flexRank['rankIMG'] = rankImage(flexRank['rank'])

    return {'Solo': soloRank, 'Flex': flexRank}


def calculateWinRate(wins, loss):
    if not wins:
        return 0
    elif not loss:
        return 100
    else:
        return round(wins/(wins + loss) * 100, 2)


def rankImage(rank):
    if not rank:
        return None
    else:
        return f"Season2022-{rank}.webp"

#------------------------------------------------------------------------------------------------------