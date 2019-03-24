#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import logging.config
import logging
import xml.etree.ElementTree as ET
from _elementtree import Element

import yaml
from helper import (create_str_prop,
                    create_str_loc_prop)

extension_filename = "{{cookiecutter.extension_name}}-{{cookiecutter.extension_version}}.oxt"
extension_id = "com.pwd.myextension"
package_name = "{{cookiecutter.extension_name}}"
xml_file = "../tmp/AddonUI.xcu"  # To be adjusted in the right location


logger = logging.getLogger(__name__)


class Function:
    """
    Define a function.

    Warning: Location has an ampersand "&" that must be converted as "&amp;"
    into the xml file.
    """

    def __init__(self, name, label, icon):
        self.name = name
        self.label = label
        self.icon = icon

    @property
    def location(self):
        return f"vnd.sun.star.script:{extension_filename}|python" \
            f"|{package_name}.py${self.name}?language=Python&location=user:" \
            f"uno_packages"


# Test values: these data should be collected from odt file.
func1 = Function('{{cookiecutter.extension_name}}_launcher',
                 '{{cookiecutter.extension_label}}',
                 'bal_16.png')
func2 = Function('send_letter', 'Send Nice Letter', 'send_letter.png')

# my_func will contain data from odt file about commands to add in menu
my_func = [func1, ]


class MenuEntry(Element):
    """
    Menu entry. Element with nested <prop>. Both Toolbar and Menubar
    use it.
    """

    def __init__(self, i, func):
        tag = "node"
        name = self.format_name(i)
        attrib = {"oor:name": name, "oor:op": "replace"}
        super().__init__(tag, attrib)
        self.append(create_str_prop("Context", "com.sun.star.text.TextDocument"))
        self.append(create_str_loc_prop("Title", {'fr': func.label}))
        self.append(create_str_prop("URL", func.location))
        self.append(create_str_prop("Target", "_self"))

    @staticmethod
    def format_name(i):
        return "N00%s" % i


class MenuBar(Element):
    """
    Build the Menubar for all functions listed in my_func.
    """

    def __init__(self):
        logger.debug('Adding a Menubar')
        attrib = {"oor:name": "{{cookiecutter.package_name}}",
                  "oor:op": "replace"}
        node = "node"
        super().__init__(node, attrib)
        self.append(create_str_prop("Context"))
        self.append(create_str_loc_prop(
            "Title", {'fr': "{{cookiecutter.company_name}}"}))
        submenu = ET.SubElement(self, "node", {"oor:name": "Submenu"})
        for i, func in enumerate(my_func, start=1):
            submenu.append(MenuEntry(i, func))


class ToolBar(Element):
    """
    Build the Toolbar for all functions listed my_func.
    """

    def __init__(self):
        logger.debug('Adding a Toolbar')
        attrib = {"oor:name": "{{cookiecutter.package_name}}.TB1",
                  "oor:op": "replace"}
        node = "node"
        super().__init__(node, attrib)
        for i, func in enumerate(my_func, start=1):
            self.append(MenuEntry(i, func))


class Image(Element):
    """
    A class to hold icons used in toolbar. Icons are located in `icons/`.
    Func is a Func object.
    """

    def __init__(self, i, func):
        tag = "node"
        name = "{{cookiecutter.package_name}}.%s" % MenuEntry.format_name(i)
        attrib = {"oor:name": name, "oor:op": "replace"}
        super().__init__(tag, attrib)
        self.append(create_str_prop("URL", func.location))
        nod = ET.SubElement(self, "node", {"oor:name": "UserDefinedImages"})
        icon_location = "%origin%/icons/{}".format(func.icon)
        nod.append(create_str_prop("ImageSmallURL", icon_location))


def create_addon():
    """
    Creation of OptionsDialog.xcu
    """
    logger.debug("Well, it's time to create `%s`.", xml_file)
    path = os.path.dirname(os.path.realpath(__file__))
    logger.debug("We create %s in: %s", xml_file, path)

    root = Element("oor:component-data",
                   {"xmlns:oor": "http://openoffice.org/2001/registry",
                    "xmlns:xs": "http://www.w3.org/2001/XMLSchema",
                    "oor:name": "Addons",
                    "oor:package": "org.openoffice.Office"})

    with open(xml_file, "w", encoding="UTF-8") as f:
        addon_ui = ET.SubElement(root, "node", {"oor:name": "AddonUI"})
        # Menubar
        mb = ET.SubElement(addon_ui, "node", {"oor:name": "OfficeMenuBar"})
        mb.append(MenuBar())
        # Toolbar
        tb = ET.SubElement(addon_ui, "node", {"oor:name": "OfficeToolBar"})
        tb.append(ToolBar())
        # Images
        images = ET.SubElement(addon_ui, "node", {"oor:name": "Images"})
        for i, func in enumerate(my_func, start=1):
            images.append(Image(i, func))

        tree = ET.ElementTree(root)
        tree.write(f.name, "utf-8", True)
    logger.info("%s has been created.", xml_file)


if __name__ == "__main__":
    with open('logging_conf.yaml', 'r') as f:
        log_cfg = yaml.safe_load(f.read())
        logging.config.dictConfig(log_cfg)
    create_addon()
