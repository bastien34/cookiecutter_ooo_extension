#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import shutil

import yaml
import os
import xml.etree.ElementTree as ET
from _elementtree import Element

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("post_get_project")

# General
EXTENSION_FILENAME = "{{cookiecutter.extension_name}}-{{cookiecutter.extension_version}}.oxt"
MODULE = "{{cookiecutter.extension_name}}"
DIALOG_LOCATION = "../{{cookiecutter.extension_name}}/src/dialogs"
DIALOG_FILE = "{{cookiecutter.extension_name}}_dialog.xdl"
ADDONUI_LOCATION = "../{{cookiecutter.extension_name}}/src/"
ADDONUI_FILE = "AddonUI.xcu"
CONFIG_LOCATION = "../{{cookiecutter.extension_name}}/src/config"
CONFIG_FILE = "{{cookiecutter.extension_name}}_config.xcs"
ICON_LOCATION = "../{{cookiecutter.extension_name}}/src/icons"
IMAGE_LOCATION = "../{{cookiecutter.extension_name}}/src/images"


# --------------------------- Dialog window creation  -------------------------
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
    path_file = os.path.join(DIALOG_LOCATION, DIALOG_FILE)
    logger.debug('Start creating %s.', path_file)

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
    for i, d in enumerate(option_vars.values(), start=1):
        top += 20
        vtype = d['type']
        # If var == boolean -> checkbox
        if vtype == "boolean":
            dg = CheckBox(top, d['name'], str(i), d['label'], d['default'])
            ET.SubElement(bul_inboard, 'dlg:checkbox', dg.dict)

        # If var == string, we split it in two: label and text_field
        elif vtype == "string":
            label = Label(top, f"{d['name']}{i}", str(i + len(option_vars)),
                          d['label'])
            text_field = TextField(top, d['name'], i, d['default'])
            ET.SubElement(bul_inboard, 'dlg:text', label.dict)
            ET.SubElement(bul_inboard, 'dlg:textfield', text_field.dict)
        else:
            raise TypeFunctionNotSupportedError(vtype)

    with open(path_file, "w", encoding='UTF-8') as xf:
        doc_type = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE dlg:window ' \
                   'PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "dialog.dtd">'
        tostring = ET.tostring(root).decode('utf-8')
        file = f"{doc_type}{tostring}"
        xf.write(file)

    logger.info("%s created in -> %s", DIALOG_FILE, DIALOG_LOCATION)


# ------------------------------ AddonUI creation  ----------------------------


class Function:
    """
    Define a function.
    Warning: Location attribute contains an ampersand "&" that must
    be converted as "&amp;" in xml file.
    """

    def __init__(self, name, label, icon):
        self.name = name
        self.label = label
        self.icon = icon

    @property
    def location(self):
        return f"vnd.sun.star.script:{EXTENSION_FILENAME}|python" \
            f"|{MODULE}.py${self.name}?language=Python&location=user:" \
            f"uno_packages"

    def __repr__(self):
        return f'{self.name}: {self.label}'


class Elem(ET.Element):
    """
    xml.etree.ElementTree.Element
    """

    def __init__(self, tag, attrib={}, **kwargs):
        if "text" in kwargs:
            txt = kwargs.pop("text")
            super().__init__(tag, attrib, **kwargs)
            self._text(txt)
        else:
            super().__init__(tag, attrib, **kwargs)

    def _text(self, txt):
        self.text = txt


class ElemProp(Element):
    """
    Helper class, force name attribute. Build a node <prop> with
    a nested <value>.
    """

    def __init__(self, name, txt='', attrib={}):
        attrib.update({'oor:name': name})
        super().__init__("prop", attrib)
        self.append(Elem("value", text=txt))


def create_str_prop(name, txt='', attrib={}):
    attrib.update({'oor:type': 'xs:string'})
    return ElemProp(name, txt, attrib)


def create_str_loc_prop(name, langs, attrib={}):
    """build node <prop> with a child <value> containing
    text and locale information."""
    attrib.update({'oor:type': 'xs:string',
                   'oor:name': name})
    el = Elem('prop', attrib)
    for lang, value in langs.items():
        el.append(Elem("value", {"xml:lang": lang}, text=value))
    return el


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
        self.append(
            create_str_prop("Context", "com.sun.star.text.TextDocument"))
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

    def __init__(self, funcs):
        logger.debug('Adding a Menubar')
        attrib = {"oor:name": "{{cookiecutter.package_name}}",
                  "oor:op": "replace"}
        node = "node"
        super().__init__(node, attrib)
        self.append(create_str_prop("Context"))
        self.append(create_str_loc_prop(
            "Title", {'fr': "{{cookiecutter.company_name}}"}))
        submenu = ET.SubElement(self, "node", {"oor:name": "Submenu"})
        for i, func in enumerate(funcs, start=1):
            submenu.append(MenuEntry(i, func))


