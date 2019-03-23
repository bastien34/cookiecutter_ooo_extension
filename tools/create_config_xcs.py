#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import logging
import xml.etree.ElementTree as ET
from _elementtree import Element
from helper import (ElemProp, Elem)

extension_filename = "{{cookiecutter.extension_name}}-{{cookiecutter.extension_version}}.oxt"
extension_id = "com.pwd.myextension"
package_name = "{{cookiecutter.package_name}}"
xml_file = f"{package_name}_config.xcs"  # To be adjusted in the right location
locale = {"xml:lang": "fr"}

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("Now, it's time to create the %s file!\n" % xml_file)


def create_config_xcs():
    """
    Creation of OptionsDialog.xcu
    """
    path = os.path.dirname(os.path.realpath(__file__))
    logger.info("Creating xcs in: %s" % path)

    root = Element("oor:component-schema",
                   {"xmlns:oor": "http://openoffice.org/2001/registry",
                    "xmlns:xs": "http://www.w3.org/2001/XMLSchema",
                    "oor:name": "ExtensionData",
                    "oor:package": "{{cookiecutter.package_name}}",
                    "xml:lang": "en-US"})

    with open(xml_file, "w", encoding="UTF-8") as f:
        template = ET.SubElement(root, "templates")
        group = ET.SubElement(template, 'group', {'oor:name': "Production"})
        inf = ET.SubElement(group, 'info')
        inf.append(Elem('desc', {'text': 'Values for production mode'}))

        # Here, iteration on options list
        group.append(ElemProp('test_mode', 'un petit texte',
                              {'oor:type': "xs.boolean"}))

        # Manage default values
        defaults = ET.SubElement(group, 'group', {'oor:name': 'Defaults'})

        # Iteration on default values
        defaults.append(ElemProp('test_mode', '0', {'oor:type': 'xs:boolean'}))

        # Component
        cmp = ET.SubElement(root, 'component')
        leaves = ET.SubElement(cmp, 'Leaves')
        leaves.append(
            Elem('node-ref', {'oor:name': "{{cookiecutter.extension_name}}",
                              'oor:node': "Production"}))

        tree = ET.ElementTree(root)
        tree.write(f.name, "utf-8", True)
    logger.info("%s has been created.\nThanks for support !" % xml_file)


if __name__ == "__main__":
    create_config_xcs()
