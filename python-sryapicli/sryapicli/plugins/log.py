import omegaclient

from sryapicli.plugin_helpers import SRYClientPlugin


class LogPlugin(SRYClientPlugin):

    def register(self):
        self.set_command('log', help='search log command list')
        # sub_command: search
        log_search_parser = self.add_action('search', help='search app controller log')
        log_search_parser.add_argument('--clusterid', dest='cluster_id', type=int, required=True)
        log_search_parser.add_argument('--appname', dest='app_name', type=str, required=True)
        log_search_parser.add_argument('--start', dest='start_time', type=str, required=True)
        log_search_parser.add_argument('--end', dest='end_time', type=str, required=True)
        log_search_parser.add_argument('--from', dest='data_from', type=int, required=True)
        log_search_parser.add_argument('--size', dest='data_size', type=int, required=True)
        log_search_parser.add_argument('--ipport', dest='ipport', type=list)
        log_search_parser.add_argument('--source', dest='source', type=list)
        log_search_parser.add_argument('--keyword', dest='keyword', type=str)
        log_search_parser.set_defaults(func=self._get_app_logs)

        # sub_command: search_log_context
        search_log_context_parser = self.add_action('search_log_context', help='retrieve app log context')
        search_log_context_parser.add_argument('--clusterid', dest='cluster_id', type=int, required=True)
        search_log_context_parser.add_argument('--appname', dest='app_name', type=str, required=True)
        search_log_context_parser.add_argument('--ipport', dest='ipport', type=str, required=True)
        search_log_context_parser.add_argument('--source', dest='source', type=str, required=True)
        search_log_context_parser.add_argument('--timestamp', dest='timestamp', type=str, required=True)
        search_log_context_parser.add_argument('--counter', dest='counter', type=int, required=True)
        search_log_context_parser.set_defaults(func=self._get_app_context)

    def _get_app_logs(self, args):
        configs = self._get_config()
        cluster_id = args.cluster_id
        appname = args.app_name
        start = args.start_time
        end = args.end_time
        data_from = args.data_from
        data_size = args.data_size
        data = {
            'clusterid': cluster_id,
            'appname': appname,
            'start': start,
            'end': end,
            'from': data_from,
            'size': data_size
        }
        if args.ipport:
            data.update({'ipport': args.ipport})
        if args.source:
            data.update({'source': args.source})
        if args.keyword:
            data.update({'keyword': args.keyword})
        omega_client = omegaclient.OmegaClient(configs['host'], None, None, token=configs['token'])
        return omega_client.get_app_logs(**data)

    def _get_app_context(self, args):
        configs = self._get_config()
        data = {
            'clusterid': args.cluster_id,
            'appname': args.app_name,
            'ipport': args.ipport,
            'source': args.source,
            'timestamp': args.timestamp,
            'counter': args.counter
        }
        omega_client = omegaclient.OmegaClient(configs['host'], None, None, token=configs['token'])
        return omega_client.get_app_context(**data)
