#!/usr/bin/env python
"""This checks for a given list of included packages whether they are catkin packages and whether
they are named as package dependency."""

from __future__ import print_function

import os
import re
import sys

from .ros import get_rosdep

def check_includes(includes):
    """
    Checks for corresponding catkin packages
    """

    rosdep_obj = get_rosdep(False)
    catkin_packages = list()
    for package in includes:
        if rosdep_obj.has_key(package):
            catkin_packages.append(package)
    return catkin_packages

def find_include_in_file(filename):
    """Extracts all include lines from given file"""
    includes = set()
    with open(filename) as content:
        for line in content:
            if re.match("^#include", line):
                try:
                    # print(line)
                    m = re.search('(("|<)(.+?)("|>))', line)
                    inc = re.search('^(.+?)/', m.group(3)).group(1)
                    includes.add(inc)
                except AttributeError:
                    pass
    return includes

def find_cpp_include_packages(package_path='.'):
    """Main function"""
    includes = set()
    for dname, dirs, files in os.walk(package_path):
        for fname in files:
            fpath = os.path.join(dname, fname)
            includes.update(find_include_in_file(fpath))
    include_list = check_includes(includes)

    return set(include_list)
