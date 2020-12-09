---
layout: docs
title:  Run your first IBM Streams application with Visual Studio Code
description:  Learn how to get started with IBM Streams
weight:  40
published: true
tag: spl-qs
navlevel: 2
prev:
  file: qs-1
  title: Run your first application
next:
  file: qs-2
  title: Overview of Streams Concepts
---


You can use [Microsoft Visual Studio Code](https://code.visualstudio.com/) (VS Code) to edit and deploy Streams applications. You do not need to download the Streams runtime, but only the [Streams extension for VS Code](https://ibmstreams.github.io/vscode-ide/). 

This guide will walk you through deploying and monitoring a Streams application from using VS Code.


## Prerequisites

- You need access to an instance of IBM Streams on Cloud Pak for Data or the Streaming Analytics service.
  
- You should have set up the Streams extension for VS Code. Specifically, follow the [steps in the documentation](https://ibmstreams.github.io/vscode-ide/docs/) to:

  -  [Install VS Code and the Streams extension](https://ibmstreams.github.io/vscode-ide/docs/quick-start-guide/#installation-and-setup)

  -  [Add your Streams instance](https://ibmstreams.github.io/vscode-ide/docs/streams-explorer/#adding-an-instance)


After completing these steps, you're ready to run and import the sample.


## Import the sample application


The `TradesApp` sample application processes a stream of stock quotes for various companies, each identified by an id, or ticker.
It computes the rolling average price for each unique stock ticker and prints it to standard out.

1.  Download the sample application project from [here](https://streams-github-samples.mybluemix.net/?get=QuickStart%2FTradesApp).
2.  Extract the zip files into a folder.
3.  Import the application into VS Code:
    1.  Go to **File** > **Open...** (or **Add Folder to Workspace...**).
    2.  Browse to the project folder and click on **Open** (or **Add**).

<img src="/streamsx.documentation/images/vs-code/vs-code-import-sample-app.png" alt="Install sample application" class="vs-code-img" />

## Compiling the application

1.  Bring up the [Explorer](https://code.visualstudio.com/docs/getstarted/userinterface#_explorer) view on the left and expand the `application` folder.
1.  Then, either:
    - Right-click on the `TradesAppCloud.spl` file.
    - Double-click on the `TradesAppCloud.spl` file to open it in the editor and right-click in the editor.

    You will see two build options:

    - **Build**: Builds your Streams application and downloads the application bundle (`.sab`) to the application's `output` folder.
    - **Build and Submit Job**: Builds your Streams application and submits it directly to a Streams instance of your choice.
- 

    <img src="/streamsx.documentation/images/vs-code/vs-code-build-app-options.png" alt="Compile application options" class="vs-code-img" />
1.  Select **Build**.

This will build the application using the Streams instance you added previously. As the build progresses, you will see notifications appear in the bottom right corner and the build output will be displayed in the application's output channel in the **OUTPUT** panel at the bottom.

<img src="/streamsx.documentation/images/vs-code/vs-code-build-app.png" alt="Compiling the application" class="vs-code-img" />

Once the build finishes successfully, a Streams application bundle file called `application.TradesAppCloud.sab` is generated in the project's `output` folder. We will use this in the next step to run the application.

## Run the application

To run the application, you will need to submit the bundle file from the previous step to your Streams instance. Note that a running Streams application is called a *job*.

1.  Bring up the [Explorer](https://code.visualstudio.com/docs/getstarted/userinterface#_explorer) view on the left and expand the `output` folder.
1.  Right-click on the `application.TradesAppCloud.sab` file and select **Submit Job**.
1.  You will prompted for the job configuration before the job is submitted. 
    1.    If you are using Cloud Pak for Data v3.5 or newer, you will need to specify a **job definition name**. This is the name that is used to group all executions of this job in Cloud Pak for Data. 
    2.   You can also optionally specify a **Streams job name**. This is to identify the job within the Streams instance.
    3.  For more advanced configuration options, click **Show all options** to  upload a job configuration overlay JSON file, provide a description for the job, and more.

2.   This application has no parameters, so click **Submit job.** 
   <br/> <img src="/streamsx.documentation/images/vs-code/vs-code-configure-job-submission.png" alt="Configure the job submission" class="vs-code-img" />
  *Submit Job page. The job submission options depend on the Streams instance you are using.*


This will submit the application to the Streams instance you added previously. As the submission progresses, you will see notifications appear in the bottom right corner and the submission output will be displayed in the **IBM Streams** output channel in the **OUTPUT** panel at the bottom.

<img src="/streamsx.documentation/images/vs-code/vs-code-submit-app.png" alt="Run the application" class="vs-code-img" />

Once the submission finishes successfully, the **TradesAppCloud** application will be running in your instance! The success notification in the bottom right corner will show you some options to work with your new job. We'll cover them in the next step.

You can see the new job by clicking on the Streams icon on the left to bring up the **Streams Explorer** view. When you select the job in the **INSTANCES** pane, the **DETAILS** pane will update to display the job details.

## Monitor the running application

Once your application is running, you may want to monitor the job. The steps to do this depend on the version of the Streams instance you added.

{% include vs-code/monitor_running_app.html %}

## Cancel the job

Bring up the **Streams Explorer** view. Hover over the job node and then click on the **Cancel Job** icon that appears on the right.
    <img src="/streamsx.documentation/images/vs-code/vs-code-cancel-job-streams-explorer.png" alt="Cancel job: Streams Explorer" class="vs-code-img" />

## Summary

In this section, you learned how to:

- Install and set up the IBM Streams extension for VS Code
- Add a Streams instance
- Import an application
- Compile an application
- Run the application
- Monitor the running application using the job graph and Streams Console by viewing the data on a stream and viewing application logs
- Cancel a job

In the next section, you'll learn how to create the sample application that you've been working with.

## References
- [IBM Streams for IBM Cloud Pak for Data documentation](https://www.ibm.com/support/producthub/icpdata/docs/content/SSQNUZ_current/cpd/svc/streams/developing-intro.html)
- [IBM Streams standalone documentation](https://www.ibm.com/support/knowledgecenter/en/SSCRJU_5.2.0/com.ibm.streams.welcome.doc/doc/kc-homepage.html)
- [IBM Streaming Analytics in IBM Cloud documentation](https://cloud.ibm.com/docs/StreamingAnalytics?topic=StreamingAnalytics-gettingstarted)
- [Visual Studio Code documentation](https://code.visualstudio.com/docs)
