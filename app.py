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
    return render_template('home.html')


@app.route('/lol', methods=['POST'])
def lol():
    username = str(request.form['username'])
    region = str(request.form['region'])
    shard = 'sea'
    response = UserID.getUser(api, username, region)
    match_ids = MatchHistory.getMatchIDs(api, shard, response['puuid'],)
    match_details = MatchHistory.getMatchDetails(api, shard, match_ids, type='UAT')
    return render_template('MatchHistory.html', Summoner=username, result=match_details)


#------------------------------------------------------------------------------------------------------

@app.route('/test', methods=['POST'])
def loljson():
    username = str(request.form['username'])
    region = str(request.form['region'])
    shard = 'sea'
    response = UserID.getUser(api, username, region)
    match_ids = MatchHistory.getMatchIDs(api, shard, response['puuid'],)
    match_details = MatchHistory.getMatchDetails(api, shard, match_ids, type='test')
    return match_details
     
#------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')