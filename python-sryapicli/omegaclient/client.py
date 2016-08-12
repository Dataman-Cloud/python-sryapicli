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

import json
import requests

API_VERSION = "/api/v3"


class HTTPClient(object):
    """Http client for send http requests"""

    def __init__(self, server_url, name, password, token=None):
        self._base_url = self.get_url(server_url)
        self._name = name 
        self._password = password
        self._session = None
        self._token = token
        self.timeout = 86400

        self.get_token()

    @staticmethod
    def get_url(server_url):
        """Generate access url"""

        if server_url.endswith("/"):
            return server_url + API_VERSION.lstrip("/")
        return server_url + API_VERSION

    def get_session(self):
        """Get request session"""

        if not self._session:
            self._session = requests.Session()
        return self._session

    def get_token(self):
        """Obtain user auth token"""

        if self._name and self._password:
            with self.get_session() as session:
                data = {"name": self._name, "password": self._password}
                resp = session.request("POST", self._base_url + "/auth",
                                       data=json.dumps(data))

                if resp.json()['code'] == 0:
                    self._token = resp.json()['data']['token']
                else:
                    print ('Ooops, authentication failed!')

    def _request(self, url, method, **kwargs):
        """Send request"""

        kwargs.setdefault('headers', kwargs.get('headers', {}))
        kwargs['headers']['User-Agent'] = "API-CLIENT"
        kwargs['headers']['Accept'] = 'application/json'
        kwargs['headers']['Authorization'] = self._token
        kwargs['headers']['Content-type'] = 'application/json'

        if 'data' in kwargs:
            kwargs['headers']['Content-Type'] = 'application/json'
            kwargs['data'] = json.dumps(kwargs['data'])

        if 'params' in kwargs:
            kwargs['params'] = json.dumps(kwargs['params'])

        if self.timeout is not None:
            kwargs.setdefault('timeout', self.timeout)

        with self.get_session() as session:
            resp = session.request(method, url, **kwargs)
        return resp

    def request(self, url, method, **kwargs):
        """Send requests with API Verison"""

        return self._request(self._base_url + url, method, **kwargs)

    def bare_request(self, url, method, **kwargs):
        """Send requests without API Version."""

        return self._request(url, method, **kwargs)

    def get(self, url, **kwargs):
        """Send a GET request. Returns :class:`requests.Response` object"""

        return self.request(url, 'GET', **kwargs)

    def post(self, url, **kwargs):
        """Send a POST request. Returns :class:`requests.Response` object"""

        return self.request(url, 'POST', **kwargs)

    def options(self, url, **kwargs):
        """Send a OPTIONS request. Returns :class:`requests.Response` object"""

        raise NotImplementedError()

    def put(self, url, data=None, **kwargs):
        """Send a PUT request. Returns :class:`requests.Response` object"""

        return self.request(url, 'PUT', data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        """Send a PATCH request. Returns :class:`requests.Response` object"""

        return self.request(url, 'PATCH', data=data, **kwargs)

    def delete(self, url, **kwargs):
        """Send a DELETE request. Returns :class:`requests.Response` object"""

        return self.request(url, 'DELETE', **kwargs)
