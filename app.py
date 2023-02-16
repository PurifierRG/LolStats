from flask import Flask, render_template, url_for, redirect, request
from api import MatchHistory as MH
from helpers import GenericImages as GI
from helpers import RegionDetails as RD
from helpers import UserID as UID
from helpers import cache
from dotenv import load_dotenv
import os

from helpers import UserID

#------------------------------------------------------------------------------------------------------
api = os.getenv('API_KEY')
#------------------------------------------------------------------------------------------------------

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def Home():
    Page_Info = {'Title': 'LolStat'}
    return render_template('home.html', PAGE_INFO='LolStat - Home')

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

    user_info = UID.getUser(api, username, region)

    match_ids = MH.getMatchIDs(api, shard, user_info['puuid'],)
    match_details = MH.getMatchDetails(api, shard, match_ids)
    match_info = MH.getMatchInfo(match_details)
    match_player_info = MH.getMatchPlayersDetails(match_details, version)

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

    user_info = UID.getUser(api, username, region)

    match_ids = MH.getMatchIDs(api, shard, user_info['puuid'],)
    match_details = MH.getMatchDetails(api, shard, match_ids)
    match_info = MH.getMatchInfo(match_details)
    match_player_info = MH.getMatchPlayersDetails(match_details, version)
    
    return match_player_info
     
#------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')