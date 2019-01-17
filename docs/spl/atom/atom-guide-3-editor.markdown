---
layout: docs
title:  Useful editing features
description:  Steps to configure Atom for SPL development
navlevel: 2
tag: atom
prev:
  file: atom-guide-2-import
  title: Import your code into Atom
next:
  file: atom-guide-4-build
  title: Build and run an application
---



Atom Overview
-------------

Even if you are familiar with SPL, you'll still want to review this
section as it covers some of the SPL features in Atom.

**The Project Pane**

![](media/image17.png){width="5.63907261592301in"
height="2.4532370953630798in"}

This pane shows the projects you are currently working on. You can have
multiple projects open at any time. Use the Add Project Folder option
from the File menu to import a project.

**The Command Palette**

Open the command palette (CMD + SHIFT + P) on a mac to see all the
available commands. If you are ever unsure of how to do something,
search the command palette to see if it is available.

**Version Control with Git**

From the command palette, you can search for *Git or Github tab* and you
will be able to open or close these tabs. While the Git tab manages
changes in your local repository, the GitHub tab helps you with projects
hosted on GitHub.

You can also open the Github and Git tabs from the bottom right of the
editor:

![](media/image17.png){width="5.63907261592301in"
height="2.4532370953630798in"}

From the Git tab, you can view, stage and commit changes you've made to
your project:

![](media/image18.png){width="4.442667322834645in"
height="1.8482633420822396in"}

Folders and files that have been changed are also colored differently in
the **Project** pane. For example, in the screenshot above, the
QuickStart folder and README.md file have both been changed.

See the Atom Flight Manual's section on Git to learn more about the Git
support in Atom.

<https://flight-manual.atom.io/using-atom/sections/github-package/>

SPL Editing Features
--------------------

The editor has rich code completion and content assist features.

For example, open sample/Main.spl from the BusAlerts project.

Line 7 contains the line *composite BusAlerts\_Main.*

A composite defines either a Streams application or an operator. We will
discuss operators later. In this case, the composite *BusAlerts\_Main*
is the application's entry point, similar to the class containing the
main method in a Java or C++ application.

As is typical of applications, a main composite can be supplied
parameters using a ***param*** clause (line 8).

Let's use this application to explore some Atom features

![](media/image19.png){width="4.152083333333334in"
height="2.3222222222222224in"}

**Bracket matching** allows you to see the scope of a declaration:

**Code Folding**

If the closing bracket isn't easily visible, Atom allows you to fold
portions of code, as shown below:

> ![](media/image20.gif){width="2.4797462817147857in"
> height="2.6047922134733157in"}
>
> Anywhere a downwards caret
> ![](media/image21.png){width="0.17692257217847768in"
> height="0.1432108486439195in"} occurs, you can collapse the code to
> make it easier to read.

After defining any needed parameters, a composite must always start with
a *graph* clause (line 11).

Everything after the *graph* clause represents the application itself,
which is composed of one or more operators.

The first operator in the application is a FileSource operator called
BusDataFromFile:

![](media/image22.png){width="4.145262467191601in"
height="1.0918635170603674in"}

The kind of the operator is a FileSource, but to differentiate between
invocations of operators of the same kind, each instance of the operator
is called by the name of the output stream. Thus, we refer to this
invocation of FileSource as the BusDataFromFile operator.

**View an operator's documentation **

Hover over the operator name to see its documentation:

> ![](media/image23.png){width="3.887619203849519in"
> height="1.534828302712161in"}

Now that we know the job of a FileSource operator is to read data from a
file, the next few lines can be understood:

-   The **param** clause again specifies parameters, but this time for
    the operator.

    -   The file parameter specifies the name of the file.

    -   Hover over the initDelay parameter to see what it does.

You can hover over any artifacts, such as parameters, streams,
operators, and its documentation will be displayed, if it is available.

**Find References within a File**

As we saw above, the BusDataFromFile operator produces a stream of
tuples representing the data that was in the file.

To find out how the BusDataFromFile output stream is used in this
application, click on it to highlight occurrences:

> ![](media/image24.png){width="3.36709208223972in"
> height="1.405236220472441in"}
>
> References to that stream are highlighted in grey.

**Find All References Within a Project**

Continuing the example above, the BusDataFromFile stream is used by the
ParseNextBusData operator. We can find where this operator is defined by
clicking on it, and choosing **Find References** from the context menu.

![](media/image25.png){width="3.231788057742782in"
height="2.415209973753281in"}

This will show all mentions of this operator, including its definition
in another file:

![](media/image26.png){width="3.7406277340332457in"
height="1.8133497375328085in"}

In the **Symbol References pane,** you can click on a result to go to
the corresponding file.

**Note:** The **Go to Declaration** menu item is unsupported due to a
limitation in Atom.

**Finding problems**

The bottom left corner of the editor will show how many syntax errors
are in your code:

![](media/image27.png){width="1.5894039807524059in"
height="2.7696030183727034in"}**\
\
**Yay, no errors! But if there were, you could click the error icon and
it would open the Diagnostics pane to help you find and fix the errors.

You can also open all files with errors at once by typing "diagnostics
errors" from the Command Palette:

![](media/image28.png){width="3.388548775153106in"
height="1.039734251968504in"}

**Code Completion**

The editor also supports code completion to speed up development. As you
type, you can hit CTRL+SPACE to bring up a list of suggestions:

![](media/image29.png){width="2.8862423447069117in"
height="1.9336876640419947in"}

The screenshot above shows the list of parameters available for the
FileSource operator.

**Operator Templates **

In addition to suggesting word completions, there is also support for
adding code blocks based on templates. Imagine that instead of reading a
local file, we wanted to read the contents of a file stored in a Hadoop
server on the IBM Analytics Engine. Instead of the FileSource operator,
we'd use the HDFS2FileSource operator to read data from Hadoop,.

To add a new HDFS2FileSource operator to our graph, hit CTRL + SPACE on
an empty line and search the available operator templates for *hdfs*:

![](media/image30.png){width="5.38628937007874in"
height="1.2170942694663167in"}

A template exists, so use the down arrows to select *HDFS2FileSource for
IBM Analytics Engine* and hit enter:

![](media/image31.png){width="3.064390857392826in"
height="1.0190879265091863in"}

The template for the operator is added to the file, so you would only
have to change the operator's parameters, stream type, and output type
to suit your needs.

Remember:

CTRL + SPACE shows code completion suggestions at any time.

ESC dismisses the suggestions that appear.

### Atom Documentation

Additional Information about Atom is available in the documentation:

Atom Basics:
<https://flight-manual.atom.io/getting-started/sections/atom-basics/>

Using Atom: https://flight-manual.atom.io/using-atom/
