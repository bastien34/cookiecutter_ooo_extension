#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import logging
import xml.etree.ElementTree as ET
from _elementtree import Element

extension_filename = "{{cookiecutter.extension_name}}-{{cookiecutter.extension_version}}.oxt"
extension_id = "com.pwd.myextension"
package_name = "{{cookiecutter.package_name}}"
xml_file = "AddonUI.xcu"  # To be adjusted in the right location
locale = {"xml:lang": "fr"}

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("Now, it's time to create the %s file!" % xml_file)


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
func1 = Function('send_mail', 'Send Mail', 'send_mail_ico.png')
func2 = Function('send_letter', 'Send Nice Letter', 'send_letter.png')

# my_func will contain data from odt file about commands to add in menu
my_func = [func1, func2]


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

    def __init__(self, i, func):
        tag = "node"
        name = self.format_name(i)
        attrib = {"oor:name": name, "oor:op": "replace"}
        super().__init__(tag, attrib)
        self.append(PropElement("Context", "com.sun.star.text.TextDocument"))
        self.append(PropElement("Title", func.label, loc=True))
        self.append(PropElement("URL", func.location))
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
            submenu.append(MenuEntry(i, func))


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
        self.append(PropElement("URL", func.location))
        nod = ET.SubElement(self, "node", {"oor:name": "UserDefinedImages"})
        icon_location = "%origin%/icons/{}".format(func.icon)
        nod.append(PropElement("ImageSmallURL", icon_location))


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

        menubar = ET.SubElement(addon_ui, "node",
                                {"oor:name": "OfficeMenuBar"})
        menubar.append(MenuBar())

        toolbar = ET.SubElement(addon_ui, "node",
                                {"oor:name": "OfficeToolBar"})
        toolbar.append(ToolBar())

        images = ET.SubElement(addon_ui, "node", {"oor:name": "Images"})
        for i, func in enumerate(my_func, start=1):
            images.append(Image(i, func))

        tree = ET.ElementTree(root)
        tree.write(f.name, "utf-8", True)
    logger.info("%s has been created. Thanks for support !" % xml_file)


if __name__ == "__main__":
    create_addon()
