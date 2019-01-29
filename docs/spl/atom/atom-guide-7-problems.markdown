---
layout: docs
title:  Troubleshooting
description:  Fixing common problems
navlevel: 2
tag: atom
prev:
  file: atom-guide-6-toolkits
  title: Adding a toolkit to your application
---


The following are some known issues and their workarounds.

1.  You tried to open the Streams Console from Atom but got this error:

    ```
    CWOAU0062E: The OAuth service provider could not redirect the
    request because the redirect URI was not valid. Contact your system
    administrator to resolve the problem.
    ```

    If this occurs, open the Streams Console from your browser:
    1. Log in to the [IBM Cloud Dashboard](https://cloud.ibm.com)

    2. Access the console through one of the following ways:

      -   From the dashboard, click on your Streaming Analytics service
          instance under Services. Then from the instance page, click
          "Launch" to go to the console

      Once you are logged in, opening the Console from Atom will work.

      You can also find the console URL from the direct link available in the Atom Console pane.
          Look for *Streaming Analytics Console URL*.

2.  Compiling an application fails with this message:

    ```
    CDISP0127E ERROR: The following toolkit file is out of date:
      ../toolkits/com.ibm.streamsx.inet/toolkit.xml. This file is newer:
      ../toolkits/com.ibm.streamsx.inet/com.ibm.streamsx.inet/InetSource/InetSource.xml.

    ```
This error means a file in a toolkit you downloaded has changed.
If you did not make any changes, this might be a bug that you can work around by doing the following:

    a.  Open a terminal window and change to the toolkits directory where you copied additional toolkits:

        cd /Users/path/to/tkdir

    b. For each toolkit listed in the error message, change to that toolkit directory.

        cd com.ibm.streamsx.inet
        find . -name "function.xml" -print0 | xargs  touch
        find . -name "toolkit.xml" -print0 | xargs  touch

    These commands are for a Mac.  On Linux the arguments to `xargs` might be slightly different.

Try recompiling your application.
