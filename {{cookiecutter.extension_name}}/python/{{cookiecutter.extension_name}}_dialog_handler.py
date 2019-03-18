# -*- coding: utf-8 -*-

import unohelper
from {{cookiecutter.extension_name}} import options_dialog

IMPLEMENTATION_NAME = "{{cookiecutter.package_name}}.IM"
SERVICE_NAME = "{{cookiecutter.package_name}}.service"


def create(ctx, *args):
    return options_dialog.create(
        ctx,
        *args,
        implementation_name=IMPLEMENTATION_NAME,
        service_name=SERVICE_NAME
    )


g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
    create, IMPLEMENTATION_NAME, (SERVICE_NAME,),
)
