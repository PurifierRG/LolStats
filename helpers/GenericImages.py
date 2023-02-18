import requests
from helpers import cache

#------------------------------------------------------------------------------------------------------

def getChampImage(champName, version):
    url = f"http://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{champName}.png"
    return url

#------------------------------------------------------------------------------------------------------

def getSummonerSpellImage(spellId, version):
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
    spellName = SPELL_MAP.get(spellId, "None")
    spellUrl = f"http://ddragon.leagueoflegends.com/cdn/{version}/img/spell/{spellName}.png"
    return spellUrl

#------------------------------------------------------------------------------------------------------

def getRuneImage(rune_id, version):
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/runesReforged.json"
    
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to retrieve rune data: {response.status_code}")
    
    rune_data = response.json()
    rune_images = {}

    for tree in rune_data:
        rune_images[tree['id']] = f"http://ddragon.leagueoflegends.com/cdn/img/{tree['icon']}"
        for slot in tree['slots']:
            for rune in slot['runes']:
                rune_images[rune['id']] = f"https://ddragon.leagueoflegends.com/cdn/img/{rune['icon']}"

    if rune_id not in rune_images:
        raise ValueError(f"Invalid rune id: {rune_id}")

    return rune_images.get(rune_id)

#------------------------------------------------------------------------------------------------------

def getItemImage(itemId, version):
    if itemId == 0:
        itemUrl = "http://ddragon.leagueoflegends.com/cdn/5.5.1/img/ui/champion.png"
    else:
        itemUrl = f"http://ddragon.leagueoflegends.com/cdn/{version}/img/item/{itemId}.png"
    return itemUrl

#------------------------------------------------------------------------------------------------------