#
#  {{cookiecutter.extension_name}}.py
#
#  Copyright 2019 {{cookiecutter.author_name}} <{{cookiecutter.author_email}}>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
import logging
from {{cookiecutter.extension_name}}_utils import (
    msgbox,
    get_config,
)
from {{cookiecutter.extension_name}}.options_dialog import NODE, KEYS

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('{{cookiecutter.extension_name}}')


class Environ:
    """
    Supply environment keys.
        eg: env = Environ()
            my_url = env.URL
    """

    def __init__(self):
        d = get_config(NODE, KEYS)
        self.__dict__.update(d)


def {{cookiecutter.extension_name}}_launcher(*args):
    """
    Launcher for creating a MissionBal2Word document.
    """

    print('launcher called')
    {% for k, v in cookiecutter.vars.items() %}
    logger.debug('Environ <%s>: %s', "{{k}}.label", Environ().{{v.name}})
    {% endfor %}

    msg = """
    {% for k, v in cookiecutter.vars.items() %}
    option: <{{ k }}>: {{ v.default }}
    {% endfor %}
    """
    msgbox(msg)



g_exportedScripts = {{cookiecutter.extension_name}}_launcher
