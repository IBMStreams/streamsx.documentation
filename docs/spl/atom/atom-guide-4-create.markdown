---
layout: docs
title:  Creating a new SPL application
description:  How to create a new project from scratch
navlevel: 2
tag: atom
prev:
  file: atom-guide-3-editor
  title: Importing your code into Atom  
next:
  file: atom-guide-5-build
  title: Build an run an application in Atom
---

The general steps to create a new project are:
- Create an empty folder on your filesystem and import it into Atom
- Create a toolkit information file
- Create one or more namespaces to organize your code (optional, but recommended)

Create the project folder
---------------------------
Create an empty folder on your filesystem, e.g. `MyStreamsProject`

From Atom, go to **File** \> **Add Project Folder** and select the project folder.

Create a toolkit information file
---------------------------------

SPL projects are also called toolkits. Each toolkit folder must include a file called `info.xml`.  This file describes the toolkit and any other toolkits it depends on.

**This file must be in the top level of the project.**

Create a file within the folder called `info.xml`.
    - Right-click the `MyStreamsProject` folder, select **New File**, and enter `info.xml` as the file name:

![new tk info file](/streamsx.documentation/images/atom/jpg/info1.jpeg)

You can copy the contents of sampleinfo.xml \[LINK\] to get you started.

For your reference, below is an overview of the contents of what needs to be present in the file.
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
------------------------

Namespaces allow you to organize your SPL code, similar to Python
modules or Java packages. Any folder with an empty file called `.namespace` will be treated as a SPL namespace.

Create a folder within your project with the target namespace:
-   Select the project, right click, and click **New Folder**.

-   Enter a name for the namespace, e.g. `my.name.space`:
    ![sample info](/streamsx.documentation/images/atom/jpg/namespace1.jpeg)

-   Create a new file within the my.name.space folder, call it
    `.namespace`

    ![new namespace](/streamsx.documentation/images/atom/jpg/namespace2.jpeg)

-   The final folder structure should look like this:

    ![folder structure](/streamsx.documentation/images/atom/jpg/namespace3.jpeg)

Now that your namespace is created, you can create your first SPL source
file.

Create a SPL source file
--------------------------

The SPL source file is where you define the application you are creating. It is good practice to organize your source files within namespaces.

-   Select the `my.name.space` folder, right-click and choose **New File**.

-   Enter the name for the new SPL file, `Main.spl`.

-   Add the namespace declaration to the file with the following line:

    `namespace my.name.space;`

**Create a main composite**

Executable SPL applications are called main composites. Below is a stub
for a new executable composite:

```
composite BusAlerts {

}
```

The final code should appear like this:

![stub app](/streamsx.documentation/images/atom/jpg/blank-app.jpeg)

Develop a simple application
---------------------------

[TBD]
