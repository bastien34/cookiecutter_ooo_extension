#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import logging.config
import xml.etree.ElementTree as ET
import yaml

# General
extension_filename = "{{cookiecutter.extension_name}}-{{cookiecutter.extension_version}}.oxt"

# file_location = "../tmp/"
file_location = "../{{cookiecutter.extension_name}}/src/dialogs"

xml_file = "{{cookiecutter.extension_name}}_dialog.xdl"

logger = logging.getLogger(__name__)


class DialogElementBase:
    """Dialog component base."""
    def __init__(self, y, id, tb):
        self.top = y
        self.id = id
        self.width = 60
        self.height = 14
        self.left = 10
        self.align = "center"
        self.valign = "center"
        self.tab_index = tb

    @property
    def dict(self):
        attrib = {}
        [attrib.update({f"dlg:{k}": str(v)}) for k, v in self.__dict__.items()]
        return attrib


class TextField(DialogElementBase):
    def __init__(self, y, id, tb, default):
        super().__init__(y, id, tb)
        self.value = default
        self.width = 160
        self.left = 80
        self.align = "left"


class Label(DialogElementBase):
    def __init__(self, y, id, tb, label):
        super().__init__(y, id, tb)
        self.value = label


class CheckBox(DialogElementBase):
    def __init__(self, y, id, tb, label, default):
        super().__init__(y, id, tb)
        self.value = label
        self.checked = default
        self.width = 100


def create_dialog(option_vars):
    """
    Creation of OptionsDialog.xcu.

    This file contains description of options var and their default
    values.

    Its parameter is a list of Var Instance.
    """
    logger.debug('Start creating %s.', xml_file)

    path = os.path.dirname(os.path.realpath(__file__))
    path_file = os.path.join(file_location, xml_file)
    path_file = os.path.join(path, path_file)

    root = ET.Element('dlg:window', {
        "xmlns:dlg": "http://openoffice.org/2000/dialog",
        "xmlns:script": "http://openoffice.org/2000/script",
        "dlg:id": "{{cookiecutter.extension_name}}_dialog",
        "dlg:left": "100",
        "dlg:top": "80",
        "dlg:width": "280",
        "dlg:height": "210",
        "dlg:closeable": "true",
        "dlg:moveable": "true",
        "dlg:withtitlebar": "false"
    })

    bul_inboard = ET.SubElement(root, "dlg:bulletinboard")

    top = 10
    for i, ov in enumerate(option_vars, start=1):
        logger.debug("range '%s' for option '%s:%s'", i, ov.name, ov.vtype)
        top += 20

        # If var == boolean, we attribute it a checkbox
        if ov.vtype == "boolean":
            logger.debug('Adding boolean: %s', ov.name)
            dg = CheckBox(top, ov.name, str(i), ov.label, ov.default)
            ET.SubElement(bul_inboard, 'dlg:checkbox', dg.dict)

        # If var == string, we split it in two: label and text_field
        elif ov.vtype == "string":
            logger.debug('Adding string: %s', ov.name)
            label = Label(top, f"{ov.name}{i}", str(i+len(option_vars)), ov.label)
            text_field = TextField(top, ov.name, i, ov.default)
            ET.SubElement(bul_inboard, 'dlg:text', label.dict)
            ET.SubElement(bul_inboard, 'dlg:textfield', text_field.dict)

    with open(path_file, "w", encoding='UTF-8') as xf:
        doc_type = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE dlg:window ' \
                   'PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "dialog.dtd">'
        tostring = ET.tostring(root).decode('utf-8')
        file = f"{doc_type}{tostring}"
        xf.write(file)

    logger.info("%s created in -> %s", xml_file, file_location)


if __name__ == "__main__":
    from create_config_xcs import test_values
    with open('logging_conf.yaml', 'r') as f:
        log_cfg = yaml.safe_load(f.read())
        logging.config.dictConfig(log_cfg)
    logger.setLevel('DEBUG')
    create_dialog(test_values)
