import argparse, getpass
from sryapicli.plugin_helpers import SRYClientPlugin
import omegaclient


class PasswordPromptAction(argparse.Action):
    def __init__(self,
             option_strings,
             dest=None,
             nargs=0,
             default=None,
             required=False,
             type=None,
             metavar=None,
             help=None):
        super(PasswordPromptAction, self).__init__(
             option_strings=option_strings,
             dest=dest,
             nargs=nargs,
             default=default,
             required=required,
             metavar=metavar,
             type=type,
             help=help)

    def __call__(self, parser, args, values, option_string=None):
        password = getpass.getpass()
        setattr(args, self.dest, password)


class AuthPlugin(SRYClientPlugin):

    def register(self):

        # command: login
        parser_auth = self.parser.add_parser('login', help="login with user email and password, api server is required")
        authen_group = parser_auth.add_argument_group('authentication')
        authen_group.add_argument("--host", dest="host", type=str, required=True)
        authen_group.add_argument("--email", dest="email", type=str, required=True)
        authen_group.add_argument("--password", dest="password", action=PasswordPromptAction, type=str, required=True)
        parser_auth.set_defaults(func=self._authen_handler)

        # command: logout
        parser_logout = self.parser.add_parser('logout', help="delete login user's token, return code 0 if success")
        parser_logout.set_defaults(func=self._logout_handler)

    def _authen_handler(self, args): 
        email = args.email
        password = args.password
        host = args.host
        omega_client = omegaclient.OmegaClient(host, email, password)
        token_json = omega_client.get_token(email, password)
        if (token_json['code'] == 0):
            configs = {'host': host}
            configs.update(token_json['data']) 
            self._save_config(configs)
        return token_json

    def _logout_handler(self, args):
        configs = self._get_config()
        omega_client = omegaclient.OmegaClient(configs['host'], None, None, token=configs['token'])
        self._delete_config()
        return omega_client.delete_token()
