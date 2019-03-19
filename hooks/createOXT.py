#!/usr/bin/env python
# -*- coding: utf-8 -*-



import subprocess
import glob
import os
import shutil
import sys
# from itertools import chain


def createOXT():

    current_path = os.path.dirname(os.path.abspath(__file__))
    oxtf = os.path.join(current_path, "..", "oxt")

    if not os.path.exists(oxtf):
        os.mkdir(oxtf)

    oxt = os.path.join(oxtf, "{{cookiecutter.extension_name}}-{{cookiecutter.extension_version}}.oxt")

    os.chdir(current_path)

    if not shutil.which("zip"):
        print("The zip command must be valid for execution.", file=sys.stderr)
        sys.exit()
    mani = [os.path.join("META-INF", "manifest.xml")]
    rdbs = glob.glob("*.rdb")
    comps = glob.glob("*.components")
    pys = glob.glob("*.py")
    xcus = glob.glob("*.xc?")
    icons = glob.glob(os.path.join("icons", "*.png"))
    dialogs = glob.glob(os.path.join("dialogs", "**", "*.*"),
                        recursive=True)
    descriptions = ["description.xml", *glob.glob(
        "{}*".format(c["ini"]["description.xml"]["license-text-en"])),
                    *glob.glob(os.path.join("descriptions",
                                            "*.txt"))]
    lst_files = []
    for lst in mani, rdbs, comps, pys, xcus, icons, dialogs, descriptions:
        if lst:
            lst_files.extend(lst)
    args = ["zip", oxt]
    args.extend(lst_files)
    subprocess.run(args)
    if os.path.exists("pythonpath"):
        exts = "py", "mo"
        lst_files = []
        for ext in exts:
            g = glob.glob(os.path.join("pythonpath", "**", "*.{}".format(ext)),
                          recursive=True)
            if g: lst_files.extend(g)
        if lst_files:
            args = ["zip", "-u", oxt]
            args.extend(lst_files)
            subprocess.run(args)


if __name__ == "__main__":
    createOXT()
