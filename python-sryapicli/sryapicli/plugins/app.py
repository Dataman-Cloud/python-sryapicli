import argparse, json
import omegaclient
from sryapicli.plugin_helpers import SRYClientPlugin
ACTIONS = ['stop', 'start']


class AppPlugin(SRYClientPlugin):

    def register(self):
        self.set_command('app', help='omega-app api command list')

        # sub-commands: ['rollback', 'stop', 'start', 'stop_deploy', 'stop_scaling', 'redeploy']
        # now only implement stop, start sub-commands.
        for action in ACTIONS:
            action_parser = self.add_action(action, help=action + 'a specified app')
            action_parser.add_argument('--cluster_id', dest='cluster_id', type=int, required=True)
            action_parser.add_argument('--app_id', dest='app_id', type=int, required=True)
            action_parser.add_argument('--action', dest='action', default=action, help=argparse.SUPPRESS)
            action_parser.set_defaults(func=self._action_cluster_app)

        # sub-command: scale
        scale_parser = self.add_action('scale', help='scale instances for a specified app')
        scale_parser.add_argument('--cluster_id', dest='cluster_id', type=int, required=True)
        scale_parser.add_argument('--app_id', dest='app_id', type=int, required=True)
        scale_parser.add_argument('--instances', dest='instances', type=int, required=True)
        scale_parser.set_defaults(func=self._scale_app)

        # sub-command: update_version
        update_version_parser = self.add_action('update_version', help='update app version')
        update_version_parser.add_argument('--cluster_id', dest='cluster_id', type=int, required=True)
        update_version_parser.add_argument('--app_id', dest='app_id', type=int, required=True)
        update_version_parser.add_argument('--version_id', dest='version_id', type=int, required=True)
        update_version_parser.set_defaults(func=self._update_app_version)

        # sub-command: get_cluster_apps
        get_apps_parser = self.add_action('get_cluster_apps', help='list all apps for specified cluster' )
        get_apps_parser.add_argument('--cluster_id',dest='cluster_id', type=int, required=True)
        get_apps_parser.set_defaults(func=self._get_cluster_apps)

        # sub-command: create_cluster_apps
        create_cluster_apps_parser = self.add_action('create', help='create app under specified cluster')
        create_cluster_apps_parser.add_argument('--cluster_id', dest='cluster_id', type=int, help='Cluster identifier')
        create_cluster_apps_parser.add_argument('-f', '--file', help='bundle json containing new app info', type=argparse.FileType('r'), required=True)
        create_cluster_apps_parser.set_defaults(func=self._create_cluster_apps)

        # sub-command: get_cluster_app
        get_cluster_app_parser = self.add_action('get', help='list specified app information under specified cluster')
        get_cluster_app_parser.add_argument('--cluster_id', dest='cluster_id', type=int, required=True)
        get_cluster_app_parser.add_argument('--app_id', dest="app_id", type=int, required=True)
        get_cluster_app_parser.set_defaults(func=self._get_cluster_app)

        # sub-command: delete_cluster_app
        delete_cluster_app_parser = self.add_action('delete', help='Delete specified app under specified cluster')
        delete_cluster_app_parser.add_argument('--cluster_id', dest='cluster_id', type=int, required=True)
        delete_cluster_app_parser.add_argument('--app_id', dest="app_id", type=int, required=True)
        delete_cluster_app_parser.set_defaults(func=self._delete_cluster_app)

        # sub-command: get_user_apps
        get_user_apps_parser = self.add_action('get_my_apps', help='list all apps belong to me.')
        get_user_apps_parser.set_defaults(func=self._get_user_apps)

        # sub-command: get_user_apps_status
        get_user_apps_status_parser = self.add_action('get_my_app_status', help="list all app's status")
        get_user_apps_status_parser.set_defaults(func=self._get_user_apps_status)

        # sub-command: get_app_versions
        get_app_versions_parser = self.add_action('get_app_version', help='list all history versions for a specific app')
        get_app_versions_parser.add_argument('--cluster_id', dest='cluster_id', type=int, required=True)
        get_app_versions_parser.add_argument('--app_id', dest="app_id", type=int, required=True)
        get_app_versions_parser.set_defaults(func=self._get_app_versions)

        # sub-command: delete_app_version
        delete_app_version_parser = self.add_action('delete_app_version', help='delete app version')
        delete_app_version_parser.add_argument('--cluster_id', dest='cluster_id', type=int, required=True)
        delete_app_version_parser.add_argument('--app_id', dest='app_id', type=int, required=True)
        delete_app_version_parser.add_argument('--version_id', dest='version_id', type=str, required=True)
        delete_app_version_parser.set_defaults(func=self._delete_app_version)

        # sub-command: update_cluster_app
        update_cluster_app_parser = self.add_action('update_cluster_app', help='update app configuration')
        update_cluster_app_parser.add_argument('--cluster_id', dest='cluster_id', type=int, required=True)
        update_cluster_app_parser.add_argument('--app_id', dest='app_id', type=int, required=True)
        update_cluster_app_parser.add_argument('--method', dest='http_method', choices=['patch', 'put'])
        update_cluster_app_parser.add_argument('-f', '--file', help='bundle json containing new app info', type=argparse.FileType('r'), required=True)
        update_cluster_app_parser.set_defaults(func=self._update_cluster_app)

        # sub-command: get_app_instances
        get_app_tasks_parser = self.add_action('get_app_instances', help='list all instances for a specific app')
        get_app_tasks_parser.add_argument('--cluster_id', dest='cluster_id', type=int, required=True)
        get_app_tasks_parser.add_argument('--app_id', dest='app_id', type=str, required=True)
        get_app_tasks_parser.set_defaults(func=self._get_app_tasks)

        # sub-command: get_app_events
        get_app_events_parser = self.add_action('get_app_events', help='list all events for a specific app')
        get_app_events_parser.add_argument('--cluster_id', dest='cluster_id', type=int, required=True)
        get_app_events_parser.add_argument('--app_id', dest='app_id', type=str, required=True)
        get_app_events_parser.set_defaults(func=self._get_app_events)

        # sub-command: get_app_nodes
        get_app_nodes_parser = self.add_action('get_app_nodes', help='list all nodes for a specific app')
        get_app_nodes_parser.add_argument('--cluster_id', dest='cluster_id', type=int, required=True)
        get_app_nodes_parser.add_argument('--app_id', dest='app_id', type=str, required=True)
        get_app_nodes_parser.set_defaults(func=self._get_app_nodes)

        # sub-command: get_cluster_ports
        get_cluster_ports_parser = self.add_action('get_cluster_ports', help='list the inner ports and outer ports for a specific cluster')
        get_cluster_ports_parser.add_argument('--cluster_id', dest='cluster_id', type=int, required=True)
        get_cluster_ports_parser.set_defaults(func=self._get_cluster_ports)

        # sub-command: get_app_scale_log
        get_app_scale_log_parser = self.add_action('get_app_scale_log', help='get the auto scale history when provided a strategy id')
        get_app_scale_log_parser.add_argument('--cluster_id', dest='cluster_id', type=int, required=True)
        get_app_scale_log_parser.add_argument('--app_id', dest='app_id', type=int, required=True)
        get_app_scale_log_parser.add_argument('--strategy_id', dest='strategy_id', type=int, required=True)
        get_app_scale_log_parser.set_defaults(func=self._get_app_scale_log)

        # sub-command: get_my_scale_log
        get_user_scale_log_parser = self.add_action('get_my_scale_log', help='get all the auto scale history owned by this loggin user')
        get_user_scale_log_parser.set_defaults(func=self._get_user_scale_log)

    def _get_cluster_apps(self, args):
        configs = self._get_config()
        cluster_id = args.cluster_id
        omega_client = omegaclient.OmegaClient(configs['host'], None, None, token=configs['token'])
        return omega_client.get_cluster_apps(cluster_id)

    def _create_cluster_apps(self, args):
        configs = self._get_config()
        cluster_id = args.cluster_id
        data = json.loads(args.file.read())
        omega_client = omegaclient.OmegaClient(configs['host'], None, None, token=configs['token'])
        return omega_client.create_cluster_apps(cluster_id, **data)

    def _get_cluster_app(self, args):
        configs = self._get_config()
        cluster_id = args.cluster_id
        app_id = args.app_id
        omega_client = omegaclient.OmegaClient(configs['host'], None, None, token=configs['token'])
        return omega_client.get_cluster_app(cluster_id, app_id)

    def _delete_cluster_app(self, args):
        configs = self._get_config()
        cluster_id = args.cluster_id
        app_id = args.app_id
        omega_client = omegaclient.OmegaClient(configs['host'], None, None, token=configs['token'])
        return omega_client.delete_cluster_app(cluster_id, app_id)

    def _get_user_apps(self, args):
        configs = self._get_config()
        omega_client = omegaclient.OmegaClient(configs['host'], None, None, token=configs['token'])
        return omega_client.get_user_apps()

    def _get_user_apps_status(self, args):
        configs = self._get_config()
        omega_client = omegaclient.OmegaClient(configs['host'], None, None, token=configs['token'])
        return omega_client.get_user_apps_status()

    def _get_app_versions(self, args):
        configs = self._get_config()
        cluster_id = args.cluster_id
        app_id = args.app_id
        omega_client = omegaclient.OmegaClient(configs['host'], None, None, token=configs['token'])
        return omega_client.get_app_versions(cluster_id, app_id)

    def _delete_app_version(self, args):
        configs = self._get_config()
        cluster_id = args.cluster_id
        app_id = args.app_id
        version_id = args.version_id
        omega_client = omegaclient.OmegaClient(configs['host'], None, None, token=configs['token'])
        return omega_client.delete_app_version(cluster_id, app_id, version_id)

    def _update_cluster_app(self, args):
        configs = self._get_config()
        cluster_id = args.cluster_id
        app_id = args.app_id
        http_method = args.http_method
        data = json.loads(args.file.read())
        omega_client = omegaclient.OmegaClient(configs['host'], None, None, token=configs['token'])
        return omega_client.update_cluster_app(cluster_id, app_id, http_method, **data)

    def _get_app_tasks(self, args):
        configs = self._get_config()
        cluster_id = args.cluster_id
        app_id = args.app_id
        omega_client = omegaclient.OmegaClient(configs['host'], None, None, token=configs['token'])
        return omega_client.get_app_tasks(cluster_id, app_id)

    def _get_app_events(self, args):
        configs = self._get_config()
        cluster_id = args.cluster_id
        app_id = args.app_id
        omega_client = omegaclient.OmegaClient(configs['host'], None, None, token=configs['token'])
        return omega_client.get_app_events(cluster_id, app_id)

    def _get_app_nodes(self, args):
        configs = self._get_config()
        cluster_id = args.cluster_id
        app_id = args.app_id
        omega_client = omegaclient.OmegaClient(configs['host'], None, None, token=configs['token'])
        return omega_client.get_app_nodes(cluster_id, app_id)

    def _get_cluster_ports(self, args):
        configs = self._get_config()
        cluster_id = args.cluster_id
        omega_client = omegaclient.OmegaClient(configs['host'], None, None, token=configs['token'])
        return omega_client.get_cluster_ports(cluster_id)

    def _get_app_scale_log(self, args):
        configs = self._get_config()
        cluster_id = args.cluster_id
        app_id = args.app_id
        strategy_id = args.strategy_id
        omega_client = omegaclient.OmegaClient(configs['host'], None, None, token=configs['token'])
        return omega_client.get_app_scale_log(cluster_id, app_id, strategy_id)

    def _get_user_scale_log(self, args):
        configs = self._get_config()
        omega_client = omegaclient.OmegaClient(configs['host'], None, None, token=configs['token'])
        return omega_client.get_user_scale_log()

    def _action_cluster_app(self, args):
        configs = self._get_config()
        cluster_id = args.cluster_id
        app_id = args.app_id
        action = args.action
        data = {'method': action}
        omega_client = omegaclient.OmegaClient(configs['host'], None, None, token=configs['token'])
        return omega_client.update_cluster_app(cluster_id, app_id, 'patch', **data)

    def _scale_app(self, args):
        configs = self._get_config()
        cluster_id = args.cluster_id
        app_id = args.app_id
        instances = args.instances
        data = {'method': 'scale'}
        data.update({'instances': instances})
        omega_client = omegaclient.OmegaClient(configs['host'], None, None, token=configs['token'])
        return omega_client.update_cluster_app(cluster_id, app_id, 'patch', **data)

    def _update_app_version(self, args):
        configs = self._get_config()
        cluster_id = args.cluster_id
        app_id = args.app_id
        version_id = args.version_id
        data = {'method': 'update_version'}
        data.update({'versionId': version_id})
        omega_client = omegaclient.OmegaClient(configs['host'], None, None, token=configs['token'])
        return omega_client.update_cluster_app(cluster_id, app_id, 'patch', **data)

