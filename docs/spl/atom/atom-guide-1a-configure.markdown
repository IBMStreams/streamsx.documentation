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

Download the Streams Packages for Atom
--------------------------------------

If necessary, [download and install Atom](https://atom.io). To install the Streams Packages for Atom:

1. In Atom, open the package installation screen:
* Mac: **Atom > Preferences > Install > Packages**
* Windows&reg;: **File > Settings > Install > Packages**
  ![Screenshot of Atom package install](/streamsx.documentation/images/atom/jpg/install-package.jpg)

2. Search for each of the following packages and install them:
* atom-ide-ui
* ide-ibmstreams
* language-ibmstreams-spl
* build-ibmstreams

3. In Atom, open the Streams themes:
* Mac: **Atom > Preferences > Install > Themes**
* Windows&reg;: **File > Settings > Install > Themes**

4. Search for and install the following themes if you want to:
* streams-dark-syntax
* streams-light-syntax

Create an instance of the Streaming Analytics service
-----------------------------------------------------

Instead of downloading the tools to set up your own Streams environment, you can use the Streaming Analytics cloud service. Applications that are created in Atom can be sent to the Streaming Analytics service to be compiled and run.

If you already have an instance of Streaming Analytics service in [IBM Cloud](https://console.ng.bluemix.net/), make sure that it is started and running.

To create a new instance of the Streaming Analytics service, you need to complete the following steps:
1. Go to the [IBM Cloud web portal](https://www.ibm.com/cloud-computing/bluemix/) and sign in (or sign up for a free account).
2. Go to the [Streaming Analytics service](https://console.bluemix.net/catalog/services/streaming-analytics) page within the Catalog.
3. Enter the service name and then click **Create** to set up your service. The service dashboard opens and your service starts automatically. The service name appears as the title of the service dashboard.

Add the credentials for your Streaming Analytics service
--------------------------------------------------------

In order for Atom to connect to your Streaming Analytics instance, your build-ibmstreams package needs to be configured with your instance's service credentials:

1. From the IBM Cloud dashboard, click the instance of the Streaming Analytics service you created earlier to go to the service's main page.
  ![service main page](/streamsx.documentation/images/atom/jpg/sa-manage-page.jpg)

2. Make sure the service is started, if not, click **Start**.

3. Click **Service Credentials** to get the credentials for the service.  If there are no credentials listed, click **New Credentials** to create one, accepting the defaults.

4. Copy the credentials:
  ![Screenshot of credentials page](/streamsx.documentation/images/atom/jpg/creds.jpg)

5. If you are using a Mac, go to **Atom > Preferences > Packages**. If you are using Windows&reg; go to **File > Settings > Packages**. Find the **build-ibmstreams** package and click **Settings**.

6. Paste the credentials you copied in to the **Settings** text box.

Add a toolkits folder
---------------------

Streans toolkits provide extra functionality to your Streams applications, such as enabling you to connect to a data source like Kafka. See [extending your application with toolkits](/streamsx.documentation/docs/spl/atom/atom-guide-6-toolkits) to learn more. Before you can add toolkits into your applications, you need to complete the following:

1. Designate an empty folder on your local filesystem as your toolkits directory. This folder will contain any additional toolkits that you want to use in your application.

2. If you are using a Mac, go to **Atom >  Preferences > Packages**. If you are using Windows&reg;, go to **File > Settings > Packages**. Find the **ide-ibmstreams** package and click **Settings**. Enter the path to the toolkit directory you just created in the **Toolkits Path**.
    ![Toolkit dir setting](/streamsx.documentation/images/atom/jpg/toolkit-dir.jpg)

Switch from Streams Studio Development
-----------------------------------------
If you have used Streams Studio, the following list summarizes some important things to look out for.

- **SPL Projects from Streams Studio** can be used in Atom without having to make any changes. See the [importing your code section](/streamsx.documentation/docs/spl/atom/atom-guide-2-import-code/) for instructions.

- **Adding a Streams Toolkit to your workspace** is discussed in the [toolkits section](/streamsx.documentation/docs/spl/atom/atom-guide-6-toolkits/).

- Although the **SPL graphicaleditor** is not available, you can view an application graph in the Streams Console.

- **Build Configurations** are not used to compile or run applications from Atom. To compile an SPL composite, you select the SPL file containing the composite, right click, and choose **Build** or **Build and submit job**.
    ![build action](/streamsx.documentation/images/atom/jpg/build-submit.jpg)

- **Streams Installation, Instance and Domain Management:** SPL Plugins for Atom do not include any domain or instance management features because your Streams instance is created and managed in the IBM Cloud. You can configure your Streams instance from the Streaming Analytics Console.

- **Application Monitoring:** Applications that are started from Atom are executed on the Streaming Analytics service. Thus, you must use Streams Console to view metrics, errors, and the Streams graph.
