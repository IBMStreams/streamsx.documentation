---
layout: samples
title: 044_streams_checkpointing_at_work
---

### 044_streams_checkpointing_at_work

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/043_import_export_filter_at_work_importing_exporting_filter_import_with_filter_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/045_file_source_using_spl_custom_operator_my_file_source_file_source_using_spl_custom_operator_spl/"> > </a>
</div>

~~~~~~
/*
This example shows a key feature of Streams by which an operator's
state variables can be preserved when a PE fails and gets restarted.
This is done through a combination of the SPL configuration directives named
"checkpointing" and "restartable". Developers can protect their critical
operator data by taking advantage of this built-in checkpointing feature. 
When you run this example, you will see data flows without any gaps or
interruption, when a PE is killed manually and then gets restored automatically by
the Streams runtime.

In order to test this example, you have to run in distributed mode.
*/
namespace checkpointing.example;

composite streams_checkpointing_at_work {
	graph
		stream<rstring str, int64 i> Test1 = Beacon() {
			param
				period: 1.0;
				iterations: 4000;
				
			output
				// Send the value of seconds elapsed since epoch.
				Test1: str = (rstring)getSeconds(getTimestamp()), i = getSeconds(getTimestamp());
		}
		
		stream<rstring str, int64 i, int64 j> CheckpointedStream = Custom(Test1) {
			logic
				state: {
					// In a terminal window, run "streamtool lspes" command and note down
					// the pid for this PE identified by its output stream name.
					// In that same terminal window, run "kill -9 <pid>" for that PE's pid.
					// When this PE is forcefully killed, Streams runtime will automatically
					// restore the value held by this state variable at the time of the crash. 
					mutable int64 _cnt = 0;	
				}
				
				onTuple Test1: {
					_cnt++;
					mutable CheckpointedStream _oTuple = {};
					assignFrom(_oTuple, Test1);
					_oTuple.j = _cnt;
					// You can check this output from the PE console log as shown below.
					// After you kill the PE, it will automatically get restarted by the
					// Streams runtime. Its internal state also will get restored from the
					// latest checkpoint that was taken just before the crash. You should see
					// no missing data in the flow as logged in the following file.
					// cat /tmp/Streams-<domain_id>/logs/<host_name>/instances/<streams_instance_name>/jobs/<job_id>/pec.pe.<peId>.stdouterror
					printStringLn("_oTuple = " + (rstring)_oTuple);
					submit(_oTuple, CheckpointedStream);
				}
				
			config
				// We will do a periodic checkpoint of this operator every two seconds.
				checkpoint: periodic(2.0);
				restartable: true;
				relocatable: true;
		}
		
		stream<int64 minValue, int64 maxValue, int64 avgValue> AggregatedStream = Aggregate(CheckpointedStream) {
			window
				CheckpointedStream: sliding, count(50), count(1);
			
			output
				AggregatedStream: minValue = Min(j), maxValue = Max(j), avgValue = Average(j);
		}
		
		() as FileWriter = FileSink(AggregatedStream) {
			param
				file: "AggOutput.csv";
				append: true;
		
		}
		
		
}

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/043_import_export_filter_at_work_importing_exporting_filter_import_with_filter_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/045_file_source_using_spl_custom_operator_my_file_source_file_source_using_spl_custom_operator_spl/"> > </a>
</div>

