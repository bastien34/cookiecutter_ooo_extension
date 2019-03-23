#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import logging
import xml.etree.ElementTree as ET
from _elementtree import Element


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("create_addon_ui")

extension_id = "com.pwd.myextension"
package_name = "{{cookiecutter.package_name}}"
xml_file = "DEV_AddonUI.xcu"
locale = {"xml:lang": "fr"}

# my_func will contain data from odt file about commands to add in menu
my_func = ["{{cookiecutter.extension_label}}"]


class PropElement(Element):
    """
    In AddonUI.xcu, a <prop> element has always an attrib `oor:type` and
    `oor:name and a <value> as child element.
    If a text is given, it will contained in <value> element.
    If loc then a dict attrib is appended to <value> element:
        {"xml:lang": "fr"}
    """
    def __init__(self, name, text="", loc=False):
        tag = "prop"
        attrib = {"oor:type": "xs:string", "oor:name": name}
        self.locale = {}
        super().__init__(tag, attrib)
        if loc:
            self.locale = locale
        value = ET.SubElement(self, "value", self.locale)
        value.text = text


class MenuEntry(Element):
    """
    Menu entry. Element with nested <prop>. Both Toolbar and Menubar
    use it.
    """
    def __init__(self, i, function_label):
        tag = "node"
        name = self.format_name(i)
        attrib = {"oor:name": name, "oor:op": "replace"}
        super().__init__(tag, attrib)
        self.append(PropElement("Context", "com.sun.star.text.TextDocument"))
        self.append(PropElement("Title", function_label, loc=True))
        macro_url = """vnd.sun.star.script:{{cookiecutter.extension_name}}-{{cookiecutter.extension_version}}.oxt|python|{{cookiecutter.extension_name}}.py${{cookiecutter.extension_name}}_launcher?language=Python&amp;location=user:uno_packages"""
        self.append(PropElement("URL", macro_url))
        self.append(PropElement("Target", "_self"))

    @staticmethod
    def format_name(i):
        return "N00%s" % i


class MenuBar(Element):
    """
    Build the Menubar for all functions listed in my_func.
    """
    def __init__(self):
        attrib = {"oor:name": "{{cookiecutter.package_name}}",
                  "oor:op": "replace"}
        node = "node"
        super().__init__(node, attrib)
        self.append(PropElement("Context"))
        self.append(PropElement("Title", "{{cookiecutter.company_name}}",
                                loc=True))
        submenu = ET.SubElement(self, "node", {"oor:name": "Submenu"})
        for i, func in enumerate(my_func, start=1):
            submenu.append(MenuEntry(i=i, function_label=func))


class ToolBar(Element):
    """
    Build the Toolbar for all functions listed my_func.
    """
    def __init__(self):
        attrib = {"oor:name": "{{cookiecutter.package_name}}.TB1",
                  "oor:op": "replace"}
        node = "node"
        super().__init__(node, attrib)

        for i, func in enumerate(my_func, start=1):
            entry = MenuEntry(i=i, function_label=func)
            self.append(entry)


class Image(Element):
    """
    A class to hold icons used in toolbar.
    """
    def __init__(self, i):
        tag = "node"
        name = "{{cookiecutter.package_name}}.%s" % MenuEntry.format_name(i)
        attrib = {"oor:name": name, "oor:op": "replace"}
        super().__init__(tag, attrib)
        val = "vnd.sun.star.script:{{cookiecutter.extension_name}}-{{cookiec" \
              "utter.extension_version}}.oxt|python|{{cookiecutter.extension" \
              "_name}}.py${{cookiecutter.extension_name}}_launcher?language=" \
              "Python&amp;location=user:uno_packages"
        self.append(PropElement("URL", val))
        nod = ET.SubElement(self, "node", {"oor:name": "UserDefinedImages"})
        nod.append(PropElement("ImageSmallURL", "%origin%/icons/bal_16.png"))


def create_addon():
    """
    Creation of OptionsDialog.xcu
    """
    path = os.path.dirname(os.path.realpath(__file__))
    logger.info("Creating xcu in: %s" % path)

    root = Element("oor:component-data",
                   {"xmlns:oor": "http://openoffice.org/2001/registry",
                    "xmlns:xs": "http://www.w3.org/2001/XMLSchema",
                    "oor:name": "Addons",
                    "oor:package": "org.openoffice.Office"})

    with open(xml_file, "w", encoding="UTF-8") as f:
        addon_ui = ET.SubElement(root, "node", {"oor:name": "AddonUI"})

        menubar = ET.SubElement(addon_ui, "node", {"oor:name": "OfficeMenuBar"})
        menubar.append(MenuBar())

        toolbar = ET.SubElement(addon_ui, "node", {"oor:name": "OfficeToolBar"})
        toolbar.append(ToolBar())

        images = ET.SubElement(addon_ui, "node", {"oor:name": "Images"})
        for i, func in enumerate(my_func, start=1):
            images.append(Image(i=i))

        tree = ET.ElementTree(root)
        tree.write(f.name, "utf-8", True)
    logger.info("%s has been created. Thanks for support !" % xml_file)


if __name__ == "__main__":
    create_addon()
