#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import logging
import xml.etree.ElementTree as ET
from helper import Elem, ElemProp, ElemPropLoc


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('create_addon_ui')

extension_id = 'com.pwd.myextension'
xml_file = 'DEV_AddonUI.xcu'


class ElemLeaf(Elem):
    def __init__(self, attrs):
        if "Id" not in attrs:
            attrs["Id"] = attrs["Name"]
        attrs["OptionsPage"] = "%origin%/dialogs/optionsdialog.xdl"
        attrs["EventHandlerService"] = extension_id
        super().__init__("node",
                         {'oor:name': attrs.pop("Name"), "oor:op": "fuse"})
        for key, val in attrs.items():
            if key == "Label":
                self.append(ElemPropLoc(key, val))
            else:
                self.append(ElemProp(key, val))


class ElemNode(Elem):
    def __init__(self, attrs, *, leaves=None):
        super().__init__("node",
                         {'oor:name': attrs.pop("Name"), "oor:op": "fuse"})
        for key, val in attrs.items():
            if key == "Label":
                self.append(ElemPropLoc(key, val))
            else:
                self.append(ElemProp(key, val))
        if leaves is not None:
            self.append(Elem("node", {'oor:name': "Leaves"}))
            for leaf in leaves:
                self[-1].append(leaf)


class ElemOrderdNode(Elem):
    def __init__(self, name, index=None):
        super().__init__("node", {'oor:name': name, "oor:op": "fuse"})
        if index is not None:
            self.append(ElemProp("Index", index))


class ElemModule(Elem):
    def __init__(self, name,
                 nodes):
        super().__init__("node", {'oor:name': name, "oor:op": "fuse"})
        self.append(Elem("node", {'oor:name': "Nodes"}))
        for node in nodes:
            self[-1].append(node)


class ElemSingleOption(Elem):
    def __init__(self, name):
        super().__init__("node", {'oor:name': name, "oor:op": "fuse"})
        self.append(ElemProp("Hide", "true"))


class ElemOptionsPage(Elem):
    def __init__(self, name, *, hide=None, singleoptions=None):
        super().__init__("node", {'oor:name': name, "oor:op": "fuse"})
        if hide is not None:
            self.append(ElemProp("Hide", "true"))
        if singleoptions is not None:
            self.append(Elem("node", {'oor:name': "Options"}))
            for singleoption in singleoptions:
                self[-1].append(
                    singleoption)


class ElemOptionsGroup(Elem):
    def __init__(self, name, *, hide=None, optionspages=None):
        super().__init__("node", {'oor:name': name, "oor:op": "fuse"})
        if hide is not None:
            self.append(ElemProp("Hide", "true"))
        if optionspages is not None:
            self.append(Elem("node", {'oor:name': "Pages"}))
            for optionspage in optionspages:
                self[-1].append(
                    optionspage)


def create_config_xcu():
    """
    Creation of OptionsDialog.xcu
    """
    path = os.path.dirname(os.path.realpath(__file__))
    logger.info('Creating xcu in: %s' % path)

    with open(xml_file, "w", encoding="utf-8") as f:
        root = Elem("oor:component-data",
                    {"oor:name": "Addons",
                     "oor:package": "org.openoffice.Office",
                     "xmlns:oor": "http://openoffice.org/2001/registry",
                     "xmlns:xs": "http://www.w3.org/2001/XMLSchema"})

        root.append(Elem("node", {'oor:name': "AddonUI"}))
        root[-1].append(Elem("node", {'oor:name': "OfficeMenuBar"}))
        root[-1].append(Elem("node", {'oor:name': "OfficeToolBar"}))
        root[-1].append(Elem("node", {'oor:name': "Images"}))

        attrib = {'oor:name': extension_id,
                  'oor:op': "replace"}

        leaf = Elem("node", attrib)
        root[-1].append(leaf)

        # root.append(Elem("node", {'oor:name': "Modules"}))
        # orderednode = ElemOrderdNode(
        #     name)
        # node = ElemModeule("com.sun.star.text.TextDocument", (
        #     orderednode,))
        # root[-1].append(node)
        #
        # root.append(Elem("node", {
        #     'oor:name': "OptionsDialogGroups"}))
        # security = ElemOptionsPage("Security",
        #                            hide=True)
        # memory = ElemOptionsPage("Memory",
        #                          hide=True)
        # productname = ElemOptionsGroup("ProductName", optionspages=(security,
        #                                                             memory))
        # root[-1].append(
        #     productname)
        # internet = ElemOptionsGroup("Internet",
        #                             hide=True)
        # root[-1].append(
        #     internet)
        #
        tree = ET.ElementTree(root)
        tree.write(f.name, "utf-8", True)

    logger.info('%s has been created. Thanks for support !' % xml_file)


if __name__ == "__main__":
    create_config_xcu()
