---
layout: docs
title:  Reviewing SPL code in Atom
description:  Features in  Atom to make SPL development easier.
navlevel: 2
tag: atom
prev:
  file: atom-guide-2-import-code
  title: Import your code into Atom
next:
  file: atom-guide-4-create
  title: Creating a new SPL project
---

This section covers some of the SPL features in Atom.

Atom overview
-----------------------------------------

Here is an look of the Atom editor showing some important features:

![editor overview](/streamsx.documentation/images/atom/jpg/atom-1.jpg)

* The **Project** pane shows the projects you are currently working on. Use **File \> Add Project Folder** to import a project.



The Command Palette
--------------------

Open the command palette (`CMD + SHIFT + P` on a Mac) to see all the
available commands.

![cmd palette](/streamsx.documentation/images/atom/jpg/cmd-palette.jpg)

If you looking for a pane or view or an action, search the command palette to find it.

For example, you can open the Github tabs from the command palette. Search for *Git or Github tab*.

Version control with Git
-------------------------

The **Git** tab manages changes in your local repository and the **GitHub** tab helps you with projects hosted on GitHub. Open/close these tabs from the bottom right of the editor or the command palette.

![open git tab](/streamsx.documentation/images/atom/jpg/github-open.jpg)

Folders and files that have been changed are also highlighted in the
**Project** pane. For example, in the screenshot above, the `SensorMonitor.spl` file has been changed (yellow) and the `output` folder has been added (green).

See the [Atom Flight Manual section on Git](https://flight-manual.atom.io/using-atom/sections/github-package/) to learn more about the Git support in Atom.


SPL Editing Features
--------------------

The editor has rich code completion and content assist features.

For example, open `sample/Main.spl` from the `BusAlerts` project.

Line 7 contains the line `composite BusAlerts\Main`.

This is the *main composite* of this application. It is the application's entry point.

Let's use this application to explore some Atom features.

#### Bracket matching
Shows you the scope of a declaration:

![bracket-match](/streamsx.documentation/images/atom/jpg/brackets.jpg)


#### Code Folding

If the closing bracket isn't easily visible, collapse portions of code, as shown below:

<figure>
  <img src="/streamsx.documentation/images/atom/jpg/fold.gif" alt="code folding"/>
  <figcaption>Collapsing the composite shows the other functions defined in the SPL file.
  </figcaption>
</figure>

Anywhere a downwards caret ![caret](/streamsx.documentation/images/atom/jpg/caret.jpeg) occurs, use it to collapse the code to make it easier to read.

View an operator's documentation
--------------------------------
You can hover over any artifact, such as a parameter, stream, or operator, and its documentation will be displayed, if it is available.

For example, the first operator in the application is a `FileSource` operator. Hover over the operator to see its documentation:

![fsrc-doc](/streamsx.documentation/images/atom/jpg/hover.gif)

This operator reads data from a file and produces a stream of tuples representing the data that was in the file.

The **param** clause is a list of named parameters of the operator, such as the `file` parameter which specifies the name of the file.

Hover over the `initDelay` parameter to see what it does.

Find References within a File
------------------------------
To find out where a stream or operator is used within a file, you can click on it to highlight occurrences.

For example, a stream called `BusDataFromFile` is the output of the `FileSource` above.
Click on the `BusDataFromFile` stream to highlight occurrences:

![found occurences](/streamsx.documentation/images/atom/jpg/ocurrences.jpeg)

Find All References Within a Project
------------------------------------

Use **Find References** to find where an artifact is used within the whole project.

Continuing the example above, the `BusDataFromFile` stream is used by the `ParseNextBusData` operator.
To see where the `ParseNextBusData` operator is defined, right click and select **Find References** from the context menu.

![find refs](/streamsx.documentation/images/atom/jpg/refs.gif)

This will open the **Symbol References** pane, which lists all references of this operator, including its definition.
Click on a result in that pane to go to the corresponding file.

**Note:** The **Go to Declaration** menu item is unsupported due to a
limitation in Atom.

Code completion
-----------------

The editor also supports code completion. As you type, you can hit `CTRL+SPACE` to bring up a list of suggestions:

![Content assist](/streamsx.documentation/images/atom/jpg/contentassist.gif)

The screenshot above shows the list of parameters available for the `FileSource` operator.

Operator Templates
---------------------

You can also add operators using templates.

Imagine that instead of the FileSource operator, we wanted to use the
HDFS2FileSource operator to read data from Hadoop.

To add a new HDFS2FileSource operator to our graph, type `CTRL + SPACE` on an empty line and search the available operator templates for *hdfs*:

![operator template content assist](/streamsx.documentation/images/atom/jpg/template.gif)

A template exists, so use the down arrows to select *HDFS2FileSource for IBM Analytics Engine* and hit enter:
The template for the operator is added to the file. Change the operator's parameters, stream type, and output type to suit your needs.


Finding problems
---------------------

The bottom left corner of the editor will show any compilation or syntax errors in your code:

![errors list](/streamsx.documentation/images/atom/jpg/error-list.jpg)

Click the error icon to open the **Diagnostics** pane to help you find and fix the errors.

![errors pane](/streamsx.documentation/images/atom/jpg/errors.jpeg)

You can also open all files with errors at once by typing "diagnostics errors" from the Command Palette:

![Open all errors](/streamsx.documentation/images/atom/jpg/open-all-errors.jpeg)


Summary
---------

*  Open the command palette to access all panes and actions in Atom.
* `CTRL + SPACE` shows code completion suggestions at any time.
* `ESC` dismisses the suggestions that appear.

Atom Documentation
----------------------

Additional Information about Atom is available in the documentation:

* [Atom Basics](https://flight-manual.atom.io/getting-started/sections/atom-basics/)
* [Using Atom](https://flight-manual.atom.io/using-atom/)
