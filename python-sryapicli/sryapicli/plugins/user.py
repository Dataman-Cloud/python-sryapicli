import argparse
from sryapicli.plugin_helpers import SRYClientPlugin
import omegaclient


class UserPlugin(SRYClientPlugin):

    def register(self):

        # command: me
        self.set_command('user', help='get user information')
        user_info_parser = self.add_action('info', help='show current login user information')
        user_info_parser.set_defaults(func=self._get_my_info)

    def _get_my_info(self, args):
        configs = self._get_config()
        omega_client = omegaclient.OmegaClient(configs['host'], None, None, token=configs['token'])
        return omega_client.get_user()
