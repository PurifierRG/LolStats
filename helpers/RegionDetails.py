import requests
from helpers import cache

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
        raise ValueError('Shard Not Found (Invalid Region)')

#------------------------------------------------------------------------------------------------------

def getVersion(api, region):
    versionRegion = ''.join((x for x in region if not x.isdigit()))
    response = requests.get(f"https://ddragon.leagueoflegends.com/realms/{versionRegion}.json", params={'api_key':api})
    if response.status_code == 200:
        data = response.json()
        version = data['v']
        return str(version)
    else:
        raise ConnectionError("Error getting current version, status code: {response.status_code}")

#------------------------------------------------------------------------------------------------------