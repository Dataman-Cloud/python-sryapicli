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


class LogMixin(object):
    """Log controller for response log rest apis"""

    def get_app_logs(self, **kwargs):
        """Retrive app runtime logs"""

        resp = self.http.post("/es/index", data=kwargs)

        return self.process_data(resp)

    def get_app_context(self, **kwargs):
        """Retrive app context?"""

        resp = self.http.post("/es/context", data=kwargs)

        return self.process_data(resp)
