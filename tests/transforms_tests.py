from __future__ import (
    absolute_import, division, generators, nested_scopes, print_function,
    unicode_literals, with_statement
)

import pathlt.transforms


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
