---
layout: samples
title: 099_consistent_region_java_10
---

### 099_consistent_region_java_10

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/098_consistent_region_java_09_com_acme_test_ConsistentRegion9_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/103_view_annotation_at_work_com_acme_test_ViewAnnotationAtWork_spl/"> > </a>
</div>

~~~~~~
/* 
==========================================================================
Copyright (C) 2014-2015, International Business Machines Corporation
All Rights Reserved                                                 

This is one of many examples included in the "SPL Examples for
Beginners" collection to show the use of the consistent region feature
built into Streams 4.x and higher versions.

This particular example shows how a Java primitive operator can play a role inside a
consistent region. Please look at the Java operator code
inside the impl/java/src sub-directory in this SPL project. There are certain callback
functions that the Java operator developer needs to implement the checkpoint and restore
state events. This example simulates the operator failure by 
aborting one of the operators in the flow graph automatically when the application is 
in the middle of executing the logic. By doing that, the core fault tolerance feature of
the consistent region will get triggered to recover from a failure that occurred in an 
application graph. It will prove that the tuples will not be missed and the application state
kept inside this Java operator will be preserved during the course of the
unexpected operator failure and the subsequent recovery/restoration.

Initial Streams setup needed before running this example
---------------------------------------------------------
To use the consistent region feature, one must run the application in the
Distributed mode. Before that, certain configuration needs to be completed;
i.e. Streams checkpoint back-end related properties must be set. One can use
the file system or an external Redis infrastructure as a checkpoint back-end.
In this example, we will use the filesystem by setting the following
Streams instance properties:

streamtool setproperty instance.checkpointRepository=fileSystem -d <YOUR_DOMAIN_ID> -i <YOUR_INSTANCE_ID>
streamtool setproperty instance.checkpointRepositoryConfiguration={\"Dir\":\"/your/checkpoint/directory/here/\"}

Resolving Java errors you may see after importing this project
--------------------------------------------------------------
For this particular project, if you right click on this project
in Eclipse and select Properties, a dialog box will open up.
In that, click on "Java Build Path" in the left navigation bar.
On the right hand side, select the "Libraries" tab and you will
have to ensure that the following two required JAR files are added to this project.
If not, you have to add them using the "Add External Jars" button.
If they are already added and if they point to a different Streams installation
directory than yours, you have to delete them and add them fresh from your
Streams installation directory.
Those JAR files are added from the Streams installation directory.
i.e. $STREAMS_INSTALL/<STREAMS_VERSION>/lib

1) $STREAMS_INSTALL/<STREAMS_VERSION>/lib/com.ibm.streams.operator.jar
2) $STREAMS_INSTALL/<STREAMS_VERSION>/lib/com.ibm.streams.operator.samples.jar

Compile and Run
---------------
1) You can either compile this application inside the Streams Studio or from a Linux
   terminal window via the sc (Streams compiler) command.
 
2) You can launch from Streams Studio or submit via the streamtool command.
   In the resulting output file in the data directory (results.txt) will show you
   that there is no gap in the results. If that is the case , then the
   consistent region feature worked correctly during and after the forced
   crash of this application.
==========================================================================
*/
namespace com.acme.test;

composite ConsistentRegion10 {
	graph
		// JobControlPlane operator is mandatory in applications with consistent regions.
		// Simply include it anywhere in your application graph.
		() as JCP = JobControlPlane() {}
		
		// We are going to declare a consistent region for this entire application graph.
		@consistent(trigger=periodic, period=0.500)
		stream<int32 x, int32 y, rstring operation> CalcRequest = FileSource() {
			param
				initDelay: 4.0;
				file: "requests.txt";
				format: csv;
				hasDelayField: true;
				hasHeaderLine: true;
		}
		
		// This Java primitive operator has code to forcefully abort itself on
		// receiving the 21st tuple. It should recover from that failure and 
		// continue smoothly to complete all the calculation requests without
		// missing out on anything.
		stream<int32 sequence, int32 x, int32 y, rstring operation, int32 result> CalcResponse = JavaCalculator(CalcRequest) {
		}
		
		() as MySink1 = FileSink(CalcResponse) {
			param
				file: "results.txt";
				flush: 1u;
		}
		
		/*
		// This is a sink used for debugging purposes.
		// It will record in this file all the consistent region events as they occur.
		() as AnotherSink = FileSink(CalcRequest) {
		  param
		    file: "allTuples.txt";
		    truncateOnReset: false;
		    writeStateHandlerCallbacks: true;
		    writePunctuations: true;
		    flush: 1u;
		}
		*/
}

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/098_consistent_region_java_09_com_acme_test_ConsistentRegion9_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/103_view_annotation_at_work_com_acme_test_ViewAnnotationAtWork_spl/"> > </a>
</div>

