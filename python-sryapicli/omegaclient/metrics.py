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

from omegaclient.utils import url_maker


class MetricsMixin(object):
    """Metrics associated apis"""

    def get_app_history_metrics(self, cluster_id, app_alias):
        """List app history metrics"""

        resp = self.http.get(url_maker("/clusters", cluster_id, "apps",
                                       app_alias, "monitor"))

        return self.process_data(resp)

    def get_app_requests(self, cluster_id, app_alias):
        """List app's requests for per second"""

        resp = self.http.get(url_maker("/clusters", cluster_id, "apps",
                                       app_alias, "session"))

        return self.process_data(resp)

    def get_app_live_metrics(self, cluster_id, app_alias):
        """List all living metrics"""

        resp = self.http.get(url_maker("/clusters", cluster_id, "apps",
                                       app_alias, "metrics"))

        return self.process_data(resp)

    def get_cluster_resource_metrics(self, cluster_id):
        """List cluster metrics"""

        resp = self.http.get(url_maker("/clusters", cluster_id, "metrics"))

        return self.process_data(resp)
