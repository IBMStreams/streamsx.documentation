---
layout: samples
title: 063_on_the_fly_tuple_creation_and_encoding_decoding_in_java_primitive_operators
---

### 063_on_the_fly_tuple_creation_and_encoding_decoding_in_java_primitive_operators

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/062_data_sharing_between_non_fused_spl_custom_and_java_primitive_operators_com_acme_test_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/064_using_spl_composite_params_com_acme_test_CompositeParams_spl/"> > </a>
</div>

~~~~~~
/*
======================================================================
This example shows how to create a tuple on the fly within a 
Java primitive operator. After that it shows how to encode a
tuple into a blob and decode a blob into a tuple.
======================================================================
*/
namespace application;

composite Main {
	graph
		stream<int32 dummy> Dummy1 = Beacon() {
			param
				iterations: 1u;
		}
		
		// Invoke the Java primitive operator.
		stream<Dummy1> Dummy2 = MyJavaEncodeDecode(Dummy1) {
		}
		
		() as MySink1 = Custom(Dummy2) {
			logic
				onTuple Dummy2: {
					printStringLn("Result=" + (rstring)Dummy2);
				}
		}
}

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/062_data_sharing_between_non_fused_spl_custom_and_java_primitive_operators_com_acme_test_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/064_using_spl_composite_params_com_acme_test_CompositeParams_spl/"> > </a>
</div>

