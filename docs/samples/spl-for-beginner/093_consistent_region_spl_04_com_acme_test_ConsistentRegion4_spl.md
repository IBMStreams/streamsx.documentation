---
layout: samples
title: 093_consistent_region_spl_04
---

### 093_consistent_region_spl_04

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/092_consistent_region_spl_03_com_acme_test_ConsistentRegion3_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/094_consistent_region_spl_05_com_acme_test_ConsistentRegion5_spl/"> > </a>
</div>

~~~~~~
/* 
==========================================================================
Copyright (C) 2014-2015, International Business Machines Corporation
All Rights Reserved                                                 

This is one of many examples included in the "SPL Examples for
Beginners" collection to show the use of the consistent region feature
built into Streams 4.x and higher versions.

This particular example shows how every single SPL based operator in an application
graph will take part in the consistent region. This example simulates the operator
failure by aborting two different operators automatically when the application is
in the middle of executing the logic. In addition, this application has two
different consistent regions defined at two composites with the same reachability point.
By doing that, the core fault tolerance feature of the consistent region will get
triggered to recover from a failure that occurred in an application graph.
It will prove that the tuples will not be missed and the Join operator's window state will not
be compromised during the course of the unexpected operator failure and the
subsequent recovery/restoration. [Please note that this example will take about 40 seconds to
produce the full results that you can verify.]

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

Compile and Run
---------------
1) You can either compile this application inside the Streams Studio or from a Linux
   terminal window via the sc (Streams compiler) command.
 
2) You can launch from Streams Studio or submit via the streamtool command.
   In the resulting output file in the data directory will show you that there is no
   gap in the joined pairs of the data. If that is the case , then the
   consistent region feature worked correctly during and after the forced
   crash of this application.
==========================================================================
*/
namespace com.acme.test;

composite ConsistentRegion4 {
	graph
		// JobControlPlane operator is mandatory in applications with consistent regions.
		// Simply include it anywhere in your application graph.
		() as JCP = JobControlPlane() {}
		
		// We are going to invoke two composites here which have their own consistency regions.
		// These composites act as sources for this application.
		stream<int32 i, rstring str> MsgA = Test1() {
		}
		
		// We will crash this operator once when the tuple attribute value is 15.
		stream<MsgA> StreamA = Custom(MsgA) {
			logic
				onTuple MsgA: {
					if ((MsgA.i == 15) && (getRelaunchCount() == 0u)) {
						abort();
					} else {
						submit(MsgA, StreamA);
					}
				}
		}

		// Invoke the second composite.
		stream<int32 i, rstring str> MsgB = Test2() {
		}
		
		// We will crash this operator once when the tuple attribute value is 25.
		stream<MsgB> StreamB = Custom(MsgB) {
			logic
				onTuple MsgB: {
					if ((MsgB.i == 25) && (getRelaunchCount() == 0u)) {
						abort();
					} else {
						submit(MsgB, StreamB);
					}
				}
		}
		
		// Let us now join those two streams.
		stream<int32 ai, rstring astring, int32 bi, rstring bstring> JoinedStream =  Join(StreamA; StreamB) {
			window
				StreamA: sliding, count(10000);
				StreamB: sliding, count(10000);
			
				param
					match: StreamA.i == StreamB.i;			
				
				output
					JoinedStream: ai = StreamA.i, astring = StreamA.str, bi = StreamB.i, bstring = StreamB.str;
		}
		
		() as MySink1 = FileSink(JoinedStream) {
			param
				file: "result.txt";
				flush: 1u;
		}
}


composite Test1(output A) {
	graph
		// Starting a consistent region from a source operator is an ideal thing to do.
		@consistent(trigger=periodic, period=0.25)
		stream<int32 i> SourceA = Beacon() {
			param
				iterations: 30;
				period: 1.0;
				initDelay: 3.0;
				
			output
				SourceA: i = (int32)IterationCount() + 1;
		}
		
		
		stream<int32 i, rstring str> A = Custom(SourceA) {
			logic
				onTuple SourceA: {
					mutable A oTuple = {};
					oTuple.i = SourceA.i;
					oTuple.str = "A" + (rstring)SourceA.i;
					submit(oTuple, A); 
				}
		}
}

composite Test2(output B) {
	graph
		@consistent(trigger=periodic, period=0.25)
		stream<int32 i> SourceB = Beacon() {
			param
				iterations: 30;
				period: 1.0;
				initDelay: 3.0;
				
			output
				SourceB: i = (int32)IterationCount() + 1;
		}
		
		
		stream<int32 i, rstring str> B = Custom(SourceB) {
			logic
				onTuple SourceB: {
					mutable B oTuple = {};
					oTuple.i = SourceB.i;
					oTuple.str = "B" + (rstring)SourceB.i;
					submit(oTuple, B); 
				}
		}
}
~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/092_consistent_region_spl_03_com_acme_test_ConsistentRegion3_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/094_consistent_region_spl_05_com_acme_test_ConsistentRegion5_spl/"> > </a>
</div>

