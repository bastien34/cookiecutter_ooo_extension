#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import re
import sys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('pre_gen_project')

PKG_REGEX = r'^([a-z]+:)*[a-z]+$'


def create_pkg(pkg):
    # if not re.match(PKG_REGEX, pkg):
    #     logger.error('Invalid value for package_name "{}"'.format(pkg))
    #     sys.exit(1)
    #
    # pkg_dir = re.sub(':', '/', pkg)
    #
    # logger.info('Create package structure "{}"'.format(pkg_dir))
    # os.makedirs(pkg_dir)
    print(pkg)

create_pkg('{{cookiecutter.package_name}}')
