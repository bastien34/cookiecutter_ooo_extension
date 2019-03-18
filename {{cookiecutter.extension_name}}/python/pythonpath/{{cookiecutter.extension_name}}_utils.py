# -*- coding: utf-8 -*-

import os
import uno
import pyuno
from com.sun.star.beans import PropertyValue
from com.sun.star.uno import RuntimeException
from com.sun.star.awt.MessageBoxType import (MESSAGEBOX, INFOBOX,
                                             ERRORBOX, WARNINGBOX, QUERYBOX)


def get_config(node, keys):
    """Returns settings as a dict."""
    settings = {}
    reader = getConfigurationAccess(node)
    values = reader.getPropertyValues(keys)
    for key, value in zip(keys, values):
        if not value and reader.Defaults.hasPropertyByName(key):
            value = reader.Defaults.getPropertyValue(key)
        settings[key] = value
    return settings


def createUnoService(service, ctx=None, args=None):
    if not ctx:
        ctx = uno.getComponentContext()
    smgr = ctx.getServiceManager()
    if ctx and args:
        return smgr.createInstanceWithArgumentsAndContext(service, args, ctx)
    elif args:
        return smgr.createInstanceWithArguments(service, args)
    elif ctx:
        return smgr.createInstanceWithContext(service, ctx)
    else:
        return smgr.createInstance(service)


def getConfigurationAccess(nodevalue, updatable=False):
    cp = createUnoService("com.sun.star.configuration.ConfigurationProvider")
    node = PropertyValue("nodepath", 0, nodevalue, 0)
    if updatable:
        return cp.createInstanceWithArguments(
            "com.sun.star.configuration.ConfigurationUpdateAccess", (node,))
    else:
        return cp.createInstanceWithArguments(
            "com.sun.star.configuration.ConfigurationAccess", (node,))


def getProductName():
    key = "/org.openoffice.Setup/Product"
    reader = getConfigurationAccess(key)
    return reader.ooName


def mri(target):
    """Macro to instantiate Mri introspection tool from hanya."""
    try:
        mri = createUnoService("mytools.Mri")
        mri.inspect(target)
    except (RuntimeException, AttributeError):
        print('Fail loading MRI')
        msgbox('MRI is not installed.\nPlease visit:\n'
               'http://extensions.services.openoffice.org',
               'Error', 'error')


def msgbox(message, titre="Message", boxtype='message', boutons=1, frame=None):
    types = {'message': MESSAGEBOX, 'info': INFOBOX, 'error': ERRORBOX,
             'warning': WARNINGBOX, 'query': QUERYBOX}
    tk = createUnoService("com.sun.star.awt.Toolkit")
    if not frame:
        desktop = createUnoService("com.sun.star.frame.Desktop")
        frame = desktop.ActiveFrame
        if frame.ActiveFrame:
            # top window is a subdocument
            frame = frame.ActiveFrame
    win = frame.ComponentWindow
    box = tk.createMessageBox(win, types[boxtype], boutons, titre, message)
    return box.execute()


def path_to_url(path):
    if not path.startswith('file://'):
        return pyuno.systemPathToFileUrl(os.path.realpath(path))


def get_package_path(file_to_find):
    """
    Returns the path for template or image, using the constant TEMPLATE_NAME
    or LOGO_URL, which does not start with a "/".
    """
    working_dir = os.path.join(os.path.dirname(__file__), file_to_find)
    path = os.path.normpath(working_dir)
    if path.startswith('file:'):
        path = path.split(':')[1]
    assert os.path.isfile(path)
    return path_to_url(path)
