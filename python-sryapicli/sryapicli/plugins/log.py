import omegaclient

from sryapicli.plugin_helpers import SRYClientPlugin


class LogPlugin(SRYClientPlugin):

    def register(self):
        self.set_command('log', help='search log command list')
        # sub_command: search
        log_search_parser = self.add_action('search', help='search app controller log')
        log_search_parser.add_argument('--cluster_id', dest='cluster_id', type=int, required=True)
        log_search_parser.add_argument('--app_name', dest='app_name', type=str, required=True)
        log_search_parser.add_argument('--start', dest='start_time', type=str, required=True)
        log_search_parser.add_argument('--end', dest='end_time', type=str, required=True)
        log_search_parser.add_argument('--form', dest='form', type=int)
        log_search_parser.add_argument('--size', dest='size', type=int)
        log_search_parser.add_argument('--ipport', dest='ipport', type=list)
        log_search_parser.add_argument('--source', dest='source', type=list)
        log_search_parser.add_argument('--keyword', dest='keyword', type=str)
        log_search_parser.set_defaults(func=self._get_app_logs)

        # sub_command: search_log_context
        search_log_context_parser = self.add_action('search_log_context', help='retrieve app log context')
        search_log_context_parser.add_argument('--cluster_id', dest='cluster_id', type=int, required=True)
        search_log_context_parser.add_argument('--app_name', dest='app_name', type=str, required=True)
        search_log_context_parser.add_argument('--ipport', dest='ipport', type=str)
        search_log_context_parser.add_argument('--source', dest='source', type=str)
        search_log_context_parser.add_argument('--timestamp', dest='timestamp', type=str)
        search_log_context_parser.add_argument('--count', dest='count', type=int)
        search_log_context_parser.set_defaults(func=self._get_app_context)

    def _get_app_logs(self, args):
        configs = self._get_config()
        cluster_id = args.cluster_id
        appname = args.app_name
        start = args.start_time
        end = args.end_time
        data = {
            'clusterid': cluster_id,
            'appname': appname,
            'start': start,
            'end': end,
        }
        if args.form:
            data.update({'form': args.form})
        if args.size:
            data.update({'size': args.size})
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
        cluster_id = args.cluster_id
        app_name = args.app_name
        data = {
            'clusterid': cluster_id,
            'appname': app_name
        }
        if args.ipport:
            data.update({'ipport': args.ipport})
        if args.source:
            data.update({'source': args.source})
        if args.timestamp:
            data.update({'timestamp': args.timestamp})
        if args.count:
            data.update({'count': args.count})
        omega_client = omegaclient.OmegaClient(configs['host'], None, None, token=configs['token'])
        return omega_client.get_app_context(**data)
