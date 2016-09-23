---
layout: samples
title: 053_java_primitive_operator_with_complex_output_tuple_types
---

### 053_java_primitive_operator_with_complex_output_tuple_types

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/052_streams_to_python_python_wrapper_example_streams_to_python_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/054_serialize_deserialize_tuples_com_acme_test_serialize_deserialize_tuples_spl/"> > </a>
</div>

~~~~~~
/*
This example shows how a Java primitive operator is created from scratch.
In addition, this example shows how we can create a complex output tuple
inside the Java primitive operator and then submit that tuple.

As a bonus, this application can also show how one can write to the Streams
PE trace and PE log files from the Java primitive operator using the Java APIs.

[THIS EXAMPLE HAS A COMPANION JAVA PROJECT NAMED Java_Complex_Type_Submission.]
*/
namespace com.acme.test;
use com.acme.complex.otuple.submission::*;

/*
Some Tips:
 
1) You can open the Java Operator model file in the com.acme.complex.otuple.submission
sub-directory located in the main project directory of this application and browse that
XML file using the operator model editor. It will show you how this Java primitive
operator is configured.
 
2) You also have to build the companion Java project Java_Complex_Tuple_Type_Submission by
switching to the Eclipse Java perspective. The Java source for the business logic 
code can be found in that Java project. In the SPL-Examples-For-Beginners package you 
downloaded, that Java project may have been built already. If that is true, then you
need not build the Java project. If it is not already built, then go ahead and build that
Java project. Once that Java Project is built, copy the ComplexTupleTypeSubmission.class from there to 
this current (053_XXXX) SPL project's impl/java/bin directory with its
full Java package name (i.e. impl/java/bin/com/acme/complex/tuple/type/submission/ComplexTupleTypeSubmission.class)
*/
composite java_primitive_operator_with_complex_output_tuple_types {
	type
		SnapshotData_t = ustring ric, map<ustring, float64> dblMap, map<ustring, ustring> strMap;
		SnapshotResponse_t = list<SnapshotData_t> responses; 
		TestInputData_t = int32 dummyInt, rstring dummyString, list<int32> dummyIntList;
		
	graph
		// Generate two three tuples via Beacon.
		stream<int32 dummyInt> DummySignal = Beacon() {
			param
				iterations: 3;
				initDelay: 3.0;
		}
		
		
		stream<TestInputData_t> TestInputData = Custom(DummySignal) {
			logic
				state: {
					mutable int32 _cnt = 0;
					mutable list<int32> _dummyInt = [21, 44, 203];
					mutable list<rstring> _dummyString = 
						["Focus on peace", "Work hard and play hard", "Think and act wisely"];
					mutable list<list<int32>> _dummyIntList= 
						[[64, 85, 90, 92, 95], [164, 185, 190, 192, 195], [264, 285, 290, 292, 295]];
					mutable TestInputData _testInputData = {};
				}
				
				onTuple DummySignal: {
					_testInputData.dummyInt = _dummyInt[_cnt];
					_testInputData.dummyString = _dummyString[_cnt];
					_testInputData.dummyIntList = _dummyIntList[_cnt];
					
					if (++_cnt == 3) {
						_cnt = 0;
					}

					// We will generate this output tuple so that Java primitive operator can receive an
					// input tuple with two primitive typed attributes and one collection typed attribute.					
					submit(_testInputData, TestInputData);
				}
		}
		
		// Invoke the Java operator that will output a tuple with complex data types.
		stream<SnapshotResponse_t> Response = JavaPrimitiveWithComplexOutputTupleSubmission(TestInputData) {
		}
		
		// Capture the output tuple from the Java primitive operator and print it on the screen.
		() as MySink = Custom(Response) {
			logic
				onTuple Response: {
					printStringLn("Response from the Java primitive operator=" + (rstring)Response);
				}
		}
}

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/052_streams_to_python_python_wrapper_example_streams_to_python_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/054_serialize_deserialize_tuples_com_acme_test_serialize_deserialize_tuples_spl/"> > </a>
</div>

