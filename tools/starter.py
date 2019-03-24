#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging.config
import yaml
from create_addon_ui import create_addon
from create_config_xcs import create_config_xcs


if __name__ == "__main__":
    with open('logging_conf.yaml', 'r') as f:
        log_cfg = yaml.safe_load(f.read())
        logging.config.dictConfig(log_cfg)
        logger = logging.getLogger(__name__)
    logger.info('Start job')
    create_addon()
    create_config_xcs()
    logger.info('Job finished')
