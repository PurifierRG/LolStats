from flask import Flask, render_template, url_for, request
from api import lolapi

#------------------------------------------------------------------------------------------------------

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def home():
    return "Hello World"


@app.route('/lol', methods=['POST','GET'])
def lol():
    username = request.args.get('username')
    response = lolapi.getUser(username)
    return response
    
#------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')