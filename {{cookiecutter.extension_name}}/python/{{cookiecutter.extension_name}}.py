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

from {{cookiecutter.extension_name}}_utils import (
    msgbox,
    get_config,
)
from {{cookiecutter.extension_name}}.options_dialog import NODE, KEYS


class Environ:
    """
    Supply environment keys.
        eg: env = Environ()
            my_url = env.URL
    """

    def __init__(self):
        self.node = NODE
        self.keys = KEYS
        self.settings = get_config(self.node, self.keys)
        self.test_mode = self.settings.get('test_mode')
        self._load_vars()

    def _load_vars(self):
        if self.test_mode:
            self._url = 'dev_url'
            self._token = 'dev_token'
            self._prestation_path = 'prestation_dev_path'
        else:
            self._url = 'url'
            self._token = 'token'
            self._prestation_path = 'prestation_path'

    @property
    def URL(self):
        return self.settings.get(self._url)

    @property
    def TOKEN(self):
        return self.settings.get(self._token)

    @property
    def PRESTATION_PATH(self):
        return self.settings.get(self._prestation_path)


def {{cookiecutter.extension_name}}_launcher(*args):
    """
    Launcher for creating a MissionBal2Word document.
    """
    print('launcher called')
    env = Environ()
    msgbox(env.URL)



g_exportedScripts = {{cookiecutter.extension_name}}_launcher
