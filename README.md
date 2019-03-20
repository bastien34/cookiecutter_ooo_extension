OOo Extension with Options Dialog in 1 minute only
==================================================

## Features
Create a starter boilerplate for an OOo extension including options dialog in 
1 minute.

Powered by [Cookiecutter](https://github.com/audreyr/cookiecutter).

Options dialog Specification can be found at: https://wiki.openoffice.org/wiki/Documentation/DevGuide/Extensions/Options_Dialog

## Usage
Let's pretend you want to create an extension including options feature called 
"fantastic_extension". Rather than copying an old project and then editing it 
to include your numerous settings among which some of them are always get 
forgotten until the worst possible moment, get cookiecutter_ to do all the work.

First, get Cookiecutter. Trust me, it's awesome!

    $ pip install "cookiecutter>=1.4.0"

Now run it against this repo:

    $ cookiecutter git@github.com:bastien34/cookiecutter_ooo_extension.git

You'll be prompted for some values. Provide them, then a base project will be 
created for you. You can **replay the project generation** without being prompted 
on the command line. Use the `--replay` option:

    $ cookiecutter --replay git@github.com:bastien34/cookiecutter_ooo_extension.git

**Warning!** Depending on your OOo version, installing by double clicking on the
extension file can bug. Install it from the extension manager!

### General Vars
|Keys               | Default values                      | Note         |
| ---               | ---                                 |---              |
|extension_name     | my_extension                        |No blank space
|extension_label    | My extension                        |Displayed in menu
|extension_version  | 0.0.1                               |
|package_name       | com.mycompany.myextension           |Identifier, see below the schema to assure uniqueness
|leaf_label         | Settings                            |Displayed as node's leaf
|leaf_id            | settings                            |Unique ID for your leaf
|node               | node1                               |Let it as it is
|company_name       | Your Company                        |
|author_name        | Your Name                           |
|author_email       | your_mail@provider.com              |
|update_url         | pointing to your update.xml file    |URL
|release_note_url   | pointing to your release note       |URL
|publisher_url      | https://yourwebsite.com             |URL
|image_name         | logo.png                            |PNG or JPG, 42x42 pixels


## What you gonna have
The result will be 2 dirs. 

First one named "your_extension" contains the project source.  You'll start 
writing your code in it.

The second dir `oxt` contains the extension, that you can test and install.

For now, as an example, we let options dialog for few settings (url, token,
path), a Menubar and a Toolbar linked to a launcher that open a simple message 
box.

That's it. Stupid and simple !

#### Treeview of the project source

```
├── {{cookiecutter.extension_name}}
│   ├── AddonUI.xcu
│   ├── config
│   │   ├── {{cookiecutter.extension_name}}_config.xcs
│   │   ├── {{cookiecutter.extension_name}}_dialog.xcu
│   │   └── {{cookiecutter.extension_name}}_options.components
│   ├── Descriptions
│   │   ├── descr-en.txt
│   │   ├── descr-fr-FR.txt
│   │   └── descr-fr.txt
│   ├── description.xml
│   ├── dialogs
│   │   └── {{cookiecutter.extension_name}}_dialog.xdl
│   ├── icons
│   │   ├── bal_16.png
│   │   └── excel_16.png
│   ├── images
│   │   └── logo.png
│   ├── META-INF
│   │   └── manifest.xml
│   ├── python
│   │   ├── {{cookiecutter.extension_name}}_dialog_handler.py
│   │   ├── {{cookiecutter.extension_name}}.py
│   │   └── pythonpath
│   │       ├── {{cookiecutter.extension_name}}
│   │       │   └── options_dialog.py
│   │       ├── {{cookiecutter.extension_name}}_utils.py
│   │       └── locales
│   │           └── fr_FR
│   │               └── LC_MESSAGES
│   │                   ├── messages.mo
│   │                   └── messages.po
│   └── WindowState
│       └── tbWriter.xcu
├── cookiecutter.json
├── hooks
│   ├── createOXT.py
│   ├── post_gen_project.py
│   └── pre_gen_project.py
├── LICENSE
└── README.md

```

### Filenames coding
You'll find a file description here: 
https://wiki.openoffice.org/wiki/Documentation/DevGuide/Extensions/File_Format

We use `{{cookiecutter.extension_name}}` in filename to keep thinks distinct and 
well organized. If you have many extension, each one with has a config.xcu, it 
might be difficult to find straight away which project it belongs to.


|Filename               | Note                      | Location         |
| ---               | ---                                 |---              |
|{{cookiecutter.extension_name}}_dialog.xdl     | Content of graphic Windows, build using the LibO dialog editor. (290x215 max)|`dialogs/{{cookiecutter.extension_name}}_dialog.xdl`
|manifest.xml    | Contains appropriate entry for modules, configuration data.      |`META-INF/manifest.xml`
|`{{cookiecutter.extension_name}}_config.xcs`    | Configuration schema of your vars.      |`config/{{cookiecutter.extension_name}}_config.xcs`
|`{{cookiecutter.extension_name}}_dialog.xcu`   | Configuration data file gives location for executables and dialog box.      |`config/{{cookiecutter.extension_name}}_dialog.xcu`
|`{{cookiecutter.extension_name}}_options.component`| Dialog handler location and implementation name | `config/{{cookiecutter.extension_name}}_options.component`
|`{{cookiecutter.extension_name}}_dialog_handler.py`{{cookiecutter.extension_name}}_options.component`| Dialog handler file | `python/{{cookiecutter.extension_name}}_dialog_handler.py`
|`{{cookiecutter.extension_name}}.py`| File where you'll start working on your code. Contains a simple launcher. | `python/{{cookiecutter.extension_name}}.py`
|`description.xml`| Description of your extension. See below. |  `description.xml`
|`AddonUI.xcu`| Toolbars and Menubar. |  `AddonUI.xcu`


#### Options Dialog Window
This `.xdl` file contains the description of the graphic Windows. We build it 
using the LibO dialog editor.

The size of the windows should be something like width: 290, height: 215.

It may not have the “OK”, “CANCEL”, “HELP” or “Back” buttons. These buttons are 
already part of OOo's options dialog and the options dialog created by the 
Extension Manager.


#### manifest.xml
An extension needs to provide configuration data (xcu files) in order to define 
modules, nodes and leaves. These files can be anywhere in the extension, except 
in META-INF, and there must be an appropriate entry in the manifest-xml.

#### Config file: `{{cookiecutter.extension_name}}_config.xcs`
The configuration Schema file gives important information on your vars. For this
first version, I let personal stuff. It's up to you to adapt it manually to
your needs.

Important var here is `oor:package="{{cookiecutter.package_name}}`

#### Config file: `{{cookiecutter.extension_name}}_dialog.xcu`
The configuration data file gives location for executables, for the dialog box. 

Contains:

- Nodes name: defined as: {{cookiecutter.package_name}}.{{cookiecutter.node}}. 
(e.g.: `com.mycompany.myextension.node1`)

- Nodes label: defined as: {{cookiecutter.extension_label}} (e.g.: `My Extension`)

- Leaves name: {{cookiecutter.package_name}} After multiple experiment, it seems 
that it is here the unique identifier as said above: "Every leaf has exactly one 
Options page and is assigned to exactly one Node and one Dialog".

- Leaves id: {{cookiecutter.package_name}} (See Identifier section before)

- EventHandler Service: `{{cookiecutter.package_name}}.service`


#### Config file: `{{cookiecutter.extension_name}}_options.component`
This file gives the dialog handler location (seen before) and the implementation 
name.

- Implementation name: `{{cookiecutter.package_name}}.IM` 

- Event handler Service name: see `.xcu` config file

#### Dialog handler File: launcher of the options feature
This file uses the already configured implementation name and event handler
service name as defined above.

#### {{cookiecutter.extension_name}}.py
The file where you'll create your fantastic code. For now, we let here a
Environ class that handle all var.

#### Description: description.xml
- Company name: Your company name `{{cookiecutter.company_name}}`

- Author name: your name `{{cookiecutter.author_name}}`

- Author email: your email `{{cookiecutter.author_email}}`

- Package name: `{{cookiecutter.package_name}}` as said, **reversed_domainname
.company.product.nodename.leafname.**
which can be `com.mycompany.myextension`

- Project version: `{{cookiecutter.extension_version}}` e.g.: "0.0.1"

- Image name: `{{cookiecutter.image_name}}` Images are in `images/` folder. 
42x42. eg: `my_image.jpg` JPG or PNG can be used.

- Update URL: `{{cookiecutter.update_url}}` 

- Publisher URL: your website

- Release note url. 


#### AddonUI.xcu
File that contains every think to create toolbars and Menubar. 


## Localization

Localization (`messages.po`) are located in `python/pythonpath/locales`.
 
We used 'xgettext' to generate our template as following:

`find . -name "*.py" > potfiles`

`xgettext -n --files-from potfiles -d python/pythonpath/locales/messages `

Then you can delete the 'potfiles'.


## TODO'S

### Create boilerplate from ODT File
Tris processe could start from a python macro embedded in a `.odt` file.

This file should contain more detailed values used to create a more complete project. 
First table would contain general vars (keys / values seen above). 

The second table would contain table for Toolbar and Menubar creation as following.

**MenuBar and ToolBar**

| Function name | Function label|Module |Icon |
| ------------- |:--------------:| :-----:| --- |
| extension_launcher |My Extension   | my_extension.py |extension_icon.jpg |
| feature2_launcher      | Feature 2 | my_extension.py |feature2_icon.jpg|
| etc. | ...      | ...    |... |

And of course, a table to generate the `.xcs ` file containing options we want
for our Options dialog.

**Variables that need a Dialog Box**

| Var name | Var label | Type | Default value
| ------------- |:-------------:|:-----:| :---:
| test_mode |Test mode   | boolean | true
| token      | Token | string | find a valid token
| url      | Url | string | https://my_webservice.com/

These tables would help generate these files:

- AddonUI.xcu (Menubar & Toolbar description)

- _config.xcs (vars in Options dialog)

It should be done before the extension generation. See `hooks/pre_gen_project.py`.
It's made for that.

You'll find a complete file description here : 
https://wiki.openoffice.org/wiki/Documentation/DevGuide/Extensions/File_Format


## Definitions from the specification document

#### Node 

In the spec, it seems that a name for a node might be: `“OpenOffice.org Writer”` 
which looks like a label. This has to be checked ! Using this node should place 
a leaf in this node.

#### Leaves

A leaf has a human readable, localized name. Every leaf has exactly one Options 
page and is assigned to exactly one Node and one Dialog. A leaf cannot have 
children. 

Leaves also have a unique identifier.

Leaves can be added to an existing Node or Nodes (unclear, we got it from specs).

#### Identifiers 

Modules, nodes, and leaves have an unique identifier. These are used as values 
for the oor:name attributes of a node element in the xcu file. Other identifiers 
are used as property values in the `.xcu` files. All these identifiers have to 
comply to the requirements for node names and value elements off the OOo registry.

To ensure uniqueness, we recommend to form the strings similar to this schema:

**reversed_domainname.company.product.nodename.leafname.**

For example:

`com.mycompany.myextension.mynode.leaf1`

For UTF8 identifier identity is element-by-element identity of the sequences of 
Unicode scalar values (no case folding, no normalization, etc.).
