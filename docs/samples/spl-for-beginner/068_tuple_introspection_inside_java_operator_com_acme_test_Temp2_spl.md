---
layout: samples
title: 068_tuple_introspection_inside_java_operator
---

### 068_tuple_introspection_inside_java_operator

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/067_simple_java_source_operator_com_acme_test_Temp1_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/069_changing_map_value_during_iteration_com_acme_test_ChangeCollectionValue_spl/"> > </a>
</div>

~~~~~~
/*
This example demonstrates how one can introspect tuples inside a 
Java operator and determine the type and name of the attributes
contained in that tuple.

(You will need Streams 4.x or later to run this example.)
*/
namespace com.acme.test;

composite Temp2 {
	type
		MySchema = tuple<int64 a, tuple<rstring b, float64 c, uint32 d, boolean e, list<rstring> f> g, map<rstring,float32> h>;
		
	graph
		// Generate a single tuple for our test.
		stream<MySchema> Test1 = Beacon() {
			param
				initDelay: 4.0;
				iterations: 1u;
		}

		// Invoke the Java operator that will inspect the incoming tuple
		// and print the type and name of all the tuple attributes.
		// Since we have a nested tuple, it should do it recursively.
		// (See the source code in impl/java/src directory.)
		stream<MySchema> Test2 = MyJavaOp(Test1) {
		}
		
		// This is a custom sink.
		() as Sink1 = Custom(Test2) {
			logic
				onTuple Test2: {
					// Do nothing.
				}
		}
}

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/067_simple_java_source_operator_com_acme_test_Temp1_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/069_changing_map_value_during_iteration_com_acme_test_ChangeCollectionValue_spl/"> > </a>
</div>

