---
layout: docs
title:  Useful Editor Features
description:  Features in  Atom to make SPL development easier.
navlevel: 2
tag: atom
prev:
  file: atom-guide-2-import-code
  title: Import your code into Atom
next:
  file: atom-guide-4-build
  title: Build and run an application
---

This section covers some of the SPL features in Atom.

Atom overview
-----------------------------------------

Here is an look of the Atom editor showing some important features:

![stub app](/streamsx.documentation/images/atom/jpg/atom-1.jpeg)

* The **Project** pane shows the projects you are currently working on. You can have multiple projects open at any time. Use **File \> Add Project Folder** to import a project.



The Command Palette
--------------------

Open the command palette (**CMD + SHIFT + P** on a Mac) to see all the
available commands.

![stub app](/streamsx.documentation/images/atom/jpg/cmd-palette.jpeg)

If you are ever unsure of how to do something,
search the command palette to see if it is available.

For example, you can open the Github tabs from the command palette. Search for *Git or Github tab*.

Version control with Git
-------------------------

The **Git** tab manages changes in your local repository and the **GitHub** tab helps you with projects hosted on GitHub. Open/close these tabs from the bottom right of the editor or the command palette.

![open git tab](/streamsx.documentation/images/atom/jpg/github-open.jpeg)

Folders and files that have been changed are also highlighted in the
**Project** pane. For example, in the screenshot above, the `SensorMonitor.spl` file has been changed (yellow) and the `output` folder has been added (green).

See the [Atom Flight Manual section on Git](https://flight-manual.atom.io/using-atom/sections/github-package/) to learn more about the Git support in Atom.


SPL Editing Features
--------------------

The editor has rich code completion and content assist features.

For example, open `sample/Main.spl` from the `BusAlerts` project.

Line 7 contains the line `composite BusAlerts\Main`

This is the *main composite* of this application. It is the
application's entry point.

Let's use this application to explore some Atom features.

#### Bracket matching
Shows you the scope of a declaration:

![bracket-match](/streamsx.documentation/images/atom/jpg/brackets.jpg)


#### Code Folding

If the closing bracket isn't easily visible, collapse portions of code, as shown below:

<figure>
  <img src="/streamsx.documentation/images/atom/jpg/fold.gif" alt="code folding"/>
  <figcaption>Collapsing the composite shows the other functions defined in the SPL file.</figcaption>
</figure>

Anywhere a downwards caret ![caret](/streamsx.documentation/images/atom/jpg/caret.jpeg) occurs, use it to collapse the code to
make it easier to read.

View an operator's documentation
--------------------------------
You can hover over any artifacts, such as parameters, streams,
operators, and its documentation will be displayed, if it is available.

For example, the first operator in the application is a `FileSource` operator. Hover over the operator to see its documentation:

![fsrc-doc](/streamsx.documentation/images/atom/jpg/filesource.jpeg)

This operator reads data from a file and produces a stream of tuples
representing the data that was in the file.

This helps us understand the next few lines:

The **param** clause is a list of named parameters of the operator, such
as the `file` parameter which specifies the name of the file.

Hover over the `initDelay` parameter to see what it does.

**Find References within a File**
To find out where a stream or operator is used within a file, you can click on it to highlight occurrences.

For example, a stream called
`BusDataFromFile` is the output of the `FileSource` above.
Click on the `BusDataFromFile` stream to highlight occurrences:

![found occurences](/streamsx.documentation/images/atom/jpg/ocurrences.jpeg)

**Find All References Within a Project**

Use **Find References** to find where an articact is used within the whole project.

Continuing the example above, the `BusDataFromFile` stream is used by the
`ParseNextBusData` operator.
To see where this operator is defined, right click and select **Find
References** from the context menu.

![find refs](/streamsx.documentation/images/atom/jpg/find-references.jpeg)

This will show all mentions of this operator, including its definition in the **Symbol References** pane:

![found refs](/streamsx.documentation/images/atom/jpg/found-references.jpeg)

Click on a result in that pane to go to the corresponding file.

**Note:** The **Go to Declaration** menu item is unsupported due to a
limitation in Atom.

Finding problems
---------------------

The bottom left corner of the editor will show how many syntax errors
are in your code:

![errors pane](/streamsx.documentation/images/atom/jpg/errors.jpeg)

Click the error icon to open the **Diagnostics** pane to help you find and fix the errors.

You can also open all files with errors at once by typing "diagnostics
errors" from the Command Palette:

![](media/image28.png){width="3.388548775153106in"
height="1.039734251968504in"}

**Code Completion**

The editor also supports code completion. As you type, you can hit
CTRL+SPACE to bring up a list of suggestions:

![](media/image29.png){width="2.8862423447069117in"
height="1.9336876640419947in"}

The screenshot above shows the list of parameters available for the
FileSource operator.

**Operator Templates **

You can also add operators using templates.

Imagine that instead of the FileSource operator, we wanted to use the
HDFS2FileSource operator to read data from Hadoop.

To add a new HDFS2FileSource operator to our graph, hit CTRL + SPACE on
an empty line and search the available operator templates for *hdfs*:

![](media/image30.png){width="5.38628937007874in"
height="1.2170942694663167in"}

A template exists, so use the down arrows to select *HDFS2FileSource for
IBM Analytics Engine* and hit enter:

![](media/image31.png){width="3.064390857392826in"
height="1.0190879265091863in"}

The template for the operator is added to the file. Change the
operator's parameters, stream type, and output type to suit your needs.

Remember:

CTRL + SPACE shows code completion suggestions at any time.

ESC dismisses the suggestions that appear.

### Atom Documentation

Additional Information about Atom is available in the documentation:

Atom Basics:
<https://flight-manual.atom.io/getting-started/sections/atom-basics/>

Using Atom: https://flight-manual.atom.io/using-atom/s
