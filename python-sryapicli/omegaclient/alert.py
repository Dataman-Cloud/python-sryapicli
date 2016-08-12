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


class AlertMixin(object):
    """Alert associated apis."""

    def get_tasks(self, **kwargs):
        """Lists all the policies that the user created."""

        resp = self.http.get("/alert/tasks", params=kwargs)

        return self.process_data(resp)

    def create_task(self, **kwargs):
        """Created new policy"""

        resp = self.http.post("/alert/tasks", data=kwargs)

        return self.process_data(resp)

    def put_task(self, **kwargs):
        """Updated policy information."""

        self.http.put("/alert/tasks", data=kwargs)

    def patch_task(self, policy_id, **kwargs):
        """Updated policy status."""

        self.http.patch(url_maker("/alert/tasks", policy_id), data=kwargs)

    def get_task(self, policy_id):
        """List policy information."""

        resp = self.http.get(url_maker("/alert/tasks", policy_id))

        return self.process_data(resp)

    def delete_task(self, policy_id):
        """Delete policy"""

        self.http.delete(url_maker("/alert/tasks", policy_id))

    def get_alarm_events(self, **kwargs):
        """List all alarm event's histories."""

        resp = self.http.get("/alert/events", params=kwargs)

        return self.process_data(resp)
        
