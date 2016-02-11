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
    print(output)
    assert output == '../../test'
