---
layout: samples
title: 074_user_defined_parallelism_01
---

### 074_user_defined_parallelism_01

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/073_java_operator_fusion_com_acme_test_JavaFusion_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/075_user_defined_parallelism_02_com_acme_test_UDP2_spl/"> > </a>
</div>

~~~~~~
/*
This is example 1 in the series of 12 User Defined Parallelism (UDP) scenarios.
UDP is a great feature to parallelize an entire composite or a particular operator.

This example code is taken from the Streams InfoCenter and added here to benefit the
beginners of the Streams SPL programming model. Many thanks to our Streams colleague
Scott Schneider for coming up with this set of UDP examples. Full credit goes to him.

It is recommended that you run this example in Distributed mode and visualize the
parallel region in the Streams instance graph.
*/

namespace com.acme.test;

// Replication is done in this UDP scenario where every operator runs on its own PE. (non-fused)

composite UDP1 {
	graph
		stream<int32 i> MyData = Beacon() {
			param
				iterations: 5000; 
		}

		stream<MyData> EnrichedData = Custom(MyData) {
			logic
				state: {
					mutable int32 _i = 0;
				}
				
				onTuple MyData: {
					_i++;
					MyData.i = _i;
					submit(MyData, EnrichedData);
				}
		}
		
		// Create 5 parallel copies of the following Custom operator.
		@parallel (width=5)
		stream<MyData> TransformedData = Custom(EnrichedData) {
			logic
				onTuple EnrichedData: {
					EnrichedData.i = EnrichedData.i + 50;
					submit(EnrichedData, TransformedData);
				}
		}
		
		
		() as MySink = FileSink(TransformedData) {
			param
				file: "Test1.csv";
		}
		
}

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/073_java_operator_fusion_com_acme_test_JavaFusion_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/075_user_defined_parallelism_02_com_acme_test_UDP2_spl/"> > </a>
</div>

