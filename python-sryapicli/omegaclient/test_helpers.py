
class MockAPI(object):

    def get_cluster_apps(self, cluster_id):
        return {'cluster_id': cluster_id}
