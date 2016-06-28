"""
Mock implementation of the GroupMe public API.

This application exists to help test the chat application GroupCurses. It
implements the API defined at https://dev.groupme.com/docs/v3 and provides mock
responses to queries.
"""
from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify(response={
        'text': 'Hello, world!'
    })

@app.route('/groups')
def index_groups():
    """
    List the authenticated user's active groups.

    :param page integer - Fetch a particular page of results. Defaults to 1.
    :param per_page integer - Define page size. Defaults to 10.
    """
    page = request.args.get('page')
    per_page = request.args.get('per_page')

@app.route('/groups/former')
def former_groups():
    """
    List the groups you have left but can rejoin.
    """
    pass

@app.route('/groups/<gid>')
def show_group(gid):
    """
    Load a specific group.
    """
    pass

@app.route('/groups', methods=['POST'])
def create_group():
    """
    Create a new group.

    Accepts a JSON object with the following keys as input.
    :param name
    :param description
    :param image_url
    :param share
    """
    pass

@app.route('/groups/<gid>/update', methods=['POST'])
def update_group(gid):
    """
    Update a group after creation.

    Accepts a JSON object with the following keys as input.
    :param name
    :param description
    :param image_url
    :param office_mode
    :param share
    """
    pass

@app.route('/groups/<gid>/destroy', methods=['POST'])
def destroy_group(gid):
    """
    Disband a group.

    This action is only available to the group creator.
    """
    pass

@app.route('/groups/<gid>/join/<share_token>', methods=['POST'])
def join_group(gid, share_token):
    """
    Join a shared group.
    """
    pass

@app.route('/groups/join', methods=['POST'])
def rejoin_group(gid):
    """
    Rejoin a group.

    Only works if you previously removed yourself.

    Requires the following URL parameters.
    :param group_id
    """
    pass

@app.route('/groups/<gid>/members/add', methods=['POST'])
def add_group_members(gid):
    """
    Add members to a group.
    """
    pass
