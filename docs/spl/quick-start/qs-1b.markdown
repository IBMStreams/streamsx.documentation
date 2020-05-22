---
layout: docs
title:  Run your first IBM Streams application with VS Code
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

Run your first Streams application using VS Code


## Installation and Setup


## Import the sample application

The application we will use is called **TradesAppCloud** in the **TradesApp** project. It processes a stream of stock quotes for various companies, each identified by a ticker.
It computes the rolling average price for each unique stock ticker and prints it to standard out.

Download the sample application project using this URL: `https://streams-github-samples.mybluemix.net/?get=QuickStart%2FTradesApp`

## Compiling the application
## Run the application
Explain how to launch to IBM Cloud or SAS
Tabs might be helpful

<ul class="nav nav-tabs">
  <li class="active"><a data-toggle="tab" href="#Cloud"><b>Cloud</b></a></li>
   <li><a data-toggle="tab" href="#SAS"><b>SASo</b></a></li>
</ul>

<div class="tab-content">

<div id="Cloud" class="tab-pane fade in active">
<!--- STREAMING ANALYTICS SERVICE ---->
Stuff for Cloud
</div>

  <div id="SAS" class="tab-pane fade">
Stuff for SAS
</div>


## View the running application
  Job graph in Streams explorer
  Streams Console

### Observe the data flowing through the application in real time

### View Job Logs



#### Launch the application using the Streams Console

1. You need to get the URL of the Streams Console for your Streams instance. 
   - **Find the URL for Streams add-on in IBM Cloud Pak for Data:**
     - From the navigation menu, click <strong>My instances</strong>.
     - Click the <strong>Provisioned Instances</strong> tab.
     - Find your Streams instance, and click **View details** from the context menu. Open the URL under **External console endpoint**.
       
   - **Find the URL for Streams stand-alone deployment:** [See the documentation](https://www.ibm.com/support/knowledgecenter/en/SSCRJU_5.2.0/com.ibm.streams.dev.doc/doc/find-dns-url.html#find-dns-url). Choose *finding the internal URL*  or *finding the external URL* depending on whether or not you will be accessing the Streams Console from within the Kubernetes cluster.


2. From the Streams Console, click **Submit job**:
  <br/>
![submit job](https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/11/streams-submit-job.png)

   * Browse to the location of the compiled application.  This will be a `.sab` file in the `output` folder of your project.
   * Set any parameters, and submit the application.

You should see a popup like this once submission is successfull:

<img alt="job success" src="/streamsx.documentation/images/qse/submit-console.png"/>

Notice that a running Streams application is called a *job*.

Keep these steps in mind for submitting applications for IBM Cloud Pak for Data when developing with Streams Studio.

## View the running application in Cloud Pak for Data

After launching the application in the Streams Console you can go to the Job Graph in Cloud Pak for Data to view the running application. 

1. From the main menu, go to **My Instances** > **Jobs**. This will bring you to the list of jobs.
2. Find your job in the list  based on its name, and from the context menu of the job, click **View job graph**.

A new page called the Job Graph should open. 
This shows a graph that represents the application we launched. Streams applications are really directed graphs that analyze data as it is processed. Each node in the graph is an **operator** that processes data, and each arrow represents a **stream** of live data. 

<img alt="job graph in cpd" src="/streamsx.documentation/images/qse/graph-cpd.jpg"/>




### Summary

## Cancel the job

### References
- Streams studio documentation
- Streams in Cloud Pak for Data documentation