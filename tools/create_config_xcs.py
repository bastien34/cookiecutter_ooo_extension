#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import logging.config
import xml.etree.ElementTree as ET
from _elementtree import Element

import yaml
from helpers import (ElemProp, Elem)


# General
extension_filename = "{{cookiecutter.extension_name}}-{{cookiecutter.extension_version}}.oxt"

# file_location = "../tmp/"  # dev
file_location = "../{{cookiecutter.extension_name}}/src/config"
xml_file = "{{cookiecutter.extension_name}}_config.xcs"
locale = {"xml:lang": "fr"}

logger = logging.getLogger(__name__)


class Var:
    def __init__(self, name, label, vtype, default):
        self.name = name
        self.label = label
        self.vtype = vtype
        self.default = default


# Test values
v1 = Var('test_mode', 'Activate test mode', 'boolean', 'true')
v2 = Var('output_dir', 'Output', 'string', os.environ['HOME'])
v3 = Var('url', 'URL', 'string', 'https://my_website.com/')

test_values = v2,


def create_config_xcs(option_vars):
    """
    Creation of OptionsDialog.xcu.

    This file contains description of options var and their default
    values.

    Its parameter is a list of Var Instance.
    """
    path = os.path.dirname(os.path.realpath(__file__))
    logger.debug('Start creating %s.', xml_file)

    path_file = os.path.join(file_location, xml_file)
    path_file = os.path.join(path, path_file)

    root = Element("oor:component-schema",
                   {"xmlns:oor": "http://openoffice.org/2001/registry",
                    "xmlns:xs": "http://www.w3.org/2001/XMLSchema",
                    "oor:name": "ExtensionData",
                    "oor:package": "{{cookiecutter.package_name}}",
                    "xml:lang": "en-US"})

    with open(path_file, "w", encoding="UTF-8") as xf:
        template = ET.SubElement(root, "templates")
        group = ET.SubElement(template, 'group', {'oor:name': "Production"})
        inf = ET.SubElement(group, 'info')
        inf.append(Elem('desc', {'text': 'Values for production mode'}))
        defaults = ET.SubElement(group, 'group', {'oor:name': 'Defaults'})

        # Iteration on options list
        for ov in option_vars:
            vtype = f'xs:{ov.vtype}'
            ET.SubElement(group, 'prop', {'oor:name': ov.name,
                                          'oor:type': vtype})
            defaults.append(ElemProp(ov.name, ov.default,
                                     {'oor:type': vtype}))

        # Component
        cmp = ET.SubElement(root, 'component')
        leaves = ET.SubElement(cmp, 'group', {'oor:name': 'Leaves'})
        leaves.append(
            Elem('node-ref', {'oor:name': "{{cookiecutter.extension_name}}",
                              'oor:node-type': "Production"}))

        tree = ET.ElementTree(root)
        tree.write(xf.name, "utf-8", True)

    logger.info("%s created in -> %s", xml_file, file_location)


if __name__ == "__main__":
    with open('logging_conf.yaml', 'r') as f:
        log_cfg = yaml.safe_load(f.read())
        logging.config.dictConfig(log_cfg)
    create_config_xcs(test_values)
