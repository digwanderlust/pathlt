from __future__ import (
    absolute_import, division, generators, nested_scopes, print_function,
    unicode_literals, with_statement
)

import copy

import mock

import pathlt.transforms
from tests import fakes


def test_no_parents():
    input = 'test/1'
    output = pathlt.transforms.parentdir_expand(input)
    assert input == output


def test_expand_parents():
    input = '..2/test'
    output = pathlt.transforms.parentdir_expand(input)
    assert output == '../../test'


def test_physical_path_negative():
    input = 'test/test/'
    output = pathlt.transforms.physical_path(input)
    assert input == output


def test_physical_path_escaped_slash():
    input = r'test/test\//'
    output = pathlt.transforms.physical_path(input)
    assert input == output


def test_physical_path_positive():
    expected_ouput = '<physical_path>'

    def fake_callback(_):
        return expected_ouput

    output = pathlt.transforms.physical_path('test/test//', fake_callback)
    print(output)
    assert output == expected_ouput


def _disambiguated_check(test_case):
    tc = copy.deepcopy(test_case)
    lister = fakes.get_listdir_mock(tc['fake_dirs'])
    output = pathlt.transforms.__disambiguate_path(
        tc['search_root'],
        tc['search_path'],
        listdir_callback=lister,
    )
    assert output == tc['expected_output']


def test_disambiguate():
    fake_dirs = {'foo': ['bar', 'apple', 'orange']}
    test_cases = [
        {
            'search_root': 'foo',
            'search_path': 'b',
            'expected_output': 'bar',
            'fake_dirs': fake_dirs
        },
        {
            'search_root': 'foo',
            'search_path': 'c',
            'expected_output': None,
            'fake_dirs': fake_dirs
        },
        {
            'search_root': 'baz',
            'search_path': 'b',
            'expected_output': None,
            'fake_dirs': fake_dirs
        },
    ]
    for test_case in test_cases:
        yield _disambiguated_check, test_case


def _unambiguous_path_check(test_case):
    tc = copy.copy(test_case)
    output = pathlt.transforms.unambiguous_path(
        tc['path'],
        exists_callback=tc['exists_callback'],
        disambiguate_callback=tc['disambiguate_callback']
    )
    assert output == tc['expected_output']


def _get_fake_disambiguate(unambiguous_dirs):
    """ Create a function that mocks __disambiguate

    Return unambiguous dir expansion if available otherwise return the
    original directory name.
    :param unambiguous_dirs: list
    :return: str
    """

    def _inner(root, x):
        return unambiguous_dirs.get(x, x)

    return mock.Mock(side_effect=_inner)


def test_unambiguous_path():
    existing_paths = ['foo', 'foo/bar', 'foo/bar/baz', 'bizz']
    transitions = {'f': 'foo', 'b': 'bar', 'bad_path': None, }
    test_cases = [
        {
            'expected_output': 'foo/bar/baz',
            'path': 'f/bar/baz',
            'exists_callback': fakes.get_exists_mock(existing_paths),
            'disambiguate_callback': _get_fake_disambiguate(transitions),
        }, {
            'expected_output': 'foo/bar',
            'path': 'f/b',
            'exists_callback': fakes.get_exists_mock(existing_paths),
            'disambiguate_callback': _get_fake_disambiguate(transitions),
        }, {
            'expected_output': 'bizz',
            'path': 'bizz',
            'exists_callback': fakes.get_exists_mock(existing_paths),
            'disambiguate_callback': _get_fake_disambiguate(transitions),
        }, {
            'expected_output': 'foo',
            'path': 'f',
            'exists_callback': fakes.get_exists_mock(existing_paths),
            'disambiguate_callback': _get_fake_disambiguate(transitions),
        }, {
            'expected_output': 'bad_path',
            'path': 'bad_path',
            'exists_callback': fakes.get_exists_mock(existing_paths),
            'disambiguate_callback': _get_fake_disambiguate(transitions),
        }
    ]
    for test_case in test_cases:
        yield _unambiguous_path_check, test_case
