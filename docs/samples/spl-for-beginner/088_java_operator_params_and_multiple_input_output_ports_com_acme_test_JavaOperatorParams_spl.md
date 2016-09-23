---
layout: samples
title: 088_java_operator_params_and_multiple_input_output_ports
---

### 088_java_operator_params_and_multiple_input_output_ports

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/087_email_alerts_via_java_native_function_com_acme_test_EmailAlerts_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/089_integrating_streams_apps_with_web_apps_com_acme_test_WebCalculator_spl/"> > </a>
</div>

~~~~~~
/*
This example demonstrates the following three features of the Streams Java primitive operator framework.

1) Invoking a Java operator with operator parameters in the param clause.
2) Processing tuples inside a Java operator arriving from multiple input ports.
3) As a bonus, it shows a way to populate a complex output tuple containing other nested tuple structures.
   [There is another example 053_java_primitive_operator_with_complex_output_tuple_types which
    shows a different technique to achieve a similar task. But, the method shown below in this
    example is a better one to follow.]
*/
namespace com.acme.test;

composite Java_Operator_Params {
	type
		// We will use the following nested tuple structure with user defined tuple types to demonstrate the feature #3 mentioned above in the comments.
		CrewDutyTimeType = CrewInfoType, tuple<int32 dutyTimeMinutes>;
		CrewInfoType = tuple<rstring employeeNumber, rstring firstName, rstring lastName, rstring middleInitial, rstring crewBase, list<CrewSequenceType> sequences>;
		CrewSequenceType = tuple<boolean isDomestic, rstring sequencePosition, rstring sequenceKey, rstring originDate, list<CrewDutyPeriodType> dutyPeriods>;
		CrewDutyPeriodType = tuple<rstring dutyPeriodStartDateGMT, rstring dutyPeriodEndDateGMT, list<FlightPairingType> pairings>;
		FlightPairingType = tuple<rstring flightNumber, rstring originAirport, rstring destinationAirport>;
	
	graph
		// Let us define three different Beacon operators to generate the required input
		// streams for the three input ports we will have in the Java operator.
		stream<int32 i> IntInput = Beacon() {
			param
				iterations: 4u;
		}
		
		stream<float32 f> FloatInput = Beacon() {
			param
				iterations: 4u;
		}		
	
		stream<int32 dummy> DummyInput = Beacon() {
			param
				iterations: 1u;
		}
		
		// Invoke the Java primitive operator with operator parameters and its three
		// different input ports. This operator will also produce, three different
		// output streams which we will capture and display on the screen.
		// [Refer to the Java source code in the impl/src/java sub-directory of this SPL project.]
		(stream<IntInput> O1; stream<FloatInput> O2; stream<CrewDutyTimeType> O3) = MyJavaOp(IntInput; FloatInput; DummyInput) {
			param
				floatVal: (float32)6.67;
				intVal: 45;
		}				
		
		() as Sink1 = FileSink(O1) {
			param
				file: "/dev/stdout";
				flush: 1u;
		}
		
		() as Sink2 = FileSink(O2) {
			param
				file: "/dev/stdout";
				flush: 1u;
		}		
		
		() as Sink3 = FileSink(O3) {
			param
				file: "/dev/stdout";
				flush: 1u;
		}		
}
~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/087_email_alerts_via_java_native_function_com_acme_test_EmailAlerts_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/089_integrating_streams_apps_with_web_apps_com_acme_test_WebCalculator_spl/"> > </a>
</div>

