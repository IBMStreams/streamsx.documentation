---
layout: samples
title: 091_consistent_region_spl_02
---

### 091_consistent_region_spl_02

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/090_consistent_region_spl_01_com_acme_test_ConsistentRegion1_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/092_consistent_region_spl_03_com_acme_test_ConsistentRegion3_spl/"> > </a>
</div>

~~~~~~
/* 
==========================================================================
Copyright (C) 2014-2015, International Business Machines Corporation
All Rights Reserved                                                 

This is one of many examples included in the "SPL Examples for
Beginners" collection to show the use of the consistent region feature
built into Streams 4.x and higher versions. This particular example was
written by my colleague Gabriela Jacques da Silva and full credit goes to her. 

This particular example shows how every single SPL based operator in an application
graph will take part in the consistent region. This example simulates the operator
failure by aborting that operator automatically when the application is
in the middle of executing the logic. By doing that, the core fault tolerance
feature of the consistent region will get triggered to recover from a
failure that occurred in an application graph. It will prove that the
tuples will not be missed and the local operator state will not be
compromised during the course of the unexpected operator failure and the
subsequent recovery/restoration. 


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
   gap in the joined pairs of odd and even numbers. If that is the case , then the
   consistent region feature worked correctly during and after the forced
   crash of this application.
==========================================================================
*/
namespace com.acme.test;

composite ConsistentRegion2 {
	graph
		// JobControlPlane operator is mandatory in applications with consistent regions.
		// Simply include it anywhere in your application graph.
		() as JCP = JobControlPlane() {}

		// Configures an operator-driven consistent region. In this example, 
		// the Beacon operator is the start of the consistent region. Beacon
		// starts the establishment of a consistent state based on the triggerCount
		// parameter which was added starting in Streams 4.x.
		// In this case, it is configured to establish a consistent
		// state at every 20000 tuples. 
		//
		// IMPORTANT: In an operator driven consistent region, there can be
		// only one source operator.
		@consistent(trigger=operatorDriven)
		stream<uint64 id> Beat = Beacon() {
			param
				iterations: 500000;
				// This is a required parameter for Beacon when it is the start operator in a
				// consistent region with a trigger type of operatorDriven.
				triggerCount: 20000u;
				initDelay: 5.0;

			output
				Beat: id = IterationCount();
    	}
    	
		// Discard any odd tuple. Count the number of even tuples, and submit
		// the input tuple together with the current number of processed tuples.
		// If the PE crashes, and the operator is not in a consistent region,
		// the current value of 'count' is lost. If the operator is in a consistent
		// region, the value of 'count' is restored to the value it had at the last
		// successfully established consistent state. 
		stream<uint64 id, uint64 counter> Even = Functor(Beat) {
			logic
				state: {
					mutable uint64 count = 0ul;
				}
				
			param
				// Throw away the odd numbered tuples and process only the even numbered tuples.
				filter : (id % 2ul) == 0ul;

			output
				Even: id = Beat.id, counter = count++; 

			config
				placement: partitionColocation("fused");
		}   	

		// When processing tuple with id 123456, abort. This emulates a transient
		// error while processing a tuple. We simulate a transient error by executing
		// the abort function only when the relaunch count of the PE is 0. 
		stream<Even> CrashEven = Custom(Even) {
			logic
				onTuple Even: {
					if (id == 123456ul && getRelaunchCount() == 0u) {
            			abort();
          			}  
          		
          			submit(Even, CrashEven); 
        		}
        	
      		config
        	placement: partitionColocation("fused");
    	}

		// Same as the Functor above, but passing on Odd numbers.
		stream<uint64 id, uint64 counter> Odd = Functor(Beat) {
			logic
				state: {
					mutable uint64 count = 0ul;
				}
				
			param
				// Throw away the even numbered tuples and process only the odd numbered tuples.
				filter: (id % 2ul) == 1ul;
				
      		output
      			Odd: id = Beat.id, counter = count++; 
    	}
    	
		stream<Odd> PassOddThrough = Custom(Odd) {
			logic
				onTuple Odd: {
					submit(Odd, PassOddThrough);
				}
		}

		// Barrier Joining both Odd and Even Streams. 
		stream<uint64 evenId, uint64 evenCounter, uint64 oddId, uint64 oddCounter> JoinedStreams = 
			Barrier(CrashEven as I1; PassOddThrough as I2) {
				output
					JoinedStreams: evenId = I1.id, evenCounter = I1.counter, 
						oddId = I2.id, oddCounter = I2.counter;
    	} 

		() as FS = FileSink(JoinedStreams) {
			param
				file: "joined.txt";
		}     	    	
}
~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/090_consistent_region_spl_01_com_acme_test_ConsistentRegion1_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/092_consistent_region_spl_03_com_acme_test_ConsistentRegion3_spl/"> > </a>
</div>

