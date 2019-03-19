Creating an OOo Extension with Options Dialog in less 5 than minutes'
===================================================================

## Features
Create a starter boilerplate for an OOo extension including options dialog in 
less than 5 minutes.

Powered by [Cookiecutter](https://github.com/audreyr/cookiecutter).

Specification can be found at: https://wiki.openoffice.org/wiki/Documentation/DevGuide/Extensions/Options_Dialog

## Usage
Let's pretend you want to create an extension including options feature called 
"fantastic_extension". Rather than copying an old project and then editing it 
to include your numerous settings among which some of them are always get 
forgotten until the worst possible moment, get cookiecutter_ to do all the work.

First, get Cookiecutter. Trust me, it's awesome:

    $ pip install "cookiecutter>=1.4.0"

Now run it against this repo::

    $ cookiecutter git@github.com:bastien34/cookiecutter_ooo_extension.git

You'll be prompted for some values. Provide them, then a base project will be 
created for you.

**Replay project generation** without being prompted on the command line:

    $ cookiecutter --replay git@github.com:bastien34/cookiecutter_ooo_extension.git

## TODO'S

### Create boilerplate from ODT File
We should create the base extension from  a `.odt` file instead of a `.json`. This
document could have a table for Toolbar and Menubar menu, for variables that 
would need an Options Dialog.

**General Vars**

|Keys               | Default values                |
| ---               | ---                           |
|extension_name     | my_extension                  |
|extension_label    | My extension                  |
|extension_version  | 0.0.1                         |
|package_name       | com.mycompany.myextension     |
|leaves             | com.mycompany.myextension     |
|leaf_id            | leaf_1       |
|leaf_label         | Leaf 1       |
|node               | node1        |
|company_name       | Your Company        |
|author_name        | You Name                |
|author_email       | your_mail@provider.com       |
|update_url         | pointing to your update.xml file       |
|release_note_url   | pointing to your release note       |
|publisher_url      | https://yourwebsite.com             |
|image_name         | logo.png                 |



**MenuBar and ToolBar**

| Function name | Function label|Module |Icon |
| ------------- |:--------------:| :-----:| ---: |
| extension_launcher |My Extension   | my_extension.py |extension_icon.jpg |
| feature2_launcher      | Feature 2 | my_extension.py |feature2_icon.jpg|
| etc. | ...      | ...    |... |


**Variables That needs a Dialog Box**

| Var name | Var label | Type |
| ------------- |:-------------:| -----:| 
| test_mode |Test mode   | boolean |
| token      | Token | string |
| url      | Url | string |



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

- Leaves: (com.rdt.com.Bal)

- name id of the leaf (com.rdt.comp.Bal)

### Filenames
You'll find a complete file description here : 
https://wiki.openoffice.org/wiki/Documentation/DevGuide/Extensions/File_Format

#### Options Dialog Window
This `.xdl` file contains the description of the graphic Windows. We build it 
using the LibO dialog editor.

The size of the windows should be something like width: 290, height: 215.

It may not have the “OK”, “CANCEL”, “HELP” or “Back” buttons. These buttons are 
already part of OOo's options dialog and the options dialog created by the 
Extension Manager.

The URL of this file must be included in the `.xcu` file (which is automatically
done by our tool).

Location: `dialogs/{{cookiecutter.extension_name}}_dialog.xdl`

#### manifest.xml
An extension needs to provide configuration data (xcu files) in order to define 
modules, nodes and leaves. These files can be anywhere in the extension, except 
in META-INF, and there must be an appropriate entry in the manifest-xml.

Location: `META-INF/manifest.xml`

#### Config file: `{{cookiecutter.extension_name}}_config.xcs`
The configuration Schema file gives important information on your vars. For this
first version, I let personal stuff. It's up to you to adapt it manually to
your needs.

Important var here is `oor:package="{{cookiecutter.package_name}}`

Location: `config/{{cookiecutter.extension_name}}_config.xcs`


#### Config file: `{{cookiecutter.extension_name}}_dialog.xcu`
The configuration data file gives location for executables, for the dialog box. 

Important vars here are:

- Nodes name: defined as: {{cookiecutter.package_name}}.{{cookiecutter.node}}. 
(e.g.: `com.mycompany.myextension.node1`)

- Nodes label: defined as: {{cookiecutter.extension_label}} (e.g.: `My Extension`)

- Leaves name: {{cookiecutter.leaves}} We need to understand why a plural form 
here. Try to add more than one leaf. For now, we consider it more as a single "leaf".

- Leaves id: {{cookiecutter.leaf_id}} (See Identifier section before)

- EventHandler Service: `{{cookiecutter.package_name}}.service`

Location: `config/{{cookiecutter.extension_name}}_dialog.xcu`


#### Config file: `{{cookiecutter.extension_name}}_options.component`
This file gives the dialog handler location (seen before) and the implementation 
name.

- Implementation name: `{{cookiecutter.package_name}}.IM` 

- Event handler Service name: see `.xcu` config file

Location: `config/{{cookiecutter.extension_name}}_options.component`

#### Dialog handler File: launcher of the options feature
This file uses the already configured implementation name and event handler
service name as defined above.

Location: `python/{{cookiecutter.extension_name}}_dialog_handler.py`


#### {{cookiecutter.extension_name}}.py
The file where you'll create your fantastic code. For now, we let here a
Environ class that handle all var.

Location: `python/{{cookiecutter.extension_name}}.py`


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

Location: `description.xml`


#### AddonUI.xcu
File that contains every think to create toolbars and menubars. 

For now it links to 


#### Other vars
- Project name: It can be your extension name. Should be short, no blank space, 
as it'll be used to create filename.

Using `{{cookiecutter.extension_name}}` in filename is a nice idea to keep thinks 
distinct and well organized. If you have many extension, each one with a 
config.xcu, it could be difficult to identify which project it belongs to.

- {{cookiecutter.leaf_1}} line 48 in _config.xcs instead of {{cookiecutter.extension_name}}


## Localization: `messages.po` file using 'xgettext'

`find . -name "*.py" > potfiles`

`xgettext -n --files-from potfiles -d python/pythonpath/locales/messages `

Then you can delete the 'potfiles'.
