---
layout: samples
title: 084_user_defined_parallelism_11
---

### 084_user_defined_parallelism_11

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/083_user_defined_parallelism_10_com_acme_test_UDP10_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/085_user_defined_parallelism_12_com_acme_test_UDP12_spl/"> > </a>
</div>

~~~~~~
/*
This is example 11 in the series of 12 User Defined Parallelism (UDP) scenarios.
UDP is a great feature to parallelize an entire composite or a particular operator.

This example code is taken from the Streams InfoCenter and added here to benefit the
beginners of the Streams SPL programming model. Many thanks to our Streams colleague
Scott Schneider for coming up with this set of UDP examples. Full credit goes to him.

It is recommended that you run this example in Distributed mode and visualize the
parallel region in the Streams instance graph.
*/
namespace com.acme.test;

// In this example of user-defined parallelism, sibling operators exist in a parallel region.
// For parallel transformations, the sibling operators in a parallel region must be in
// either the same PE or in different PEs. This requirement implies that the
// non-sibling operators in a parallel region can be in different PEs.

composite UDP11 {
	graph
		stream<int32 i> MyData = Beacon() {
			param
				iterations: 5000; 
		}

		// Create 2 parallel versions of the composite Comp11.
		@parallel (width=2)
		stream<MyData> TransformedData = Comp11(MyData) {
		}	
		
		() as MySink = FileSink(TransformedData) {
			param
				file: "Test1.csv";
		}					
}


composite Comp11(input In; output C) {
	graph
		stream<int32 i> A = Custom(In) {
			logic
				state: {
					mutable int32 _i = 0;
				}
				
				onTuple In: {
					_i++;
					In.i = _i;
					submit(In, A);
				}
				
			config
				placement: partitionColocation("AB");		
		}
		
		stream<A> B = Custom(A) {
			logic
				onTuple A: {
					A.i = A.i + 14;
					submit(A, B);
				}

			config
				placement: partitionColocation("AB");				
		}
		
		stream<A> C = Custom(B) {
			logic
				onTuple B: {
					B.i = B.i - 10;
					submit(B, C);
				}

			config
				placement: partitionColocation("C");				
		}		
}

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/083_user_defined_parallelism_10_com_acme_test_UDP10_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/085_user_defined_parallelism_12_com_acme_test_UDP12_spl/"> > </a>
</div>

