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


class ProjectMixin(object):
    """Project controllers for response projects apis."""

    def get_projects(self):
        """list all projects(images) for speicified user."""
        resp = self.http.get("/projects")

        return self.process_data(resp)

    def get_project(self, project_id):
        """show project details."""

        resp = self.http.get(url_maker("/projects", project_id))

        return self.process_data(resp)

    def create_project(self, **kwargs):
        """create new project."""

        schema = {
            "type": "object",
            "properties": {
                "uid": {"type": "number"},
                "name": {"type": "string"},
                "imageName": {"type": "string"},
                "description": {"type": "string"},
                "repoUri": {"type": "string"},
                "branch": {"type": "string"},
                "active": {"type": "boolean"},
                "period": {"type": "number"},
                "triggerType": {"type": "number"},
            },
            "required": ["uid", "name", "imageName", "description", "repoUri",
                         "branch", "active", "period", "triggerType"]
        }

        try:
            validate(kwargs, schema)
        except (SchemaError, ValidationError) as e:
            return e

        resp = self.http.post("/projects", data=kwargs)

        return self.process_data(resp)

    def build_project(self, project_id, uid, image_name):
        """Build project."""

        data = {
            "uid": uid,
            "imageName": image_name,
        }

        resp = self.http.post(url_maker("/projects", project_id, "hook"),
                              data=data)

        return self.process_data(resp)

    def update_project(self, project_id, **kwargs):
        """Update specified project information."""

        schema = {
            "type": "object",
            "properties": {
                "uid": {"type": "number"},
                "active": {"type": "boolean"},
                "period": {"type": "number"},
                "triggerType": {"type": "number"},
            },
            "required": ["uid", "active", "period", "triggerType"]
        }

        try:
            validate(kwargs, schema)
        except (SchemaError, ValidationError) as e:
            return e

        return self.http.put(url_maker("/projects", project_id), data=kwargs)

    def delete_project(self, project_id):
        """Delete specified project."""

        return self.http.delete(url_maker("/projects", project_id))

    def get_project_builds(self, project_id):
        """list all builds for project"""

        resp = self.http.get(url_maker("/projects", project_id, "builds"))

        return self.process_data(resp)

    def get_build_logs(self, project_id, build_num, job_id):
        """List all build logs for project"""

        resp = self.http.get(url_maker("/projects", project_id, "builds",
                                       build_num, job_id, "logs"))

        return self.process_data(resp)

    def get_build_stream(self, project_id, build_num, job_id):
        """List all build text stream for project"""

        resp = self.http.get(url_maker("/projects", project_id, "builds",
                                       build_num, job_id, "stream"))

        return self.process_data(resp)
