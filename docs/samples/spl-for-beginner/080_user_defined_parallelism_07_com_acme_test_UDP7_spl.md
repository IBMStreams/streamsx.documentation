---
layout: samples
title: 080_user_defined_parallelism_07
---

### 080_user_defined_parallelism_07

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/079_user_defined_parallelism_06_com_acme_test_UDP6_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/081_user_defined_parallelism_08_com_acme_test_UDP8_spl/"> > </a>
</div>

~~~~~~
/*
This is example 7 in the series of 12 User Defined Parallelism (UDP) scenarios.
UDP is a great feature to parallelize an entire composite or a particular operator.

This example code is taken from the Streams InfoCenter and added here to benefit the
beginners of the Streams SPL programming model. Many thanks to our Streams colleague
Scott Schneider for coming up with this set of UDP examples. Full credit goes to him.

It is recommended that you run this example in Distributed mode and visualize the
parallel region in the Streams instance graph.
*/
namespace com.acme.test;

// In this example of user-defined parallelism, the processing element (PE) and operator graph
// illustrate the logical combination of the graphs in Examples 2 and 3. The fusion constraints
// place the Src operator in the same PE as the first parallel region (SrcAB), and outside the PE
// of the second parallel region (CD). 

composite UDP7 {
	graph
		stream<int32 i> MyData = Beacon() {
			param
				iterations: 5000; 
			
			config
				placement: partitionColocation("SrcAB");	
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
				
			config
				placement: partitionColocation("SrcAB");
		}
		
		// Create two parallel copies of the Comp7 composite.
		@parallel (width=2)
		stream<EnrichedData> TransformedData1 = Comp7_1(EnrichedData) {
			config
				placement: partitionColocation("SrcAB");
		}

		@parallel (width=2)
		stream<EnrichedData> TransformedData2 = Comp7_2(EnrichedData) {
			config
				placement: partitionColocation("CD");
		}
		
		() as MySink = FileSink(TransformedData1, TransformedData2) {
			param
				file: "Test1.csv";
		}		
}


composite Comp7_1(input In; output B) {
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


composite Comp7_2(input In; output D) {
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

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/079_user_defined_parallelism_06_com_acme_test_UDP6_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/081_user_defined_parallelism_08_com_acme_test_UDP8_spl/"> > </a>
</div>

