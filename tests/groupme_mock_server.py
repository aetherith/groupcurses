"""
Mock implementation of the GroupMe public API.

This application exists to help test the chat application GroupCurses. It
implements the API defined at https://dev.groupme.com/docs/v3 and provides mock
responses to queries.
"""
from functools import wraps

from flask import Flask
from flask import request
from flask import jsonify

import groupme_mock_config

app = Flask(__name__)

def checks_auth_token(f):
    """
    A decorator to replicate the authentication token checking done by GroupMe.

    Compares the passed value to the value loaded from groupme_mock_config and
    only allows the request to complete if it matches.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token or token != groupme_mock_config.correct_api_key:
            def authentication_error(*args, **kwargs):
                message = {
                    "meta": {
                        "code": 401,
                        "errors": ["unauthorized"]
                    },
                    "response": None
                }
                resp = jsonify(message)
                resp.status_code = 401
                return resp
            return authentication_error()
        return f(*args, **kwargs)
    return decorated

@app.route('/')
@checks_auth_token
def hello_world():
    return jsonify(response={
        'text': 'Hello, world!'
    })

@app.route('/groups')
@checks_auth_token
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

    Returns 202 Accepted.
    """
    pass

@app.route('/groups/<gid>/members/results/<rid>')
def get_group_member_addition_results(gid, rid):
    """
    Get membership results from an add call.
    """
    pass

@app.route('/groups/<gid>/members/<mid>/remove', methods=['POST'])
def remove_group_member(gid, mid):
    """
    Remove a member (or yourself) from a group.

    Note: The creator of the group cannot be removed from the group.
    URL Parameters:
    :param membership_id - The 'id' value from the 'members' key of the group
    JSON, not the 'user_id'.
    """
    pass

@app.route('/groups/<gid>/memberships/update', methods=['POST'])
def update_user_nickname_in_group(gid):
    """
    Update your nickname in a group.

    The nickname must be between 1 and 50 characters.
    """
    pass

@app.route('/groups/<gid>/messages')
def get_group_messages(gid):
    """
    Retrieve messages for a group.

    By default, messages are returned in groups of 20, ordered by 'created_at'
    descending. This can be raised or lowered by passing a 'limit' parameter, up
    to a maximum of 100 messages.

    Messages can be scanned by providing a message ID as either the 'before_id',
    'since_id', or 'after_id' parameter. If 'before_id' is provided, then
    messages immediately preceding the given message will be returned, in
    descending order. This can be used to continually page back through a
    group's messages.

    The 'after_id' parameter will return messages taht immediately follow a
    given message, this time in ascending order.

    Finally, the 'since_id' parameter also returns messages crated after the
    given message, but it retrieves only the most recent messages. For example,
    if more than twenty (20) messages are created after the 'since_id' message,
    using this parameter will omit the messages that immediately follow the
    given message returning only the most recent twenty.

    If no messages are found (e.g. when filtering with 'before_id') we return
    HTTP code 304.

    URL Parameters:
    :param before_id
    :param since_id
    :param after_id
    :param limit
    """
    pass

@app.route('/groups/<gid>/messages', methods=['POST'])
def create_group_message(gid):
    """
    Send a message to a group.

    If you want to attach an image, you must first process it through the
    GroupMe image service.

    JSON Parameters:
    :param source_guid - Client-side ID for messages. This can be used by
        clients to set their own identifiers on messages, but the server also
        scans these for de-duplication. If two messsages are sent with the same
        'source_guid' within one minute of each other, the second message will
        fail with a 409 Conflict response.
    :param text - Optional if there is at least one attachment. The maximum
        length is 1000 characters.
    :param attachments - An array of attachment objects. You may have more than
        one of any type of attachment, provided clients can display them.
        - Images
            :param type - "image"
            :param url - Must be an image service (i.groupme.com) URL
        - Location
            :param type - "location"
            :param name
            :param lat
            :param lng
        - Split (?)
            :param type - "split"
            :param token
        - Emoji
            :param type - "emoji"
            :param placeholder
            :param charmap array
                :param pack_id
                :param offset
    """
    pass

@app.route('/chats')
def index_direct_message_conversations():
    """
    Returns a paginated list of direct message chats, or conversations, sorted
    by 'updated_at' descending.

    URL Parameters:
    :param page - page number
    :param per_page - number of chats per page
    """
    pass

@app.route('/direct_messages')
def get_direct_messages():
    """
    Fetch direct messages between two users.

    DMs are returned in groups of 20, ordered by 'created_at' descending.

    If no messages are found (e.g. when filtering with 'since_id') we return
    code 304.

    URL Parameters:
    :param other_user_id - The other participant in the conversation
    :param before_id - Returns 20 messages created before the given message ID
    :param since_id - Returns 20 messages created after the given message ID
    """
    pass

@app.route('/direct_messages', methods=['POST'])
def send_direct_message():
    """
    Send a DM to another user.

    JSON Parameters:
    :param source_guid
    :param recipient_id
    :param text
    :param attachments
    """
    pass

@app.route('/users/me')
def get_current_user_info():
    """
    Get details about the authenticated user.
    """
    pass

@app.route('/users/update', methods=['POST'])
def update_current_user_info():
    """
    Update attributes about your own account.

    JSON Parameters:
    :param avatar_url
    :param name
    :param email
    :param zip_code
    """
    pass

@app.route('/blocks')
def get_current_user_blocks():
    """
    A list of contacts that you have blocked.

    These people cannot DM you.

    URL Parameters:
    :param user - your user ID
    """
    pass

@app.route('/blocks/between')
def get_blocks_between_users():
    """
    Requests block status between two users.

    URL Parameters:
    :param user - your user ID
    :param otherUser - other user's ID
    """
    pass

@app.route('/blocks/between', methods=['POST'])
def block_user():
    """
    Creates a block between you and specified contact.
    
    URL Parameters:
    :param user - your user ID
    :param otherUser - other user's ID
    """
    pass

@app.route('/blocks', methods=['DELETE'])
def unblock_user():
    """
    Removes block between you and specified user.

    URL Parameters:
    :param user - your user ID
    :param otherUser - other user's ID
    """
    pass
