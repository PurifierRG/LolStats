import requests, os
from dotenv import load_dotenv

def getMatchID(puuid, shard):
    url = f"https://{shard}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    response = requests.get(url, params={'api_key':api})