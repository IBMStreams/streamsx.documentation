---
layout: samples
title: 048_source_operator_with_control_port
---

### 048_source_operator_with_control_port

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/047_streams_host_tags_at_work_host_tags_streams_host_tags_at_work_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/049_json_to_tuple_to_json_using_java_sample_Main_spl/"> > </a>
</div>

~~~~~~
/*
This example shows a way to create a C++ primitive source operator and then provide a control
input port for it. Certain classes of applications can make use of this facility to control
the kind of data a source operator generates. In addition, this example shows how to pass
one or more string literals to the C++ primitive operator as invocation time parameters. As a 
bonus, this example also shows a simple way to do performance measurement inside the SPL code using
the built-in SPL high precision timestamp functions.
*/
namespace source_op_with_control_port;

composite source_operator_with_control_port {
	graph
		
		// Send a control signal every 3 seconds.
		stream<rstring newName> ControlSignal = Beacon() {
			param
				period: 3.0;
				iterations: 1000;
				
			output
				// In order to uniquely identify the control signals, we will add the
				// current time to the control string we are using.
				ControlSignal: newName = "Mary" + (rstring)getSeconds(getTimestamp());
		}
		
		// Invoke the C++ primitive source operator (that takes a control input stream).
		// Please refer to the additional commentary at the top of the C++ primitive operator code 
		// to see how easy it is to define a control input port in Streams.
		stream<rstring name, int32 age, list<rstring> movies> PersonInfo = MyOp(ControlSignal) {
			param
				// Pass a list of string literals as an operator parameter.
				favoriteMovies: "Life of Pi", "Good Will Hunting", "The Sting", "The Bourne Identity";
		}
		
		() as Sink1 = Custom(PersonInfo) {
			logic
				onTuple PersonInfo: {
					// Let us show a simple way to time the following printStringLn code.
					mutable int64 _timeInNanoSecondsBeforeExecution = 0l;
					mutable int64 _timeInNanoSecondsAfterExecution = 0l;
					mutable timestamp _timeNow = getTimestamp();
					_timeInNanoSecondsBeforeExecution = 
						((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
					printStringLn((rstring)PersonInfo);
					_timeNow = getTimestamp();
					_timeInNanoSecondsAfterExecution = 
						((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
					mutable int64 _totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
					printStringLn("Time taken for executing printStringLn = " + 
						(rstring)_totalExecutionTime + " nanosecs");
				}
		}
}

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/047_streams_host_tags_at_work_host_tags_streams_host_tags_at_work_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/049_json_to_tuple_to_json_using_java_sample_Main_spl/"> > </a>
</div>

