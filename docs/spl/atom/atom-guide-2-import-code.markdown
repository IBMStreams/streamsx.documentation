---
layout: docs
title:  Import your code into Atom
description:  Steps to configure Atom for SPL development
navlevel: 2
tag: atom
prev:
  file: atom-guide-1-configure
  title: Configure Atom
next:
  file: atom-guide-3-editor
  title: Useful editing features
---

After configuring Atom, you can start working with some code.

To get the most out of this guide, it is a good idea to import the
sample application.

If you have your own code, you can also jump to the section that best
describes your use case:

-   Import an existing project (including Streams Studio projects)

-   Import a project from GitHub

-   Creating a new project in Atom


Import the sample project for this guide
-----------------------------------------

To follow along with this guide, download the BusAlerts application
archive. \[LINK\]

-   Unpack it into a folder

-   Import it into Atom: click **File** \> **Add Project Folder**.
    Browse to the project folder and click **Open.**

The following sections describe other ways to start development --
importing your own code from a file or GitHub, or creating a new
project.

Import an existing project
--------------------------

The same steps above apply to import any SPL project for use in Atom.

From Atom, click **File** -\> **Add Project Folder**. Browse to the
project folder, and click **Open.**

Import A Project From GitHub
----------------------------

If you have existing SPL code on Github**,** you can clone the
repository from within Atom:\
From the Command Palette (*CMD + Shift + P* on Mac), type *Github
Clone*:

> ![git clone](/streamsx.documentation/images/atom/jpg/githubclone.jpeg)

Then paste the repository URL and click **Clone**.

> ![git clone uri](/streamsx.documentation/images/atom/jpg/github-clone.-uri.jpeg)

The project should be added to the project pane.

Creating a new project
----------------------

To create a new project, create an empty folder on the filesystem, and import
it into Atom.

### Create the project folder

-   Create an empty folder on your filesystem, e.g. `MyStreamsProject`

-   From Atom, go to **File** \> **Add Project Folder** and select the
    project folder.

### Create a toolkit information file

SPL projects are also known as toolkits. Each toolkit must have a
toolkit information file, `info.xml`, that describes the project and any
other applications/toolkits it depends on.
**This file must be in the top level of the project.**

-   Create a file within the folder called `info.xml`. Right-click the
    `MyStreamsProject` folder, select **New File**, and enter `info.xml` as
    the file name:

    ![new information](/streamsx.documentation/images/atom/jpg/info1.jpeg)

    Copy the contents of sampleinfo.xml \[LINK\] to get you started.

    ![sample info]((/streamsx.documentation/images/atom/jpg/sample-info.jpeg)

    ```
<toolkitInfoModel
      xmlns="http://www.ibm.com/xmlns/prod/streams/spl/toolkitInfo"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema−instance"
      xmlns:cmn="http://www.ibm.com/xmlns/prod/streams/spl/common"
      xsi:schemaLocation="http://www.ibm.com/xmlns/prod/streams/spl/toolkitInfo toolkitInfoModel.xsd">
     <identity>
       <name>MyStreamsProject</name>
       <description>My first toolkit</description>
       <version>1.0.0</version>
       <requiredProductVersion>4.0.0</requiredProductVersion>
     </identity>

     <dependencies/>

       <sabFiles>
         <include path="data/**"/>
          <include path="etc/**"/>
       </sabFiles>
    </toolkitInfoModel>
```


Learn more about the [toolkit information file in the Knowledge Center](https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.dev.doc/doc/toolkitinformationmodelfile.html).

Create a namespace
------------------

Namespaces allow you to organize your SPL code, similar to Python
modules or Java packages.

-   Create a folder within your project with the target namespace:
    Select the project, right click, and click **New Folder**.

    -   Enter a name for the namespace, e.g. `my.name.space`:
        ![sample info]((/streamsx.documentation/images/atom/jpg/namespace1.jpeg)

    -   Create a new file within the my.name.space folder, call it
        `.namespace`

        ![sample info]((/streamsx.documentation/images/atom/jpg/namespace2.jpeg)

    -   The final folder structure should look like this:

        ![sample info]((/streamsx.documentation/images/atom/jpg/namespace3.jpeg)

Now that your namespace is created, you can create your first SPL source
file.

### Create a SPL source file

A project can have multiple namespaces, and each namespace can have
multiple SPL source files. The SPL source file is where you define the
application you are creating.

-   Select the `my.name.space` folder, right click \> `New File`

-   Enter the name for the new SPL file, `Main.spl`.

-   Add the namespace declaration to the file adding the following line
    to `Main.spl`:
    ```
namespace my.name.space;
```

### Create a main composite

Executable SPL applications are called main composites. Below is a stub
for a new executable composite:

```
composite MyApp {

}
```

-   The final code should appear like this:

![sample info]((/streamsx.documentation/images/atom/jpg/blank-app.jpeg)


Now you are ready to start development. If you would like some guidance
on how to create one please see the designing your streams application
section \[LINK\].

Whether you imported an existing application or are creating one from
scratch, it is a good idea to explore the Atom editor to learn about
useful editing features.
