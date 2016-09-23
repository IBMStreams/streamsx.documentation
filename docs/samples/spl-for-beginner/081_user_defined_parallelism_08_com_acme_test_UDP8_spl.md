---
layout: samples
title: 081_user_defined_parallelism_08
---

### 081_user_defined_parallelism_08

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/080_user_defined_parallelism_07_com_acme_test_UDP7_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/082_user_defined_parallelism_09_com_acme_test_UDP9_spl/"> > </a>
</div>

~~~~~~
/*
This is example 8 in the series of 12 User Defined Parallelism (UDP) scenarios.
UDP is a great feature to parallelize an entire composite or a particular operator.

This example code is taken from the Streams InfoCenter and added here to benefit the
beginners of the Streams SPL programming model. Many thanks to our Streams colleague
Scott Schneider for coming up with this set of UDP examples. Full credit goes to him.

It is recommended that you run this example in Distributed mode and visualize the
parallel region in the Streams instance graph.
*/
namespace com.acme.test;

// In this example of user-defined parallelism, no operators from outside the parallel region are fused 
// with the operators in the parallel region. The parallel region has no incoming streams.
// The processing element (PE) is replicated because no operators from outside the parallel region are 
// fused with the operators in the parallel region. Each replicated PE happens to contain a Source operator.
// If you want to divide the data that each source handles, you must invoke the Source operators in a way that divides the data.

composite UDP8 {
	graph
		// Create two parallel copies of the composite Comp8.
		@parallel (width=2)
		stream<int32 i> TransformedData = Comp8() {
			config
				placement: partitionColocation("SrcA");
		}

		() as MySink = FileSink(TransformedData) {
			param
				file: "Test1.csv";
		}		
}


composite Comp8(output A) {
	graph
		stream<int32 i> MyData = Beacon() {
			param
				iterations: 5000; 
		}

		stream<MyData> A = Custom(MyData) {
			logic
				state: {
					mutable int32 _i = 0;
				}
				
				onTuple MyData: {
					_i++;
					MyData.i = _i;
					submit(MyData, A);
				}
		}
}

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/080_user_defined_parallelism_07_com_acme_test_UDP7_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/082_user_defined_parallelism_09_com_acme_test_UDP9_spl/"> > </a>
</div>

