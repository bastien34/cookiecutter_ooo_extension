#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import shutil
import stat

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('post_gen_project')


def zip_files():
    logger.info('Zipping file to {{cookiecutter.extension_name}}-{{cookiecutter.extension_version}}.oxt')
    extension_path = 'extension/'
    oxt = os.path.join(
        extension_path,
        "{{cookiecutter.extension_name}}-{{cookiecutter.extension_version}}.oxt"
    )
    shutil.make_archive(oxt, 'zip', 'src/')
    os.rename(oxt + '.zip', oxt)


def mv_oxt_generator():
    logger.info('Moving oxt generator for further development')
    src_file = 'oxt_gen.py'
    os.rename('src/%s' % src_file, src_file)
    st = os.stat(src_file)
    os.chmod(src_file, st.st_mode | stat.S_IEXEC)


zip_files()


mv_oxt_generator()