class ToolBar(Element):
    """
    Build the Toolbar for all functions listed my_func.
    """

    def __init__(self, funcs):
        logger.debug('Adding a Toolbar')
        attrib = {"oor:name": "{{cookiecutter.package_name}}.TB1",
                  "oor:op": "replace"}
        node = "node"
        super().__init__(node, attrib)
        for i, func in enumerate(funcs, start=1):
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


def create_addon(funcs):
    """
    Creation of AddonUI.xcu which contains Toolbar and Menubar
    configuration.
    """
    path_file = os.path.join(ADDONUI_LOCATION, ADDONUI_FILE)
    logger.debug('Start creating %s.', path_file)

    root = Element("oor:component-data",
                   {"xmlns:oor": "http://openoffice.org/2001/registry",
                    "xmlns:xs": "http://www.w3.org/2001/XMLSchema",
                    "oor:name": "Addons",
                    "oor:package": "org.openoffice.Office"})

    with open(path_file, "w", encoding="UTF-8") as xf:
        addon_ui = ET.SubElement(root, "node", {"oor:name": "AddonUI"})

        # Menubar
        mb = ET.SubElement(addon_ui, "node", {"oor:name": "OfficeMenuBar"})
        mb.append(MenuBar(funcs))

        # Toolbar
        tb = ET.SubElement(addon_ui, "node", {"oor:name": "OfficeToolBar"})
        tb.append(ToolBar(funcs))

        # Images
        images = ET.SubElement(addon_ui, "node", {"oor:name": "Images"})
        for i, func in enumerate(funcs, start=1):
            images.append(Image(i, func))
            insert_image(func.icon, ICON_LOCATION)

        tree = ET.ElementTree(root)
        tree.write(xf.name, "utf-8", True)

    logger.debug("AddonUI created in -> %s", path_file)


# ---------------------------- CONFIX.XCS creation  ---------------------------

def create_config_xcs(option_vars):
    """
    Creation of OptionsDialog.xcu.

    This file contains description of options var and their default
    values.

    Its parameter is a list of Var Instance.
    """
    path_file = os.path.join(CONFIG_LOCATION, CONFIG_FILE)
    logger.debug('Start creating %s.', path_file)
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
        for ov in option_vars.values():
            vtype = f'xs:{ov["type"]}'
            ET.SubElement(group, 'prop', {'oor:name': ov["name"],
                                          'oor:type': vtype})
            defaults.append(ElemProp(ov["name"], ov["default"],
                                     {'oor:type': vtype}))
        # Component
        cmp = ET.SubElement(root, 'component')
        leaves = ET.SubElement(cmp, 'group', {'oor:name': 'Leaves'})
        leaves.append(
            Elem('node-ref', {'oor:name': "{{cookiecutter.extension_name}}",
                              'oor:node-type': "Production"}))

        tree = ET.ElementTree(root)
        tree.write(xf.name, "utf-8", True)

    logger.info("Config XCS created in -> %s", path_file)


# ------------------------------ Exceptions -----------------------------------

def insert_image(filename, new_fn):
    logger.debug('Working Dir: %s', os.path.abspath(__file__))
    if os.path.exists(filename):
        os.rename(filename, new_fn)
    else:
        pass
        # raise ImageNotFoundError(filename)


class ImageNotFoundError(Exception):
    """Raises if icon or extension image not found."""

    def __init__(self, name):
        logger.error('ImageNotFoundError: check filename <%s>', name)
        self.message = f"Image <{name}> from your config not found in './'." \
            "Check filename or put image next to Extension " \
            "Generator!"

    def __str__(self):
        return str(self.message)


class TypeFunctionNotSupportedError(Exception):
    """Raises if icon or extension image not found."""

    def __init__(self, vtype):
        logger.error('Type <%s> not supported yet. Contribute!', vtype)
        self.message = f"Sorry, the type <{vtype}> is not supported Yet. " \
            f"You're welcome to contribute!"

    def __str__(self):
        return str(self.message)


# -----------------------------------------------------------------------------


def finalize():
    variables = yaml.load("{{cookiecutter.vars}}")
    create_dialog(variables)
    create_config_xcs(variables)

    funcs = yaml.load("{{cookiecutter.funcs}}")
    fs = []
    for f in funcs.values():
        fs.append(Function(*f.values()))
        # force demo entry
    fs.append(Function("{{cookiecutter.extension_name}}_launcher", 'Demo', 'bal_16.png'))
    create_addon(fs)
    return 1


def zip_files():
    logger.debug(
        'Zipping file to {{cookiecutter.extension_name}}-{{cookiecutter.extension_version}}.oxt')
    extension_path = 'extension/'
    oxt = os.path.join(
        extension_path,
        "{{cookiecutter.extension_name}}-{{cookiecutter.extension_version}}.oxt"
    )
    shutil.make_archive(oxt, 'zip', 'src/')
    os.rename(oxt + '.zip', oxt)
    logger.info("Extension <%s> ready to be installed. Thanks!",
                EXTENSION_FILENAME)
    return 1


finalize()

zip_files()
