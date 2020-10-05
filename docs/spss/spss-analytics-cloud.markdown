---
layout: docs
title: SPSS Analytics Toolkit in the Streaming Analytics service on IBM Cloud
description: How to use the SPSS toolkit in the IBM Cloud
weight:  70
published: true
tag: spss
prev:
  file: spss-analytics
  title: SPSS Toolkit Tutorial
next:
  file: spss-analytics-faq
  title: FAQ
---


The Streaming Analytics Service on IBM Cloud provides support for the SPSS Analytics Toolkit.  With this support, your Streams application can perform in-stream predictive scoring using one of your predefined SPSS models.  In this article, we are going to discuss a few tips required to effectively use the SPSS Analytics Toolkit operators in the cloud environment.

This article assumes you have basic understanding of using Streams and the SPSS toolkit. For more on the basic understanding you can refer to:

*   [SPSS Analytics Toolkit Lab]((/streamsx.documentation/docs/spss/spss-analytics)
*   [IBM SPSS and Streams FAQ](/streamsx.documentation/docs/spss/spss-analytics-faq)

## Development Environment Setup

As with all streams applications to be run in the cloud you must first develop, compile and test in a remote development environment and then submit the streams application bundle to execute in the cloud instance.  To work with the SPSS Analytics Toolkit, you need to install the _SPSS Solution Publisher_ product in your development environment.

To support SPSS, the Streaming Analytics Service provisions the SPSS Solution Publisher product in the following location in the cloud environment:

    /usr/IBM/SPSS/ModelerSolutionPublisher/18.2/

To enable your _Streams with SPSS _application for the IBM Cloud environment, you need to be careful with the installation path of the SPSS Solution Publisher product in your development environment.  **You must install the SPSS Solution Publisher product in the same location as it is provisioned in the cloud. **Otherwise, your Streams application will not be able to find the SPSS modeler solution runtime when it is being executed.

## SPSSScoring

The SPSSScoring operator enables predictive scoring in Streams applications using a predefined SPSS model.  It is assumed that these models are defined offline and then exported from SPSS Solution Publisher.  The export produces three files that are required by the SPSSScoring operator:

*   model.pim
*   model.par
*   model.xml

Typically, these files are expected to be stored in the data directory.  The cloud environment has special restrictions on data directory and file creations.  Therefore, for the cloud environment, it is advisable to store these files as part of the application bundle, to ensure that the application can locate these files at runtime.   For example, you may store these files in the /etc directory of your application for them to be included in the application bundle automatically.

![SPSSDirectoryStructure](/streamsx.documentation/images/spss/SPSSDirectoryStructure.jpg)

Next, in the SPL code you can specify the file locations as follows:

    stream<DataSchemaPlus> scorer = com.ibm.spss.streams.analytics::SPSSScoring(data)
    {
      param
        **pimfile: getThisToolkitDir() +"/etc/PimParXml/model.pim";
        parfile: getThisToolkitDir() +"/etc/PimParXml/model.par";
        xmlfile: getThisToolkitDir() +"/etc/PimParXml/model.xml";**
        modelFields: "sex","income";
        streamAttributes: s_sex, baseSalary+bonusSalary;

      output
        scorer:
        income = fromModel("income"),
        predLabel = fromModel("$C-beer_beans_pizza"),
        confidence = fromModel("$CC-beer_beans_pizza");
    }

The SPSS scoring operator also supports dynamic model refresh using a second optional input port where notification of a new model PIM file can be passed in. This input tuple must contain the filename of the new PIM file to use.

In the cloud environment, for security reasons, clients are not allowed to arbitrarily write files onto the file system.  Therefore, special techniques are required to send a new model PIM file to your Streams application:

1.  **Use FileSink to write new file** – In this approach, submit a second job to use a Filesink operator to write the new PIM file.  See this for details:  [Use of FileSink to write output data](https://developer.ibm.com/streamsdev/docs/getting-spl-application-ready-cloud/)
   
2.  **Use SPSS Publish Operator** – In this approach, use the SPSSPublish operator from the SPSS toolkit to publish a new PIM file.  See the next section for more details.

Please note that the cloud environment does not have a shared file system.  Therefore, when writing the new model files in the cloud to facilitate dynamic model update, you need to ensure that the files are written onto the same host where the SPSSScoring operator is executed.  In other words, whatever SPL operator is being used to produce the refreshed file, that operator must be co-located on the same host as the SPSSScoring operator.

## SPSSPublish

The SPSSPublish operator automates the ‘publish’ of a Modeler file’s scoring branch and summarizes the generated files so down-stream operators can refresh their scoring implementation with the PIM, PAR and XML files created or updated by the ‘publish’ operation.

Typically, the SPSSPublish operator is used in conjunction with a DirectoryScan or SPSSRepository operator upstream, and a SPSSScoring operator downstream.

For example, you will see a topology like this:
        
        DirecoryScan/SPSSRepository -> SPSSPublish -> SPSSScoring

The DirectoryScan or SPSSRepository operator detects that new model files are available, and sends the filenames of the new models to the SPSSPublish operator.   Downstream from the SPSSPublish operator is usually a SPSSSoring operator.  The SPSSPublish operator gets the new models, generates the required PIM, PAR and XML files, and sends a notification to the SPSSScoring operator that a new model is available.  The SPSSScoring operator will refresh its internal model upon this notification.

This technique will work in the cloud environment but requires that you have a separate job for writing the new file to the same host that the directory scan, publish and scoring operators are running on.

To ensure that all of the required operators are co-located on the same host, you may assign the affected operators in the same hostpool as follows:

*   Create a host pool in your application by adding this config clause in the main composite:

          config hostPool: P1=createPool({size=1u, tags=["host1"]}, Sys.Shared);

*   Assign all affected operators to this host pool by adding this config clause in each of the operator invocation:

          config placement : host(P1);

Here’s an example on how to do this:

### Publish and Scoring Job

  composite SPSSPublishScoringExample {
    type
      static DataSchema =
        rstring s_sex,
        int64 baseSalary,
        int64 bonusSalary;

      static DataSchemaPlus =
        DataSchema, tuple<int64 income, rstring predLabel, float64 confidence>;

    graph
      stream<rstring strFilePath> strFile = DirectoryScan(){
        param
          directory : "/tmp";
          pattern : "newmodel.str";
          ignoreExistingFilesAtStartup : true;
        config placement : host(P1);
      }

    () as trace1 = Custom(strFile) {
      logic
        onTuple strFile:{
          printStringLn("** 1 ** File notification: " + strFilePath);
        }
    }

    stream<rstring fileName> notifier = com.ibm.spss.streams.analytics::SPSSPublish(strFile){
      param
        sourceFile: "newmodel.str";
        targetPath: "/tmp";
      config placement : host(P1);
    }

    () as trace2 = Custom(notifier) {
      logic
        onTuple notifier:{
          printStringLn("** 2 ** Publish notification: " + fileName);
        }
    }

    stream<DataSchema> data = Beacon() {
      param
        period: 1.0; 

      output
        data: s_sex = ((random() > 0.5) ? "F" : "M"),
        baseSalary = (int64)(1.0 /*random()*/ * 150000.0),
        bonusSalary = (int64)(2.0 /*random()*/ * 25000.0);
    }

    stream<DataSchemaPlus> scorer = com.ibm.spss.streams.analytics::SPSSScoring(data;notifier) {
      param
        pimfile: getThisToolkitDir() +"/etc/PimParXml/model.pim";
        parfile: getThisToolkitDir() +"/etc/PimParXml/model.par";
        xmlfile: getThisToolkitDir() +"/etc/PimParXml/model.xml";
        modelFields: "sex","income";
        streamAttributes: s_sex, baseSalary+bonusSalary;

      output
        scorer:
          income = fromModel("income"),
          predLabel = fromModel("$C-beer_beans_pizza"),
          confidence = fromModel("$CC-beer_beans_pizza");
      config placement : host(P1);
    }

    () as Writer = FileSink(scorer) {
      param file: "/tmp/SPSSPublishScoring_output.csv";
        flush : 1u;
      config placement : host(P1); 
    }

    () as trace3 = Custom(scorer) {
      logic
        onTuple scorer:{
          println(scorer);
        }
      }

    config hostPool: 
      P1=createPool({size=1u, tags=["host1"]}, Sys.Shared); //sized, tagged, shared
    }

### File Writing Job

    composite FilePutter
    {
      graph
        stream<blob myline> inLine = FileSource()
        {
          param
            file : getThisToolkitDir() +"/etc/putter/model.str"  ;
            format : block;
            blockSize : 1024u;
            config placement : host(P1);
        }

        () as FileSink_2 = FileSink(inLine)
        {
          param
            file : "/tmp/newmodel.str";
            format : block;
            config placement : host(P1);
        }
        config hostPool: 
            P1=createPool({size=1u, tags=["host1"]}, Sys.Shared); //sized, tagged, shared
    }

## SPSSRepository

The SPSSRepository operator is configured to listen for specific change notifications to an object deployed in the SPSS Collaboration and Deployment Services repository. When the monitored object is changed in the repository, a notification is sent out to all listeners.  Upon the notification, the SPSSRepostory operator downloads the file version of the changed object from the repository and writes the file to a target directory.  On successful download, an output tuple describing the file updated is submitted to communicate this event to down-stream operators.

For use in the cloud environment, you need to ensure the following:

1.  For the SPSSRepository operator to receive notifications from the SPSS Collaboration and Deployment Services server, make sure this server is accessible from the cloud.
2.  The **targetFilePath** parameter in the SPSSRepository operator describes the target directory where it will save the file versions of updated objects from the repository.  Make sure the **targetFilePath** is set to **/tmp**, when the operator is running in the cloud environment.
3.  When executed in the cloud, make sure this operator is co-located on the same host as the SPSSScoring operator for which your SPSSRepository operator is sending notifications to.
