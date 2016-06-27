import os
import ruamel.yaml as yaml

class Configuration:
    def __init__(self):
        locations = [
            os.curdir,
            os.path.expanduser('~/.config/groupcurses'),
            os.path.expanduser('~'),
            '/etc/groupcurses',
            os.environ.get('GROUPCURSES_CONF'),
        ]
        for location in locations:
            try:
                with open(os.path.join(location, '.groupcursesrc'), 'r') as config_file:
                    raw_config = config_file.read()
                    try:
                        self.config = yaml.load(raw_config)
                        break
                    except yaml.YAMLError:
                        pass
            except IOError:
                pass
        self.api_key = self.config['groupme']['api_key']
