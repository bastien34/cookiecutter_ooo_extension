#!/usr/bin/python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET


class Elem(ET.Element):
    """
    xml.etree.ElementTree.Element
    tag: tag name
    attrib: dict with attributes
    kwargs: look at the parent class
    """

    def __init__(self, tag, attrib={}, **kwargs):
        """This init is a copy of parent class ET.Element"""
        print(tag, attrib)
        if "text" in kwargs:
            txt = kwargs["text"]
            print('text in kwargs %s' % txt)
            del kwargs["text"]
            super().__init__(tag, attrib, **kwargs)
            self._text(txt)
        else:
            super().__init__(tag, attrib, **kwargs)

    def _text(self, txt):
        self.text = txt


class ElemProp(Elem):
    def __init__(self, name, txt):
        super().__init__("prop", {'oor:name': name})
        self.append(Elem("value", text=txt))


class ElemPropLoc(Elem):
    def __init__(self, name, langs):
        super().__init__("prop", {'oor:name': name})
        for lang, value in langs.items():
            self.append(Elem("value", {"xml:lang": lang}, text=value))
