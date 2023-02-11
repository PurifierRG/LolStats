from flask import Flask, render_template, url_for, request
from api import UserID

#------------------------------------------------------------------------------------------------------
app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def home():
    return render_template('home.html')


@app.route('/lol', methods=['POST'])
def lol():
    username = str(request.form['username'])
    region = str(request.form['region'])
    response = UserID.getUser(username, region)
    return render_template('index.html', result=response)
     
#------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')