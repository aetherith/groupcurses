import urwid
import requests

class API():
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.groupme.com/v3/'
        self.base_params = {'token': self.api_key}

    def get(self, route, user_params=None):
        params = self.base_params.copy()
        if user_params is not None:
            params.update(user_params)
        req = requests.get(self.base_url + route, params=params)
        resp = req.json()
        if req.status_code is 200:
            return resp['response']
        else:
            urwid.emit_signal(self, 'show-status-message', resp['meta']['errors'][0])
    def post(self, route, user_params=None, user_data=None):
        params = self.base_params.copy()
        if user_params is not None:
            params.update(user_params)
        if user_data is None:
            user_data = {}
        req = requests.post(self.base_url + route, params=params, json=user_data)
        
        resp = req.json()
        if req.status_code is 201:
            return resp['response']
        else:
            urwid.emit_signal(self, 'show-status-message', resp['meta']['errors'][0])
