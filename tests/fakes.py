from __future__ import (
    absolute_import, division, generators, nested_scopes, print_function,
    unicode_literals, with_statement
)
import copy
import mock
import os


def get_listdir_mock(expected_returns):
    fake_fs = copy.deepcopy(expected_returns)

    def fake_listdir(path):
        if path in fake_fs:
            return fake_fs.get(path)
        else:
            raise OSError

    return mock.MagicMock(spec=os.path.exists, side_effect=fake_listdir)


def get_exists_mock(available_paths):
    """ Return a mock that mimis os.getcwd and always returns ret_path
    :param available_paths: list
    :return: function
    """
    available = copy.copy(available_paths)

    def exists_lookup(path):
        return path in available

    return mock.MagicMock(spec=os.path.exists, side_effect=exists_lookup)


def get_getcwd_mock(ret_path):
    """ Return a mock that mimis os.getcwd and always returns ret_path
    :param ret_path: str
    :return: function
    """
    return mock.MagicMock(spec=os.getcwd, return_value=ret_path)
