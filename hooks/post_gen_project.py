#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import shutil

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('post_gen_project')


def zip_files():
    logger.info('Zipping file to {{cookiecutter.extension_name}}-{{cookiecutter.extension_version}}.oxt')
    extension_path = '../oxt/'
    oxt = os.path.join(
        extension_path,
        "{{cookiecutter.extension_name}}-{{cookiecutter.extension_version}}.oxt"
    )
    if not os.path.exists(extension_path):
        os.mkdir(extension_path)
    manifest = os.path.join("META-INF", "manifest.xml")

    shutil.make_archive(oxt, 'zip', './')
    os.rename(oxt + '.zip', oxt)


zip_files()

# zip - 9 - r - n
# pyc - o.. / files / toto.oxt
# META - INF / * *.xcu *.xcs
# config.ini
# descriptions / * description.xml
# dialogs / * icons / * LICENSE
# optionsdialoghandler.py
# pythonpath / * OptionsDialog.components
