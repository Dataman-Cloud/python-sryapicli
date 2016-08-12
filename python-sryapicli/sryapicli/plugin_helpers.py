import json
import os, sys

CONFIG_FILE = '.sryapi-cli.json'


class SRYClientPlugin(object):
    """
    Abstract base class for plugins providing their own commands. Each subclass
    must implement `register` methods.
    """
    def __init__(self, runner):
        self.runner = runner

    def _before_register(self, parser):
        self.parser = parser

    def register(self):
        raise NotImplementedError('Plugin must implement `register` method.')

    def set_command(self, *args, **kwargs):
        """Define new command.
        For accepted arguments, see `argparse.ArgumentParser.add_argument`.
        """
        if 'help' not in kwargs:
            kwargs['help'] = ''
        cmd = self.parser.add_parser(*args, **kwargs)
        self.subparsers = cmd.add_subparsers(metavar='ACTION')

    def add_action(self, *args, **kwargs):
        return self.subparsers.add_parser(*args, **kwargs)

    def _save_config(self, configs):
        with open(CONFIG_FILE, 'w') as f:
            f.write(json.dumps(configs))

    def _get_config(self):
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    config_json = json.loads(f.read())
                    return config_json
            else:
                raise IOError
        except IOError:
            print('Please authenticate with email and password firstly')
            sys.exit(1)

    def _delete_config(self):
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
