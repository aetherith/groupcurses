import urwid
import requests

class GroupMeAPI():
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.groupme.com/v3/'
        self.base_params = {'token': self.api_key}

    def get(self, route, user_params=None):
        params = self.base_params.copy()
        if user_params is not None:
            params.update(user_params)
        try:
            req = requests.get(self.base_url + route, params=params)
            resp = req.json()
            if req.status_code is 200:
                return resp['response']
            else:
                urwid.emit_signal(self, 'show-status-message', resp['meta']['errors'][0])
        except requests.exceptions.ConnectionError:
            urwid.emit_signal(self, 'show-status-message', 'Failed to connect to API endpoint.')
            self.get(route, user_params)

    def post(self, route, user_params=None, user_data=None):
        params = self.base_params.copy()
        if user_params is not None:
            params.update(user_params)
        if user_data is None:
            user_data = {}
        try:
            req = requests.post(self.base_url + route, params=params, json=user_data)
            resp = req.json()
            if req.status_code is 201:
                return resp['response']
            else:
                urwid.emit_signal(self, 'show-status-message', resp['meta']['errors'][0])
        except requests.exceptions.ConnectionError:
            urwid.emit_signal(self, 'show-status-message', 'Failed to connect to API endpoint.')
            self.post(route, user_params, user_data)

    def send_message(self, conversation_type, cid, source_guid, message):
        """
        Send a simple text message through the GroupMe API.
        """
        if conversation_type == 'direct_message':
            message_data = {
                'direct_message': {
                    'source_guid': source_guid,
                    'recipient_id': cid,
                    'text': message[:1000],
                }        
            }
            return self.post('direct_messages', user_data=message_data)
        else:
            return False

    def get_messages(self, conversation_type, cid):
        """
        Retrieve all new messages available from the endpoint.
        """
        if conversation_type == 'direct_message':
            messages = self.get(
                'direct_messages',
                {'other_user_id': cid}
            )['direct_messages']
        elif conversation_type == 'group':
            messages = self.get('groups/' + cid + '/messages')['messages']
        messages.reverse()
        return messages

    def send_picture_message(self):
        """
        Thumbnail and send an image message through GroupMe API.
        """
        pass

    def download_picture_message(self):
        """
        Download a single picture message from GroupMe and save it locally.
        """
        pass
