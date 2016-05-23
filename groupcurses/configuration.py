import os
import configparser

class Configuration:
    def __init__(self):
        self.config = configparser.SafeConfigParser()
        self.config.read(os.path.abspath('.gitcursesrc'))
        self.api_key = self.config.get('client', 'api_key')


