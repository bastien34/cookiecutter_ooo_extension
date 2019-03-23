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
    def __init__(self, name, txt, attrib={}):
        attrib.update({'oor:name': name})
        super().__init__("prop", attrib)
        self.append(Elem("value", text=txt))


class ElemPropLoc(ElemProp):
    def __init__(self, name, langs, attrib={}):
        super().__init__(name, attrib)
        for lang, value in langs.items():
            self.append(Elem("value", {"xml:lang": lang}, text=value))
