import requests

#------------------------------------------------------------------------------------------------------

def getUser(api, username, region):
    if username != None:
        url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{username}'
        response = requests.get(url, params={'api_key':api})

        if response.status_code == 200:
            resp = response.json()
            name = resp['name']
            id = resp['id']
            accountId = resp['accountId']
            puuid = resp['puuid']
            resp = {'id': id, 'accountId': accountId, 'puuid': puuid, 'name': name}
            return resp
        else:
            raise ValueError('Username Not Found!')
    else:
        return "please fill the username"


def getRank(api, id, region):
    rankUrl = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{id}"
    rankResponse = requests.get(rankUrl, params={'api_key':api})
    rankResp = rankResponse.json()
    flexTier = rankResp[0]['tier']
    flexRank = rankResp[0]['rank']
    soloTier = rankResp[1]['tier']
    soloRank = rankResp[1]['rank']
    rankResp = {'SoloTier': soloTier, 'SoloRank': soloRank, 'FlexTier': flexTier, 'FlexRank': flexRank}
    url = {
        'SoloUrl': f"https://leagueoflegends.fandom.com/wiki/Rank_(League_of_Legends)?file=Season_2022_-_{rankResp['SoloRank']}.png",
        'FlexUrl': f"https://leagueoflegends.fandom.com/wiki/Rank_(League_of_Legends)?file=Season_2022_-_{rankResp['FlexRank']}.png"
    }
    return url

#------------------------------------------------------------------------------------------------------