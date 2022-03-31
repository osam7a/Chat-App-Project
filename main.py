from flask import Flask, render_template

__version__ = '0.1 beta'

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('home.html')

@app.route('/register')
def register(username, password):
    pass

@app.route('/login')
def register(username, password):
    pass

@app.route('/enterChannel')
def enterChannel(chID, userID):
    pass

@app.route('/createChannel')
def createChannel(chName, chPassword = 'NoPassword'):
    pass

if __name__ == '__main__':
    app.run('0.0.0.0', 3030)