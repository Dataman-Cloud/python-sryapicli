"""
This files contains all meta-class that will be used in this project.
"""
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

from types import FunctionType


class MetaAPI(type):
    """Meta class"""

    def __init__(cls, name, bases, dct):
        super(MetaAPI, cls).__init__(name, bases, dct)

        # try:
        #     cls._handlers = cls._handlers
        # except AttributeError:
        #     cls._handlers = {}
        if not hasattr(cls, '_handlers'):
            cls._handlers = {}
        else:
            for name, value in cls.__dict__.items():
                if isinstance(value, FunctionType):
                    cls._handlers[name] = value
