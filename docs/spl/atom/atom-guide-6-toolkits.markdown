---
layout: docs
title:  Adding toolkits to your application
description:  Steps to add toolkits to the editor
navlevel: 2
tag: atom
prev:
  file: atom-guide-5-build
  title: Create a new SPL project in Atom
next:
  file: atom-guide-7-problems
  title: Troubleshooting
---

All SPL projects, including the ones you create, are called toolkits.
The Streams platform includes many toolkits, each with useful operators and functions.
For example, the operators used to connect to Kafka are all in the Kafka
toolkit.

Almost all Streams applications you create will use one or more external toolkits.

This section will show you where to get them and how to add one to your application.

Find a toolkit
---------------------------------------------

If you are looking for a toolkit for a specific purpose:
-  Check the list of [toolkits available on the Streaming Analytics service](https://cloud.ibm.com/docs/services/StreamingAnalytics/compatible_toolkits.html#compatible_toolkits)

- Search [the Streams GitHub project](https://github.com/IBMStreams) for other toolkits that are not included in the Streams platform. From the project page, you can search for a toolkit by keyword.



3 steps to add a toolkit
----------

To use a toolkit you add it to your application by:

1.  Downloading the toolkit and placing it in your toolkit directory, (optional)

2.  Adding an entry for that toolkit to your project's `info.xml` file

3.  Importing the toolkit with a `use` directive in your SPL source code.


You will need to complete step 1 if:

- You want to use an updated version of one of the [supported toolkits](https://cloud.ibm.com/docs/services/StreamingAnalytics/compatible_toolkits.html#compatible_toolkits\), or

- The toolkit in question was downloaded from GitHub or is a 3rd party toolkit.



Adding a toolkit: example
------------------------

Our sample application uses input XML data that was saved in a file. We want to change it to use live data. It will retrieve bus locations from the [NextBus service](https://nextbus.com)

Instead of reading from a file using a `FileSource` operator, we now need to use the `HTTPGetXMLContent` operator from the [streamsx.inet toolkit](https://github.com/IBMStreams/streamsx.inet) to connect to NextBus.

The toolkit is included in Streams but developed in the open on GitHub.  So we can download the latest version from Github.


Step 1: Download and unpack the toolkit
------

a.  Go to the [streamsx.inet toolkit page](https://github.com/IBMStreams/streamsx.inet/releases)

b.  Download version 3.0 or greater:
    streamsx.inet.toolkit-3.0.0-**el7-amd64**

![Download page](/streamsx.documentation/images/atom/jpg/downloadtoolkit.jpeg)

**Note**: If the toolkit you wish to use has multiple releases for different platforms, choose the **el7-amd64** release. This is the release that is compatible with the Streaming Analytics service.

c.  Place the toolkit in the toolkits directory you specified when you configured Atom.
    Recall that you specified this path in **ide-ibmstreams** package settings.

 ![toolkit directory](/streamsx.documentation/images/atom/jpg/toolkit-dir.jpg)

  When you copy a toolkit to the toolkit directory, make sure that there is a `toolkit.xml` file  present at the top level of the folder.

  As shown below, there are 2 toolkits, `com.ibm.streamsx.inet` and `com.ibm.streamsx.nlp`, and both have a `toolkit.xml` file.

  ![toolkit directory](/streamsx.documentation/images/atom/jpg/toolkits.jpeg)

Step 2: Add a dependency to the toolkit to your project:
----

d.  Open the `info.xml` of your project:

  If your project does not have an `info.xml` file, create one using the sample \[HERE\]

e.  Within the XML, add a dependency to the new toolkit under the `dependencies` node:

![new toolkit dependency](/streamsx.documentation/images/atom/jpg/infoxml.jpeg)

Here is a snippet for you to paste:

```

<info:toolkit>

  <common:name>com.ibm.streams.sometoolkit</common:name>

  <common:version>[min_ver,max_ver)</common:version>

</info:toolkit>
```


After saving the `info.xml` file, the `streamsx.inet` toolkit is ready for use in our application.

Step 3: Use the toolkit's operators in your SPL source
----------------

In your SPL source, import an operator or function from the toolkit you just added  with a `use` directive at the top of the file, right after the `namespace` declaration:

- Adding `use com.ibm.streamsx.sometoolkit.namespace::SomeOperator;` will import  `SomeOperator` from the toolkit,
Then you can invoke the operator:

  ```
    stream<int32 myint> Result = SomeOperator(){

    }
  ```

E.g. to use the `HTTPGetXMLContent` operator, add the line

`use com.ibm.streamsx.inet.http::HTTPGetXMLContent;`

to the top of `BusAlerts_Main.spl`.


Now we can use the operator in our code.
We're going to replace the  `NextBusData_FromFile` stream  with a `HTTPGetXMLContext` operator:


1.  Highlight the operator's definition and then click **Edit > Toggle Comment:**
    ![toggle comment](/streamsx.documentation/images/atom/jpg/comment.jpeg)

3.  Paste the following snippet in the editor:

      ```
      stream<xml locationXMLDoc> RawData_Live = HTTPGetXMLContent()

        {

        param

        url : getUrl("vehicleLocations", $agency);

        period : 30.0; //poll every 30 seconds

        updateParameter: "t";

        updateParameterFromContent: "/body/lastTime/@time";

        }

    ```
4.  Change the `BusLocationStream` operator to use the `RawData_Live`
    stream instead of the `NextBusData_FromFile` stream:

    Change the line:

      ```
      stream <rstring id, float64 latitude, float64 longitude>
       ParsedDataStream = ParseNextBusData (NextBusData_FromFile )

      ```  
    to:

    ```
    stream
    <rstring id, float64 latitude, float64 longitude>
    ParsedDataStream  = ParseNextBusData(RawData_Live)

    ```

We've now replaced the operator that was reading from a file with one that will connect directly to NextBus. Try it out by building and launching the application.


Since the data is live, before you can see output you might need to wait a minute or 2 for the application to connect to NextBus before checking the Log Viewer.

Adding a toolkit: summary
-------------------------

1.  Toolkits must be built, meaning that the top level of the toolkit must have a `toolkit.xml` file.

      a. If you are downloading a toolkit from GitHub, a built version of the toolkit is available from the releases page of the GitHub project. If there are releases for different operating systems, choose the EL7-AMD64 release.

      b. If no release exists, or if the downloaded release does not include a `toolkit.xml` file, see the toolkit's page for instructions on building it.

2.  Put the toolkit folder into the toolkit directory you created during the initial setup.
    Recall that you specified this path in  **the ide-ibmstreams** package settings.

3.  If it does not already have one, create a toolkit information file, called `info.xml`  for your project. Download a sample here: \[LINK\].

4.  Edit the `info.xml` file to add a dependency to the toolkit you need:

    The following is an example of a project with 2 dependencies:  `com.ibm.streamsx.sometoolkit` and `com.ibm.streams.geospatial`:

    ```
    <info:dependencies>
        <info:toolkit>
          <common:name>com.ibm.streamsx.sometoolkit</common:name>
          <common:version>[1.0.0,3.0.0)</common:version>
        </info:toolkit>
        <info:toolkit>
          <common:name>com.ibm.streams.geospatial</common:name>
          <common:version>[1.0.0,3.0.0)</common:version>
        </info:toolkit>
      </info:dependencies>
      ```

5.  Add a *use* directive in your SPL code to import operators from the toolkit:

    - Adding `use com.ibm.streamsx.sometoolkit.namespace::SomeOperator;` will import  `SomeOperator` from the toolkit,
    Then you can invoke the operator:

      ```
        stream<int32 myint> Result = SomeOperator(){

        }
      ```

    - Adding `use com.ibm.streamsx.sometoolkit.namespace::*;` will import all operators and functions in that namespace.
