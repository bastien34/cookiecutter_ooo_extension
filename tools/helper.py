#!/usr/bin/python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from _elementtree import Element


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


class ElemPropStr(ElemProp):
    """
    Helper class. Force {'oor:type': 'xs:string'}
    """
    def __init__(self, name, txt='', attrib={}):
        attrib.update({'oor:type': 'xs:string'})
        super().__init__(name, txt, attrib)


class ElemPropLoc(Elem):
    """
    Helper to build node <prop> with a nested <value> containing
    text and locale information.
    """
    def __init__(self, name, langs, attrib={}):
        attrib.update({'oor:name': name})
        super().__init__('prop', attrib)
        for lang, value in langs.items():
            self.append(Elem("value", {"xml:lang": lang}, text=value))
