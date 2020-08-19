---
layout: docs
title: Streams and SPSS - Frequently Asked Questions
description: Common questions about integrating with SPSS 
weight:  80
published: true
tag: spss
prev:
  file: spss-analytics-cloud
  title: SPSS Toolkit in the Cloud
---


This answers the common questions we get about using IBM Streams and SPSS together.

## Why use Streams and SPSS together?  
IBM SPSS Modeler provides a state-of-the-art environment for understanding data and producing predictive models. Streams provides a scalable high-performance environment for real-time analysis of data in motion, including traditional structured or semi-structured data, and unstructured data types. Some applications have a need for deep analytics derived from historic information to be used to score streaming data in low-latency, high-volume, and real time, and to leverage those analytics. The SPSS Analytics Toolkit for Streams lets you integrate the predictive models designed and trained in IBM SPSS Modeler with your IBM Streams applications.

## What do I need to use them together?

1.  You need models built with the IBM SPSS Modeler product. The SPSS Modeler product is installed on a windows workstation.
2.  You need Streams installed on the linux machine(s) where Streams will be running.
3.  You need the linux Solution Publisher component of the SPSS Collaboration and Deployment Services Product installed on any node in the Streams cluster that will be used to score SPSS models in Streams.
4.  You need to configure the streams application to reference the SPSS Analytics Toolkit for Streams which was installed as part of the Solution Publisher install.

## Where can I find Information on how to use the 2 together?

1.  The Streams RedBook _<span style="text-decoration: underline;">IBM Streams: Accelerating Deployments with Analytic Accelerators</span>_ describes visual development, visualization, adapters, analytics, and accelerators for Streams. Chapter 15 covers the SPSS toolkit and it describes the required steps from model building to implementing published models into Streams as well as the development process itself. The redbook can be downloaded for free [here](http://www.redbooks.ibm.com/abstracts/sg248139.html?Open).
2.  For a step by step walk through of using the operators in the toolkit, [complete the SPSS Analytics toolkit lab](/streamsx.documentation/docs/spss/spss-analytics).
3.  The SPSS Analytics Toolkit for Streams documentation has full details on installation, operators and example usage.
    *   Toolkit for [Streams v4 and SPSS Modeler Solution Publisher version 17 and later](https://github.com/IBMPredictiveAnalytics/streamsx.spss.v4/blob/master/IBM SPSS Analytics Toolkit for Streams.pdf)

## What about PMML and the Modeling Toolkit provided in the Streams product?  
Streams includes a [PMML toolkit](https://community.ibm.com/community/user/cloudpakfordata/viewdocument/integrating-pmml-scoring-into-your?CommunityKey=c0c16ff2-10ef-4b50-ae4c-57d769937235&tab=librarydocuments) that supports scoring models in PMML (Predictive Model Markup Language) format. The PMML toolkit should work with any “compatible” PMML models at the specified versions and with models saved in Watson Machine Learning.

While SPSS Modeler can produce PMML, it does not produce it at the required versions so **PMML from SPSS cannot be used with the Mining Toolkit**.

## So why use SPSS Modeler published modeler streams vs PMML models?  
The short answer is more models, additional flexibility, and support for model deployment and management.

Using SPSS Analytics Toolkit for Streams offers more power than simply exporting the model (as PMML), because it allows you to publish and deploy complete IBM SPSS Modeler streams. That means you can perform data preparation as well as record and field operations, such as aggregating data, selecting records, or deriving new fields, before creating predictions based on a model. You can then further process the model results before saving the data–all simply by executing the published stream.

It supports all the mode types available in the SPSS Modeler palette, and you can combine multiple models in a single published IBM SPSS Modeler stream.

In addition the SPSS Toolkit provides operators that interact with the SPSS model repository. Specifically the following operators are provided:

*   **SPSSScoring** – integrates with SPSS Modeler Solution Publisher to the enable the scoring of your SPSS Modeler designed predictive models in Streams applications
*   **SPSSPublish** – automates the SPSS Modeler Solution Publisher ‘publish’ function which generates the required executable images needed to refresh the model used in your Streams applications from the logical definition of an SPSS Modeler scoring branch defined in a SPSS Modeler file
*   **SPSSRepository** – detects notification events indicating changes to the deployed models managed in the SPSS Collaboration and Deployment Services repository and retrieves the indicated Modeler file version for automated publish and preparation for use in your Streams applications

## What about the R support available in Streams?  
Streams provides the R-project Toolkit which contains an operator that facilitates integration between Streams and the R environment.

R is a language and environment for statistical computing and graphics. For example, it provides statistical techniques such as linear and nonlinear modeling, time-series analysis, clustering, and classification. For more information about R, [see http://www.r-project.org](http_/www.r-project.html).

The R-project toolkit contains the RScript operator which maps input tuple attributes to objects that can be used in R commands. It then runs a script that contains R commands and maps the objects that are output from the script to output tuple attributes. Your script provided to the operator can use any appropriate R statements including those that apply data mining algorithms.  

For more information about integrating R and Streams, see the toolkit documentation: [here](https://www.ibm.com/support/knowledgecenter/en/SSCRJU_5.3/com.ibm.streams.toolkits.doc/toolkits/dita/tk$com.ibm.streams.rproject/tk$com.ibm.streams.rproject.html) and [this tutorial.](https://developer.ibm.com/streamsdev/docs/r-toolkit-lab/)
