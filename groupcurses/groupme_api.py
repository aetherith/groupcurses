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

    def send_message(self):
        """
        Send a simple text message through the GroupMe API.
        """
        pass

    def get_messages(self):
        """
        Retrieve all new messages available from the endpoint.
        """
        pass

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
