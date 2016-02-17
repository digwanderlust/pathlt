from __future__ import (
    absolute_import, division, generators, nested_scopes, print_function,
    unicode_literals, with_statement
)

import re
import os
import fnmatch


def parentdir_expand(path):
    """ Expand parent directory traversal

  Allow the user to specify ..<n> and expand to a recognized directory path.
  for example ..5 would expand to ../../../../..

  :param path: str
  :return: str
  """
    if path[0:2] != '..':
        return path
    else:
        parentdir_match = r'\.\.(\d*){0}(.*)'.format(os.path.sep)
        matches = re.match(parentdir_match, path)
        expand_depth = matches.group(1) or 1
        extra_path = matches.group(2)

        parent_path = os.path.join(*['..'] * int(expand_depth))
        return os.path.join(parent_path, extra_path)


def physical_path(path, transform_callback=None):
    """ Return the physical path if path ends with //

    :param path: str
    :return: str
    """
    transform_callback = transform_callback or os.path.realpath

    if re.match(r'.*(?<!\\)//', path):
        return transform_callback(path)
    else:
        return path


def __disambiguate_path(root, path):
    root = root or os.getcwd()
    candidates = [f
                  for f in os.listdir(root)
                  if fnmatch.fnmatch(f, '{}*'.format(path))]
    if len(candidates) == 1:
        return candidates[0]
    else:
        return None


def unambiguous_path(path):
    if os.path.exists(path):
        return path
    else:
        head, tail = os.path.split(path)
        if head:
            root = unambiguous_path(head)
        else:
            root = head
        tail = __disambiguate_path(root, tail)
        if tail:
            return os.path.join(root, tail)
        else:
            return path
