import requests
from MatchHistory import getMatchPlayersDetails


def getLiveGameInfo(region, account_id, api, version):
    endpoint = f"https://{region}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{account_id}"
    response = requests.get(endpoint, params={'api_key': api})
    if response.status_code == 200:
        data = response.json()
        #   Type of data returned :-
        #         {
        #   "gameId": 1234567890,
        #   "mapId": 11,
        #   "gameMode": "CLASSIC",
        #   "gameType": "MATCHED_GAME",
        #   "gameQueueConfigId": 420,
        #   "participants": [
        #     {
        #       "teamId": 100,
        #       "spell1Id": 4,
        #       "spell2Id": 7,
        #       "championId": 64,
        #       "profileIconId": 29,
        #       "summonerName": "Summoner1",
        #       "bot": false,
        #       "summonerId": "abcdefghijk",
        #       "perks": {
        #         "perkIds": [8010, 9111, 9103, 8299],
        #         "perkStyle": 8000,
        #         "perkSubStyle": 8200
        #       }
        #     },
        #     {
        #       "teamId": 200,
        #       "spell1Id": 14,
        #       "spell2Id": 4,
        #       "championId": 86,
        #       "profileIconId": 23,
        #       "summonerName": "Summoner2",
        #       "bot": false,
        #       "summonerId": "lmnopqrstuv",
        #       "perks": {
        #         "perkIds": [8439, 8463, 8444, 8451],
        #         "perkStyle": 8400,
        #         "perkSubStyle": 8400
        #       }
        #     },
        #     ...
        #   ],
        #   "observers": {
        #     "encryptionKey": "abcdefghijklmnopqrstuvwxyz012345"
        #   },
        #   "platformId": "NA1",
        #   "gameStartTime": 1622669266000,
        #   "gameLength": 2324
        # }

        live_player_info = getMatchPlayersDetails(data, version)
        return live_player_info
    else:
        print("The summoner is not currently in a live game.")
