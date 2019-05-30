---
layout: docs
title:  Configure Atom
description:  Steps to configure Atom for SPL development
navlevel: 2
tag: atom
prev:
  file: atom-apps
  title: Introduction
next:
  file: atom-guide-2-import-code
  title: Importing your code into Atom
---



Download the Streams plugins for Atom
--------------------------------------------------

If you haven't already done so, [download and install
Atom](https://atom.io).

*atom-ide-ui, ide-ibmstreams, language-ibmstreams-spl,
build-ibmstreams*:

-   Go to **Atom** \> **Preferences** \> **Install** \> **Packages**
    (might be different for Windows)

-   Search for each of the above packages and install it:

    ![Screenshot of Atom package install](/streamsx.documentation/images/atom/jpg/install-package.jpg)


-   Install the Streams themes:

    -   **Atom** \> **Preferences** \> **Install** \> **Themes**

    -   Search for and install either of *streams-dark-syntax* or
        *streams-light-syntax*.

Create an instance of the Streaming Analytics service
---------------------

Instead of downloading the Streams compiler and runtime to create your applications, you will use the Streaming Analytics service, a cloud based version of Streams. Applications created in Atom are sent to the Streaming Analytics to be compiled and executed.


* If you have a Streaming Analytics service in [IBM Cloud](https://console.ng.bluemix.net/), make sure that it is started and running.

* To create a new Streaming Analytics service:
  1. Visit to the [IBM Cloud web portal](https://www.ibm.com/cloud-computing/bluemix/) and sign in (or sign up for a free account).

  2. Go to the [Streaming Analytics service](https://console.bluemix.net/catalog/services/streaming-analytics) page within the Catalog.

  3. Enter the service name and then click **Create** to set up your service. The service dashboard opens and your service starts automatically. The service name appears as the title of the service dashboard.


Add the credentials for your Streaming Analytics service
--------------------------

1. From the IBM Cloud dashboard, click the instance of the Streaming Analytics service you created earlier to go to the service's main page.
   ![service main page](/streamsx.documentation/images/atom/jpg/sa-manage-page.jpg)

6. Make sure the service is started, if not, click **Start**.

8. Click **Service Credentials** to get the credentials for the service.  If there are no credentials listed, click **New Credentials** to create one, accepting the defaults.

11. Copy the credentials:
   ![Screenshot of credentials page](/streamsx.documentation/images/atom/jpg/creds.jpg)

15. In Atom, go to **Preferences > Packages**. Find the **build-ibmstreams** package and click **Settings**.

18. Paste the credentials you copied in to the **Settings** text box.



Add a toolkits folder
---------------------------
-  Designate an empty folder on your local filesystem as your toolkits directory. This folder will contain any additional toolkits that you want to use in your application. See the section on [extending your application with toolkits](/streamsx.documentation/docs/spl/atom/atom-guide-6-toolkits) to learn more.

-  In Atom, go to Preferences \> Packages**. Find the **ide-ibmstreams** package and click **Settings.** Paste the path to the toolkit directory you just created in the **Toolkits Path** box.
    ![Toolkit dir setting](/streamsx.documentation/images/atom/jpg/toolkit-dir.jpg)

Migrating from Streams Studio
------------------------------
If you have been using Streams Studio, below you can find a summary of major differences between Streams Studio and Atom.

-   **SPL Projects from Streams Studio** can be used in Atom without having to make any changes. See the [importing your code section](/streamsx.documentation/docs/spl/atom/atom-guide-2-import-code/) for instructions.

-   **Adding a Streams Toolkit to your workspace** is discussed in the [toolkits section](/streamsx.documentation/docs/spl/atom/atom-guide-6-toolkits/).

- Although the **SPL Graphical Editor** is not available, you can view an application's graph in the Streams Console.

- **Build Configurations** are not used to compile or launch
applications from Atom. To compile an SPL composite, you select the SPL file containing the composite, right click, and choose **Build** or **Build and submit job**.

    ![build action](/streamsx.documentation/images/atom/jpg/build-submit.jpg)

-   **Streams Installation, Instance and Domain Management:** SPL
Plugins for Atom do not include any Domain or Instance management features because your Streams instance is created and managed in the IBM Cloud. You can configure your Streams instance from the  Streaming Analytics Console.

-   **Application Monitoring:** Applications launched from Atom are executed on the Streaming Analytics service. Thus, you need to use Streams Console to view metrics, errors, and the Streams graph.
