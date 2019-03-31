#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging.config
import yaml
from cookiecutter.main import cookiecutter

# TODO: group these 3 functions in one module
from create_addon_ui import (create_addon,
                             test_functions)
from create_config_xcs import (create_config_xcs,
                               test_values)
from create_dialog import create_dialog


EXTENSION_DESCRIPTION = (
    'extension_name',
    'extension_label',
    'extension_version',
    'packages_name',
    'company_name',
    'author_name',
    'update_url',
    'publisher_url',
    'image_name',
)
output_dir = '/home/bastien/tmp'
repo = "https://github.com/bastien34/cookiecutter_ooo_extension"


def test_launcher(*args):
    """
    Launcher... For now connected to `extension_manager.odt`

    Instead of creating a yaml file `.cookiecuttercc`, it seems
    wiser to send a dict as extra_context.

    """
    doc = XSCRIPTCONTEXT.getDocument()
    tb = doc.getTextTables().getByName('description_table')
    description_data = tb.getDataArray()
    tb = doc.getTextTables().getByName('function_table')
    function_data = tb.getDataArray()
    tb = doc.getTextTables().getByName('option_table')
    option_data = tb.getDataArray()

    extra_context = {}
    [extra_context.update({r[0]: r[1]}) for r in description_data]

    # TODO: Before generating the project, we must create our config files.

    cookiecutter('cookiecutter-django', no_input=True,
                 extra_context=extra_context,
                 output_dir=output_dir
                 )


if __name__ == "__main__":
    with open('logging_conf.yaml', 'r') as f:
        log_cfg = yaml.safe_load(f.read())
        logging.config.dictConfig(log_cfg)
        logger = logging.getLogger(__name__)
    logger.info('Start building configuration')
    create_addon(test_functions)
    create_config_xcs(test_values)
    create_dialog(test_values)
    logger.info('Configuration completed. Yeah!')
