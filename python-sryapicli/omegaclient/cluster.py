# Copyright (c) 2016 Dataman Cloud
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from jsonschema import SchemaError, ValidationError, validate
from omegaclient.utils import url_maker


class ClusterMixin(object):

    def get_clusters(self):
        """List all clusters"""

        resp = self.http.get("/clusters")

        return self.process_data(resp)

    def get_cluster(self, cluster_id):
        """List single cluster's information"""

        resp = self.http.get(url_maker("/clusters", cluster_id))

        return self.process_data(resp)

    def create_cluster(self, name, cluster_type, group_id):
        """Create new cluster.

        :param name: cluster name
        :param cluster_type: cluster type, current support values are:
                               1_master, 3_masters, 5_masters
        :param group_id: the group which the new cluster belong to
        """
        data = {
              "name": name,
              "clusterType": cluster_type,
              "groupId": group_id,
        }
        schema = {
              "type": "object",
              "properties": {
                  "name": {"type": "string"},
                  "clusterType": {"type": "string"},
                  "groupId": {"type": "number"},
              },
              "required": ["name", "clusterType", "groupId"]
          }
        try:
            validate(data, schema)
        except (SchemaError, ValidationError) as e:
            return e

        resp = self.http.post("/clusters", data=data)

        return self.process_data(resp)

    def delete_cluster(self, cluster_id):
        """Delete cluster"""

        return self.http.delete(url_maker("/clusters", cluster_id))

    def update_cluster(self, cluster_id, **kwargs):
        """Updated cluster information."""

        return self.http.patch(url_maker("/clusters", cluster_id), data=kwargs)

    def get_node_identifier(self, cluster_id):
        """Generated new node identifier. this identifier will be
        used for add new node."""

        resp = self.http.get(url_maker("/clusters", cluster_id,
                                       "new_node_identifier"))

        return self.process_data(resp)

    def get_cluster_node(self, cluster_id, node_id):
        """List node information"""

        resp = self.http.get(url_maker("/clusters", cluster_id, "nodes",
                                       node_id))

        return self.process_data(resp)

    def update_cluster_node(self, cluster_id, node_id, **kwargs):
        """Updated node information"""

        return self.http.patch(url_maker("/clusters", cluster_id,
                                         "nodes", node_id), **kwargs)

    def get_node_metrics(self, cluster_id, node_id):
        """Retrive node metrics"""

        resp = self.http.get(url_maker("/clusters", cluster_id, "nodes",
                                       node_id))

        return self.process_data(resp)

    def update_node_service(self, cluster_id, node_id, service_name, **kwargs):
        """Reset or restart service on node"""

        return self.http.patch(url_maker("/clusters", cluster_id, "nodes",
                                         node_id, "services", service_name),
                               **kwargs)

    def create_node(self, cluster_id, **kwargs):
        """Add new node for cluster identified by `cluster_id`"""
        return self.http.post(url_maker("/clusters", cluster_id, "nodes"),
                              data=kwargs)

    def delete_nodes(self, cluster_id, *args):
        """Delete nodes for cluster identified by `cluster_id`"""
        return self.http.delete(url_maker("/clusters", cluster_id, "node"),
                                data=args)
