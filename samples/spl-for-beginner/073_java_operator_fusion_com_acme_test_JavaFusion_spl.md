---
layout: samples
title: 073_java_operator_fusion
---

### 073_java_operator_fusion

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/072_using_streams_rest_apis_com_acme_test_UsingStreamsRestApis_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/074_user_defined_parallelism_01_com_acme_test_UDP1_spl/"> > </a>
</div>

~~~~~~
/*
This simple example shows two Java operators working fine after being fused together.
The first Java operator is a sink operator and it runs for a long time with a time
consuming task. We simulate that by sleeping inside that operator forever.
The second Java operator receives and forwards that same tuple.

This situation was used by one of the Streams customers. Hence, this example is added
to this beginner collection as a quick reference for other users.

Refer to the Java operator code in the impl/java/src directory.
*/
namespace com.acme.test;

composite JavaFusion {
	graph
		stream<int32 x> Test1 = Beacon() {
			param
				iterations: 1;
		}
		
		
		// Fuse this Beacon, FirstJavaOp, and SecondJavaOp all into a single PE.
		stream<int32 y> Test2 = Beacon() {
			param
				iterations: 1;
				
			config
				placement: partitionColocation("JavaOpFusion");
		}
		
		() as JavaSink = FirstJavaOp(Test2) {
			config
				placement: partitionColocation("JavaOpFusion");
		}
		
		stream<Test1> MyStream = SecondJavaOp(Test1) {
			config
				placement: partitionColocation("JavaOpFusion");
		}
		
		() as Sink1 = FileSink(MyStream) {
			param
				file: "Test1.csv";
		}
}

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/072_using_streams_rest_apis_com_acme_test_UsingStreamsRestApis_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/074_user_defined_parallelism_01_com_acme_test_UDP1_spl/"> > </a>
</div>

