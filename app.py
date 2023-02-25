from flask import Flask, render_template, url_for, redirect, request
import os
from dotenv import load_dotenv
from api import MatchHistory as MH
from api import LiveGame as LG
from helpers import GenericImages as GI
from helpers import RegionDetails as RD
from helpers import UserID as UID
from helpers import cache

#------------------------------------------------------------------------------------------------------
load_dotenv()
api = os.getenv('API_KEY')
#------------------------------------------------------------------------------------------------------

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def Home():
    Page_Info = {'Title': 'LolStat - Home'}
    return render_template('home.html', PAGE_INFO=Page_Info)

#------------------------------------------------------------------------------------------------------

@app.route('/lol', methods=['POST'])
def Lol():
    username = str(request.form['username'])
    region = str(request.form['region'])
    if username and region:
        return redirect(f"/lol/{region}/{username}")
    return "Please enter both username & password"


@app.route('/lol/<region>/<username>', methods=['GET'])
def MatchHistory(region, username):
    shard = RD.getShard(region)
    version = RD.getVersion(api, region)

    user_info = UID.getUser(api, region, username)

    match_ids = MH.getMatchIDs(api, shard, user_info['puuID'],)
    match_details = MH.getMatchDetails(api, shard, match_ids)
    match_info = MH.getMatchInfo(match_details)
    match_player_info = MH.getMatchPlayersDetails(version, match_details)

    live_player_info = LG.getLiveGameInfo(api, region, version, user_info['summonerID'])

    PageInfo = {
        'Title': f"{user_info['name']} - Match History",
        'Username': user_info['name'], 
        'len': len(match_player_info),
        'region': region 
    }
    return render_template('MatchHistory.html', PAGE_INFO=PageInfo, Player_Details=match_player_info, Match_Details=match_info)

# TEST ------------------------------------------------------------------------------------------------

@app.route('/test', methods=['POST'])
def Test():
    username = str(request.form['username'])
    region = str(request.form['region'])
    if username and region:
        return redirect(f"/test/{region}/{username}")
    return "Please enter both username & password"


@app.route('/test/<region>/<username>', methods=['GET'])
def TestJSON(region, username):
    shard = RD.getShard(region)
    version = RD.getVersion(api, region)

    user_info = UID.getUser(api, region, username)
    rankdetails = UID.getRankInfo(api, region, user_info['summonerID'])

    live_player_info = LG.getLiveGameInfo(api, region, version, user_info['summonerID'])

    match_ids = MH.getMatchIDs(api, shard, user_info['puuID'],)
    match_details = MH.getMatchDetails(api, shard, match_ids)
    match_info = MH.getMatchInfo(match_details)
    match_player_info = MH.getMatchPlayersDetails(version, match_details)
    
    return match_details

#------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')