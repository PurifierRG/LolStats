from flask import Flask, render_template, url_for, request
from api import UserID, MatchHistory
from dotenv import load_dotenv
import os

#------------------------------------------------------------------------------------------------------
api = os.getenv('API_KEY')
#------------------------------------------------------------------------------------------------------

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def home():
    return render_template('home.html', title='LolStat - Home')


@app.route('/lol', methods=['POST'])
def lol():
    username = str(request.form['username'])
    region = str(request.form['region'])
    version = MatchHistory.getVersion(api, region)
    shard = MatchHistory.getShard(region)
    response = UserID.getUser(api, username, region)
    match_ids = MatchHistory.getMatchIDs(api, shard, response['puuid'],)
    match_details = MatchHistory.getMatchDetails(api, shard, match_ids)
    match_player_details = MatchHistory.getMatchPlayersDetails(match_details, version)
    match_info = MatchHistory.getMatchInfo(match_details)
    return render_template('MatchHistory.html', title=f'{username} - Match History', Player_Details=match_player_details, Match_Details=match_info, user=response['name'], len=len(match_player_details))


#------------------------------------------------------------------------------------------------------

@app.route('/test', methods=['POST'])
def loljson():
    username = str(request.form['username'])
    region = str(request.form['region'])
    shard = 'sea'
    response = UserID.getUser(api, username, region)
    match_ids = MatchHistory.getMatchIDs(api, shard, response['puuid'],)
    match_details = MatchHistory.getMatchDetails(api, shard, match_ids)
    match_player_details = MatchHistory.getMatchPlayersDetails(match_details)
    match_info = MatchHistory.getMatchInfo(match_details)
    return match_details
     
#------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')