import requests

#------------------------------------------------------------------------------------------------------

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

    return ChampInfo

#------------------------------------------------------------------------------------------------------