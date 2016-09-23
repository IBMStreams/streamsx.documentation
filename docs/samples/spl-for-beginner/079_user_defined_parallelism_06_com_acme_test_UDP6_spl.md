---
layout: samples
title: 079_user_defined_parallelism_06
---

### 079_user_defined_parallelism_06

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/078_user_defined_parallelism_05_com_acme_test_UDP5_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/080_user_defined_parallelism_07_com_acme_test_UDP7_spl/"> > </a>
</div>

~~~~~~
/*
This is example 6 in the series of 12 User Defined Parallelism (UDP) scenarios.
UDP is a great feature to parallelize an entire composite or a particular operator.

This example code is taken from the Streams InfoCenter and added here to benefit the
beginners of the Streams SPL programming model. Many thanks to our Streams colleague
Scott Schneider for coming up with this set of UDP examples. Full credit goes to him.

It is recommended that you run this example in Distributed mode and visualize the
parallel region in the Streams instance graph.
*/
namespace com.acme.test;

// In this example of user-defined parallelism, one stream feeds multiple parallel regions.
// Each parallel region needs an independent splitter. In this instance, the parallel transformation adds
// two independent splitters to a single PE output port. Each of these splitters feeds one of the two independent parallel regions.

composite UDP6 {
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
		
		// Create two parallel copies of the composite Comp6.
		@parallel (width=2)
		stream<EnrichedData> TransformedData1 = Comp6_1(EnrichedData) {
			config
				placement: partitionColocation("AB");
		}

		@parallel (width=2)
		stream<EnrichedData> TransformedData2 = Comp6_2(EnrichedData) {
			config
				placement: partitionColocation("CD");
		}
		
		() as MySink = FileSink(TransformedData1, TransformedData2) {
			param
				file: "Test1.csv";
		}		
}


composite Comp6_1(input In; output B) {
	graph
		stream<int32 i> A = Custom(In) {
			logic
				onTuple In: {
					In.i = In.i + 25;
					submit(In, A);
				}
		}
		
		stream<A> B = Custom(A) {
			logic
				onTuple A: {
					A.i = A.i - 4;
					submit(A, B);
				}
		}
}


composite Comp6_2(input In; output D) {
	graph
		stream<int32 i> C = Custom(In) {
			logic
				onTuple In: {
					In.i = In.i + 45;
					submit(In, C);
				}
		}
		
		stream<C> D = Custom(C) {
			logic
				onTuple C: {
					C.i = C.i - 8;
					submit(C, D);
				}
		}
}
~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/078_user_defined_parallelism_05_com_acme_test_UDP5_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/080_user_defined_parallelism_07_com_acme_test_UDP7_spl/"> > </a>
</div>

