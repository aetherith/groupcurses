from flask import Flask
from flask import jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify(response={
        'text': 'Hello, world!'
    })

@app.route('/groups')
def index_groups():
    pass
