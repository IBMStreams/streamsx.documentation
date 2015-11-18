---
layout: docs
title: IBM Streams Data Governance Quickstart
description:  IBM Streams Data Governance Quickstart
weight: 50
---
# IBM Streams Data Governance Quickstart

### What you need to get started
*IBM Information Governance Catalog*
*Version*: 11.5 (also tested with 11.3 with fixes)
You need to know the IGC (Information Governance Catalog) server address.  This is required to upload the Streams asset definition bundle, set the governance server property in the instance, add the catalog to Streams explorer etc...

You also need a set of credentials (userid and password) for the IGC.  The instance will use these credentials to register applications and lineage flows in the governance catalog.  When accessing the catalog from Streams Studio the user can supply their individual credentials.  

### Add Streams asset definitions to IBM Information Governance Catalog

You need to upload the Streams asset definition file to the IGC.  This only needs to be done once.  The file is contained in the Streams install.  This file needs to be available on host you start the browser on.

1. open browser with *_`https://<IGC host:port>/ibm/iis/igc-rest-explorer/#!/bundles/registerBundle`_*
<img src="/streamsx.documentation/images/governance/bundleupload.png" style=" margin-left:auto; margin-right:auto; display: block;" />
2. press the browse button and navigate to `<streams_install>/4.1.0.0/etc/governance/StreamsIGCAssetDefinitions.zip`
3. Press try it out to upload the bundle.

Validate using this URL: `https://<IGC host:port>/ibm/iis/igc/#allAssetTypes/`
and you should see InfoSphere Streams (you may have to scroll)
<img src="../../../../images/governance/infospherestreamscatalogassets.png" style="margin-left:auto; margin-right:auto; display: block;" />


### Enable a Streams instance for governance
Governance occurs at the instance level.  An instnace is enabled for governance by setting two instance properties and setting the userid and password for the IGC.  These credentials are used by the instance to register Streamns applications and lineage flows.

1. Set the instance properties using either the Streams console or streamtool.
   * *governanceEnabled* -- set this to true
   * *governanceUrl* -- *_`https://<host>:<port>`_* of the governance server
2. Set the credentials for the instance using streamtool.

*_`streamtool setigcadminconfig -d <domain> -i <instance> --igc-admin-user <userid> --igc-admin-password <password>`_*


### Recompile applications
In order for operators to register flow information for lineage  compiler.  IF you submit an application without recompiling the application will register but there will not be any flow information recorded.

#### Operators supporting governance
The following operators regsiter flow information for lineage:
* FileSource, FileSink, DirectoryScan -- mapped to core catalog asset types data`_`files and data`_`folders
* ODBC operators -- mapped to core asset type database 
* Import, Export -- these are mapped to Import Streams and Export Streams and will show lineage between Streams applications.
* Kafka operators -- mapped to Streams-KafkaTopic
* MQTT operators -- mapped to Streams-MQTT
* JMS operators -- mapped to Streams-JMS 
* HDFS2FileSource, HDFS2FileSink -- mapped to Streams-HDFSFile
This list may be expanded in the future.

### Submit applications to governed instance
Submitting an application to a governed instance will result in a Streams application being created in the governance catalog.  Supported operators will automatically register flow information for lineage.  Cancelling an applicaiton will update the Streams application execution information with the cancel time.

Each time an application is submitted a new Streams application will be created using the following naming pattern:
*`<application name>--<submit time stamp>`*

### Viewing Streams Assets in the Information Governance Catalog
You can browse the Streams applications in the IGC.  

#### Streams application
Opening a Streams application will show:
* image == you can edit the Streams application and then upload an image for this application.  Typically this would either be a screen shot of the application graph but it could be any image.
* execution details -- this includes submit time, submission time values etc..
* input Streams
* output streams

#### Lineage
Lineage reports are available for Streams applications.  Just press the generate lineage report button for an asset in the IGC.  
#### Using Search
Use search to find Streams assets in the IGC.  For example to see all of the job submitted on a specific date fill out the seatch dialog as shown below.

### Using governed assets in Streams applications
You can alos use assets in the IGC during construction of a Streams application.  The Streams Studio graphical editor has been extended to show IGC assets in the palette and these can be dragged and dropped into the graph and code will be generated.  For example, dragging a data base table will generate an ODBCSource operator, the output port schema and the connections.xml document for the operator.

#### Add catalog to Streams Explorer
1. right click on Streams explorer and Add Catalog
2. provide catalog URL 

The catalog will be added to Streams explorer.

#### Drag and Drop catalog assets
The Streams Studio graphical editor palette will contain all catalogs defined to Streams explorer.  Expand the catalog to see the assets available.  The first time you expand a catalog you may be prompted for credentials to log into the catalog.
Hovering on the palette assets may show more information.  For instance hovering on a data table will show the columns for that table.

To use an asset just drag from the palette and drop it in th canvas.  The code will be generated.  You may have to edit the operator to provide additional information.
#### Create new assets in the catalog
We also support generating new assets in the governance catalog for Streams specific assets.  To add a new asset to the catalog:
1. right click on the operator node in the graph
2. from the menu select Add operator to catalog

The operator will be added to the catalog with the information available in the editor.  You may want to edit the asset from within the catalog to provide more information.
### More Information
