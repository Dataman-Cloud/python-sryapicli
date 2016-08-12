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

import copy
from jsonschema import SchemaError, ValidationError, validate
from omegaclient.utils import url_maker


class AppMixin(object):
    """App associated APIs"""

    def get_cluster_apps(self, cluster_id, **kwargs):
        """List all apps for speicified cluster"""

        resp = self.http.get(url_maker("/clusters", cluster_id, "apps"),
                             **kwargs)

        return self.process_data(resp)

    def create_cluster_apps(self, cluster_id, **kwargs):
        """Create app under speicified cluster

        :param cluster_id: Cluster identifier
        :param data: Dictionary to send in the body of the request.

        """

        # NOTE(mgniu): `deep copy or shallow copy? i'm confused.
        data = copy.deepcopy(kwargs)

        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "instances": {"type": "number"},
                "volumes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "hostPath": {"type": "string"},
                            "containerPath": {"type": "string"},
                         },
                     },
                 },
                "portMappings": {
                     "type": "array",
                     "items": {
                         "type": "object",
                         "properties": {
                             "appPort": {"type": "number"},
                             "protocol": {"type": "number"},
                             "isUri": {"type": "number"},
                             "type": {"type": "number"},
                             "mapPort": {"type": "number"},
                             "uri": {"type": "string"},
                          },
                      },
                   },
                "cpus": {"type": "number"},
                "mem": {"type": "number"},
                "cmd": {"type": "string"},
                "envs": {
                       "type": "array",
                       "items": {
                           "type": "object",
                           "properties": {
                               "key": {"type": "string"},
                               "value": {"type": "string"},
                            },
                        },
                   },
                "imageName": {"type": "string"},
                "imageVersion": {"type": "string"},
                "forceImage": {"type": "boolean"},
                "network": {"type": "string"},
                "constraints": {
                       "type": "array",
                       "items": {
                           "type": "array",
                           "items": {"type": "string"},
                       },
                   },
                "parameters": {
                       "type": "array",
                       "items": {
                           "type": "object",
                           "properties": {
                               "key": {"type": "string"},
                               "value": {"type": "string"},
                           },
                       },
                   }
            }
        }
        try:
            validate(data, schema)
        except (SchemaError, ValidationError) as e:
            return e

        resp = self.http.post(url_maker("/clusters", cluster_id, "apps"),
                              data=data)

        return self.process_data(resp)

    def get_cluster_app(self, cluster_id, app_id):
        """List specified app information under specified cluster"""

        resp = self.http.get(url_maker("/clusters", cluster_id,
                                       "apps", app_id))

        return self.process_data(resp)

    def delete_cluster_app(self, cluster_id, app_id):
        """Delete specified app under specified cluster"""

        resp = self.http.delete(url_maker("/clusters", cluster_id,
                                          "apps", app_id))
        return self.process_data(resp)

    def get_user_apps(self, **kwargs):
        """List all apps belong to specified user."""

        resp = self.http.get("/apps", **kwargs)

        return self.process_data(resp)

    def get_user_apps_status(self):
        """List all app's status"""

        resp = self.http.get("/apps/status")

        return self.process_data(resp)

    def get_app_versions(self, cluster_id, app_id):
        """List all history versions for app"""

        resp = self.http.get(url_maker("/clusters", cluster_id, "apps", app_id,
                                       "versions"))

        return self.process_data(resp)

    def delete_app_version(self, cluster_id, app_id, version_id):
        """Delete app version"""

        resp = self.http.delete(url_maker("/clusters", cluster_id,
                                          "apps", app_id, "versions",
                                          version_id))
        return self.process_data(resp)

    def update_cluster_app(self, cluster_id, app_id, http_method, **kwargs):
        """Updated app configuration"""

        if not http_method or http_method.lower() == 'patch':
            resp = self.http.patch(url_maker("/clusters", cluster_id,
                                             "apps", app_id),
                                   data=kwargs)
        else:
            resp = self.http.put(url_maker("/clusters", cluster_id, "apps",
                                           app_id), data=kwargs)

        return self.process_data(resp)

    def get_app_tasks(self, cluster_id, app_id):
        """List all app tasks"""

        resp = self.http.get(url_maker("/clusters", cluster_id, "apps", app_id,
                                       "tasks"))

        return self.process_data(resp)

    def get_app_events(self, cluster_id, app_id):
        """List all app events"""

        resp = self.http.get(url_maker("/clusters", cluster_id, "apps", app_id,
                                       "events"))

        return self.process_data(resp)

    def get_app_nodes(self, cluster_id, app_id):
        """List all app instances."""

        resp = self.http.get(url_maker("/clusters", cluster_id, "apps", app_id,
                                       "appnodes"))

        return self.process_data(resp)

    def get_cluster_ports(self, cluster_id):
        """list the inner ports and outer ports for a specific cluster"""

        resp = self.http.get(url_maker("/clusters", cluster_id, "ports"))
        return self.process_data(resp)

    def get_app_scale_log(self, cluster_id, app_id, strategy_id):
        """get the auto scale history when provided a strategy id"""

        resp = self.http.get(url_maker("/clusters", cluster_id, "apps", app_id,
                                       "scale", strategy_id))
        return self.process_data(resp)

    def get_user_scale_log(self):
        """get all the auto scale history owned by this loggin user """

        resp = self.http.get(url_maker("/scales"))
        return self.process_data(resp)
