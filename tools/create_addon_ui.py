#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import logging
import xml.etree.ElementTree as ET
from _elementtree import Element


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('create_addon_ui')

extension_id = 'com.pwd.myextension'
package_name = '{{cookiecutter.package_name}}'
xml_file = 'DEV_AddonUI.xcu'

# my_func will contain data from odt file about commands to add in menu
my_func = ['{{cookiecutter.extension_label}}', 'tatar']


def value_element(parent, text='', attrib={}):
    el = ET.SubElement(parent, 'value', attrib)
    el.text = text
    return el


def prop_element(parent, name, text='', locale=False):
    """
    Generate a <prop> node. If locale==True, then value added
    has a locale parameter: lang:"fr"
    """
    attrib = {'oor:type': 'xs:string', 'name': name}
    el = ET.SubElement(parent, 'prop', attrib)
    if locale:
        return value_element(el, text, {'oor:lang': 'fr'})
    else:
        return value_element(el, text)


class _MenuEntry(Element):
    """Menu entry. Element with nested <prop>"""
    def __init__(self, i, function_label):
        tag = "node"
        attrib = {"oor:name": "N00%s" % i, "oor:op": "replace"}
        super().__init__(tag, attrib)
        self.context = self._get_prop('Context',
                                      "com.sun.star.text.TextDocument")
        self.title = self._get_prop('Title', function_label, locale=True)
        macro_url = 'vnd.sun.star.script:{{cookiecutter.extension_name}}-' \
                    '{{cookiecutter.extension_version}}.oxt|python|{{cookiecu' \
                    'tter.extension_name}}.py${{cookiecutter.extension_name}}' \
                    '_launcher?language=Python&amp;location=user:uno_packages'
        self.url = self._get_prop('URL', macro_url)
        self.target = self._get_prop('Target', '_self')

    def _get_prop(self, name, text, locale=False):
        logger.info('Creation of prop %s' % name)
        return prop_element(self, name, text, locale)


class SubMenuEntry(Element):
    def __init__(self):
        attrib = {'name': "{{cookiecutter.package_name}}",
                  "oor:op": "replace"}
        node = 'node'
        super().__init__(node, attrib)
        prop_element(self, 'Context')
        prop_element(self, 'Title', '{{cookiecutter.company_name}}',
                     locale=True)
        submenu = ET.SubElement(self, 'node', {'oor:name': 'Submenu'})

        for i, func in enumerate(my_func, start=1):
            sm = _MenuEntry(i=i, function_label=func)
            submenu.append(sm)


def create_addon():
    """
    Creation of OptionsDialog.xcu
    """
    path = os.path.dirname(os.path.realpath(__file__))
    logger.info('Creating xcu in: %s' % path)

    with open(xml_file, "w", encoding="utf-8") as f:
        root = Element("oor:component-data",
                       {"oor:name": "Addons",
                        "oor:package": "org.openoffice.Office",
                        "xmlns:oor": "http://openoffice.org/2001/registry",
                        "xmlns:xs": "http://www.w3.org/2001/XMLSchema"})
        addon_ui = ET.SubElement(root, "node", {'oor:name': "AddonUI"})
        menubar = ET.SubElement(addon_ui, "node", {'oor:name': "OfficeMenuBar"})
        menubar.append(SubMenuEntry())

        toolbar = ET.SubElement(addon_ui, "node", {'oor:name': "OfficeToolBar"})
        images = ET.SubElement(addon_ui, "node", {'oor:name': "Images"})


        tree = ET.ElementTree(root)
        tree.write(f.name, "utf-8", True)

    logger.info('%s has been created. Thanks for support !' % xml_file)


if __name__ == "__main__":
    create_addon()
