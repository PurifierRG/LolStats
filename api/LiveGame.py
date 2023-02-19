import requests

def getLiveGameInfo(region, account_id, api):
    endpoint = f"https://{region}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{account_id}"
    response = requests.get(endpoint, params={'api_key':api})
    if response.status_code == 200:
        game_data = response.json()
        print("The following summoners are in the game:")
        for participant in game_data["participants"]:
            print(participant["summonerName"])
    else:
        print("The summoner is not currently in a live game.")

    