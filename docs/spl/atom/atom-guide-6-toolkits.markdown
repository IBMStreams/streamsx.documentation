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
Streams includes many toolkits contain useful operators and functions.
For example, the operators used to connect to Kafka are all in the Kafka
toolkit.

Almost all Streams applications you create will take advantage of some
of the toolkits included in the Streams runtime. To use these toolkits
you must add them to your application by

1.  Downloading the toolkit and placing it in your toolkit directory, if
    necessary

2.  Adding an entry for that toolkit to your project's info.xml file

3.  Importing the toolkit with a use directive in your SPL source.

If you did not download the toolkit, you can skip step 1.

You will need to complete step 1 if:

\- you are using an updated version of one of the supported toolkits
\[LINK\] or

\- the toolkit in question was downloaded from GitHub or a 3^rd^ party
toolkit.

\[https://cloud.ibm.com/docs/services/StreamingAnalytics/compatible\_toolkits.html\#compatible\_toolkits\]

Adding a toolkit example
------------------------

Our sample application has been using data that was saved in a file. We
want to change it to retrieve live bus locations from the NextBus
service.

Instead of a FileSource operator, we need to use the HTTPGetXMLContent
operator from the inet toolkit.

The inet toolkit is included in Streams but we want to use the latest
version from Github, so our first taski

### Step 1: Download and unpack the toolkit

a.  Go to <https://github.com/IBMStreams/streamsx.inet/releases>

b.  Download version 3.0 or greater:
    streamsx.inet.toolkit-3.0.0-**el7-amd64**

> ![](media/image59.png){width="4.175573053368329in"
> height="1.5689621609798776in"}
>
> **Note**: Some toolkits have platform dependent features, and so there
> will be that multiple platform dependent releases. If the toolkit you
> wish to use has multiple releases for different platforms, make sure
> to choose the **el7-amd64** release. This is the release that is
> compatible with the Streaming Analytics service.

c.  Place the toolkit in the toolkits directory:

    ![](media/image60.png){width="2.338888888888889in"
    height="2.1662193788276465in"}

    When you copy a toolkit to the toolkit directory, make sure that
    there is a toolkit.xml file is present at the top level of the
    folder, as shown above. I have two toolkits, com.ibm.streamsx.inet
    and com.ibm.streamsx.nlp, and both have a toolkit.xml file.

### Step 2 Add a dependency to the toolkit to your project:

d.  Open the info.xml file of your project, in this case
    BusAlerts/info.xml. If your project does not have an info.xml file,
    create one using the sample \[HERE\]

e.  Add a dependency to the toolkit:

    com.ibm.streamsx.inet toolkit by editing the dependencies node:

    ![](media/image61.png){width="2.9773228346456695in"
    height="2.610255905511811in"}

    Here is a snippet for you to paste:

    \<info:toolkit\>

    \<common:name\>com.ibm.streamsx.inet\</common:name\>

    \<common:version\>\[min\_ver,max\_ver)\</common:version\>

    \</info:toolkit\>

After saving the info.xml file, the com.ibm.streamsx.inet toolkit is
ready for use in our application.

### Step 3: Import the toolkit in your SPL source

Go back to Main.spl.

We're going to replace the BusDataFromFile operator which is a
FileSource, with a HTTPGetXMLContext operator from the inet toolkit.

1.  Import the operator with a **use** directive:

    At the top of Main.spl, type:

    use com.ibm.streamsx.inet.http::HTTPGetXMLContent;

2.  Highlight the operator's definition and then click Edit \> Toggle
    Comment:\
    ![](media/image62.png){width="4.37081583552056in"
    height="1.8001596675415572in"}

3.  Paste the following snippet in the editor:

    stream\<xml locationXMLDoc\> RawData\_Live = HTTPGetXMLContent()

    {

    param

    url : getUrl(\"vehicleLocations\", \$agency);

    period : 30.0; //poll every 30 seconds

    updateParameter: \"t\";

    updateParameterFromContent: \"/body/lastTime/\@time\";

    }

4.  Change the BusLocationStream operator to use the RawData\_Live
    stream instead of the RawData stream:

    Change the line:

    stream\<NextBusLocation\> BusLocationStream =
    ParseNextBusData(RawData)

    to:

> stream\<NextBusLocation\> BusLocationStream =
> ParseNextBusData(RawData\_Live)

5.  Save the application.

> We've now replaced the operator that was reading from a file with one
> that will connect directly to NextBus. Try it out by selecting
> Main.spl \> **Build and submit job**.
>
> After the build succeeds, verify it is working by opening the
> Streaming Analytics console, wait a minute or 2 for the application to
> connect, and then checking the Log Viewer again.

Adding a toolkit: summary
-------------------------

1.  Toolkits must be built, meaning that the top level of the toolkit
    must have a toolkit.xml file.

    a.  If you are downloading a toolkit from GitHub, a built version of
        the toolkit is available from the releases page of the GitHub
        project. If there are releases for different operating systems,
        choose the EL7-AMD64 build.

    b.  If no release exists, or if the downloaded release does not
        include a toolkit.xml file, see the toolkit's page for
        instructions on building it.

2.  Put the toolkit folder into the toolkit directory you created during
    the initial setup\[LINK\]. Recall that you specified this path in
    **the ide-ibmstreams** package settings.

3.  Create a toolkit information file, called info.xml for your project,
    if it does not already have one. This file describes your project
    and its dependencies. Download a sample here: \[LINK\]

    Learn more about the information file here:
    <https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.dev.doc/doc/toolkitinformationmodelfile.html>

4.  Edit the info.xml file to add a dependency to the toolkit you need

    The following is an example of adding com.ibm.streamsx.sometoolkit
    to the project's dependencies:

5.  From your SPL code, import the toolkit with a *use* directive:

    use com.ibm.streamsx.social::\*;

Find out which toolkits are already installed
---------------------------------------------

If you want to use a toolkit and are not sure if it is included in
Streams, the list of Streams toolkits that are supported on the
Streaming Analytics service is here:

https://cloud.ibm.com/docs/services/StreamingAnalytics/compatible\_toolkits.html\#compatible\_toolkits

**Download updated versions of Streams toolkits**

Periodical updates to the toolkits included in Streams are available
from Fix Central

Changing and recompiling a toolkit
----------------------------------
