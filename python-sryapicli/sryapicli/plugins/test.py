import ast

from unittest.mock import patch
from io import StringIO

from tests.test import OmegaClientTestCase


class AppPluginTestCase(OmegaClientTestCase):

    def setUp(self):
        super(AppPluginTestCase, self).setUp()

    @patch('sys.stdout', new_callable=StringIO)
    def test_get_cluster_apps(self, api, mock_stdout):
        self.runner.run(['app', 'get_cluster_apps', '--cluster_id', '891'])
        data = ast.literal_eval(mock_stdout.getvalue())
        self.assertEqual(data['cluster_id'], 891)
