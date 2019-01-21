---
layout: docs
title:  Configure Atom
description:  Steps to configure Atom for SPL development
navlevel: 2
tag: atom
prev:
  file: /
  title: Introduction
next:
  file: atom-guide-2-import-code
  title: Importing your code into Atom
---


If you haven't already done so, download and install
Atom.(https://atom.io)

### Set up and download the Streams plugins for Atom:

*atom-ide-ui, ide-ibmstreams, language-ibmstreams-spl,
build-ibmstreams*:

-   Go to **Atom** \> **Preferences** \> **Install** \> **Packages**
    (might be different for Windows)

-   Search for each of the above packages and install it:

    ![Screenshot of Atom package install](/streamsx.documentation/images/atom/jpg/install-package.jpg)


-   Install the themes of your choice:

    -   **Atom** \> **Preferences** \> **Install** \> **Themes**

    -   Search for and install either of *streams-dark-syntax* or
        *streams-light-syntax*.

#### Add the credentials for your Streaming analytics service:

-   From the IBM Cloud dashboard, click the
    instance of the Streaming Analytics service you created earlier.
    This will bring you to the service's main page.

    ![service main page](/streamsx.documentation/images/atom/jpg/sa-manage-page.jpg)

-   Make sure the service is started, if not, click **Start**.

-   Click **Service Credentials** to get the credentials for the
    service.

    -   If there are no credentials listed, click **New Credentials** to
        create one, accepting the defaults.

-   Copy the credentials:

 ![Screenshot of credentials page](/streamsx.documentation/images/atom/jpg/creds.jpg)

-   Go to **Atom \> Preferences \> Packages. Find the
    build-ibmstreams** package and click **Settings**.

-   Paste the credentials you copied in to the **Settings** text box.



#### Add a toolkits folder:
-  Designate an empty folder on your local filesystem as your
        toolkits directory. This folder will contain any additional
        toolkits that provide extra functionality.

-   Go to **Atom \> Preferences \> Packages. Find the
        ide-ibmstreams** package and click **Settings.** Paste the path
        to the toolkit directory you just created in the **Toolkits
        Path** box.

![Toolkit dir setting](/streamsx.documentation/images/atom/jpg/toolkit-dir.jpg)

### Migrating from Streams Studio

If you have been using Streams Studio, below you can find links to
sections that show you how to import your projects, compile a summary of
major differences between Streams Studio and Atom.

-   **SPL Projects from Streams Studio** can be used in Atom without
    having to make any changes. See the Get your Code into Atom section
    \[LINK\] for instructions on how to do this.

-   **Adding a Streams Toolkit to your workspace** is discussed in the
    Extending your application with toolkits section[LINK\].

-   **The SPL Graphical Editor** is not available, you can view an
    application's graph in the Streams Console.

-   **Build Configurations** are not used to compile or launch
    applications from Atom.

    To compile an SPL composite, you select the SPL file containing the
    composite, right click, and choose Build or Build and Submit.

    ![Toolkit dir setting](/streamsx.documentation/images/atom/jpg/build-submit.jpg)

-   **Streams Installation, Instance and Domain Management:** SPL
    Plugins for Atom do not include any Domain or Instance management
    features because your Streams instance is created and managed in the
    IBM Cloud. You can configure your Streams instance from the
    Streaming Analytics Console. Learn more about the Streams Console
    here\[LINK\].

-   **Application Monitoring:** Applications launched from Atom are
    executed on the Streaming Analytics service. Thus, you need to use
    Streams Console to view metrics, errors, and the Streams graph.
