---
layout: docs
title:  Adding toolkits to your application
description:  Steps to add toolkits to the editor
navlevel: 2
tag: atom
prev:
  file: atom-guide-4-build
  title: Build and run an application
next:
  file: atom-guide-6-problems
  title: Troubleshooting
---



While Streams applications can be written in Java and Python, this guide
is going to focus on developing applications using Streams Processing
Language (SPL).

Import the sample project for this guide
-----------------------------------------

To follow along with this guide, download the BusAlerts application
archive. Unpack it into a folder and import it into Atom: **File** \>
**Add Project Folder** and browse to the project folder.

The following sections describe other ways to start development --
importing your own code from a file or GitHub, or creating a new
project.

Import an existing project
--------------------------

The same steps above apply to import any SPL project for use in Atom.
**File** -\> **Add Project Folder** and browse to the project folder.

Import A Project From GitHub
----------------------------

-   If you have existing SPL code on Github**,** you can clone the
    repository from within Atom:\
    From the Command Palette ( CMD + shift + p on Mac), type Github
    Clone:

> ![](media/image6.png){width="4.084616141732283in"
> height="2.577128171478565in"}

-   Then paste the repository URL and click Clone.

> ![](media/image7.png){width="4.211873359580053in"
> height="1.3076924759405075in"}

Creating a new project
----------------------

-   Create an empty folder on your filesystem, e.g. MyStreamsProject

-   From Atom, go to File \> Add Project Folder and select the project
    folder.

### Create a toolkit information file

-   Create a file within the folder called info.xml. Right-click the
    MyStreamsProject folder, select "New File", and enter info.xml as
    the file name:

    ![](media/image8.png){width="3.707043963254593in"
    height="0.6178412073490813in"}

    This file is called the toolkit information file. SPL projects are
    also called toolkits, and this file describes the application you're
    going to create, as well as lists any additional
    applications/toolkits it depends on.

    Copy the contents of sampleinfo.xml \[LINK\] to get you started.

    ![](media/image9.png){width="4.484615048118985in"
    height="3.406919291338583in"}

    *Sample info.xml file*

    Learn more about the information file here:
    <https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.dev.doc/doc/toolkitinformationmodelfile.html>

Create a namespace
------------------

Namespaces allow you to organize your SPL code, similar to Python
modules or Java packages.

-   Create a folder within your project with the target namespace:\
    Select the project, right click, and click *New Folder. *

    -   Enter a name for the namespace, e.g. "my.name.space":\
        ![](media/image10.png){width="4.019099956255468in"
        height="1.0069444444444444in"}

    -   Create a new file within the my.test.namespace folder, call it
        ".namespace".

        ![](media/image11.png){width="5.053846237970253in"
        height="1.046405293088364in"}

    -   The final folder structure should look like this:

        ![](media/image12.png){width="2.2918799212598424in"
        height="1.5437040682414698in"}

Now that your namespace is created, you can create your first SPL file.

Create a Main composite
-----------------------

-   Select the "my.name.space" folder, right click \> "New File"

-   Enter the name for the new SPL file, Main.spl.

-   Add the namespace declaration to the file adding the following line
    to Main.spl:\
    namespace my.name.space;

    composite MyApp {

    }

-   The final code should appear like this:

    ![](media/image13.png){width="4.330768810148731in"
    height="1.529650043744532in"}

Now you are ready to start development. If you are brand new to Streams
please continue the sections Basic Building Blocks, SPL Basics, and
Simple Streams Application in the Quick Start Guide.

Whether you imported an existing application or are creating one from
scratch, it is a good idea to explore the Atom editor to learn about
useful editing features.

![](media/image14.png){width="4.741064085739283in"
height="2.523179133858268in"}

Get familiar with the Editor
