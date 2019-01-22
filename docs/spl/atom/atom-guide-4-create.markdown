---
layout: docs
title:  Creating a new SPL application
description:  How to create a new project from scratch
navlevel: 2
tag: atom
prev:
  file: atom-guide-3-editor
  title: Reviewing SPL code in Atom
next:
  file: atom-guide-5-build
  title: Build an run an application in Atom
---

The general steps to create a new project are:
- Create an empty folder on your filesystem and import it into Atom
- Create a toolkit information file

Once you create your project, you can start creating applications. The main entry point of any SPL application is called a _Main Composite_. So after creating your project, you can create your first Main composite by:

- Defining a namespace to organize your code (optional, but recommended)
- Create a Main composite within a SPL file


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

Create a Main composite
--------------------------

Main composites are defined in SPL source files. These files have a `.spl` extension.

**Create a source file within a namespace**:

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
Now that you have created a project, let us walk through the creation of the BusAlerts application.


What will the application do?
=============================
Recall that this application will display alerts and advertisements within the city's public transit vehicles as they move around the city. The buses periodically report their location. When a bus is near an area with an alert, the application will detect this and send the alert.

We're going to develop the application in 3 steps:
![application phases](/streamsx.documentation/images/atom/jpg/phases2.jpg)

When developing Streams applications, it is helpful to **break down the application into individual tasks, and then find one or more operators to perform each task.**


Use operators to process data in steps
--------------------------------------

Remember that an **operator** is building block of a Streams application. It performs a specific task with an **input stream** of data and then produces an **output stream** which is the result of the processing. So our  application will  be made up of different operators that perform each of the above 3 tasks.


**Create the Main Composite**

If you haven't already, create a new main composite for your application. See above for instructions.

Step 1: Ingest data
====================

All Streams applications start with ingesting the data that will be analyzed.

In our case, the data we are processing is the location of each bus as it is reported. Each record is a XML string that describes the bus and
it's latitude, longitude, current speed, end so on:
```
<vehicle id="5764" routeTag="24" dirTag="24\_\_\_I\_F00"
 lat="37.734356" lon="-122.390739" secsSinceReport="9"
 predictable="true" heading="218" speedKmHr="0"\>

```
We’ll use a `FileSource` operator to read the data from the file :



```
	stream<xml locationXMLDoc> NextBusData_FromFile = FileSource()
	{
		param
			file : getApplicationDir() + "/data/saved_BusLocations.txt" ;
			initDelay : 30.0 ;
	}

```
