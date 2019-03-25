#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging.config
import yaml
from create_addon_ui import (create_addon,
                             test_functions)
from create_config_xcs import (create_config_xcs,
                               test_values)
from create_dialog import create_dialog


"""
This starter needs a Environ.
"""


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
