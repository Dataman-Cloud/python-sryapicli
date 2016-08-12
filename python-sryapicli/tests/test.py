import contextlib
import functools
import types
from unittest import mock
import unittest
from io import StringIO

from omegaclient.test_helpers import MockAPI
from sryapicli import ClientRunner

def mock_api(func):
    @functools.wraps(func)
    def wrapper(self):
        with mock.patch('omegaclient.OmegaClient') as cls:
            api = MockAPI()
            cls.return_value = api
            return func(self, api)
    return wrapper


class OmegaClientMetaClass(type):
    """Automatically wrap all test methods in `mock_api` decorator.
    """
    def __new__(cls, name, bases, attrs):
        for attr_name, attr_value in iter(attrs.items()):
            if isinstance(attr_value, types.FunctionType) and attr_name.startswith('test_'):
                attrs[attr_name] = mock_api(attr_value)
        return super(OmegaClientMetaClass, cls).__new__(cls, name, bases, attrs)


class OmegaClientTestCase(unittest.TestCase, metaclass=OmegaClientMetaClass):

    def setUp(self):
        self.runner = ClientRunner()
        self.runner.setup()
