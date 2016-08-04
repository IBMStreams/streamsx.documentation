---
layout: samples
title: 085_user_defined_parallelism_12
---

### 085_user_defined_parallelism_12

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/084_user_defined_parallelism_11_com_acme_test_UDP11_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/086_jms_source_sink_using_activemq_com_acme_test_JMSSourceSink_spl/"> > </a>
</div>

~~~~~~
/*
This is example 12 in the series of 12 User Defined Parallelism (UDP) scenarios.
UDP is a great feature to parallelize an entire composite or a particular operator.

This example code is taken from the Streams InfoCenter and added here to benefit the
beginners of the Streams SPL programming model. Many thanks to our Streams colleague
Scott Schneider for coming up with this set of UDP examples. Full credit goes to him.

It is recommended that you run this example in Distributed mode and visualize the
parallel region in the Streams instance graph.
*/
namespace com.acme.test;

// In this example of user-defined parallelism, sibling operators exist in a parallel region,
// and the Src operator is fused from outside the parallel region with operators that are
// inside the parallel region. This example is similar to Example 11 except that the Src operator,
// which is outside the parallel region, is fused with operators A and B from inside the parallel
// region. Because the Src, A, and B operators are in the same PE, the parallel transformation
// does not replicate the PE, but does replicate operators A and B. Operator C is in a different PE.
// The parallel transformation for that PE also replicates the PE.

composite UDP12 {
	graph
		stream<int32 i> MyData = Beacon() {
			param
				iterations: 5000; 

			config
				placement: partitionColocation("AB");				
		}

		// Create two parallel copies of the composite Comp12.
		@parallel (width=2)
		stream<MyData> TransformedData = Comp12(MyData) {
		}	
		
		() as MySink = FileSink(TransformedData) {
			param
				file: "Test1.csv";
		}					
}


composite Comp12(input In; output C) {
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

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/084_user_defined_parallelism_11_com_acme_test_UDP11_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/086_jms_source_sink_using_activemq_com_acme_test_JMSSourceSink_spl/"> > </a>
</div>

