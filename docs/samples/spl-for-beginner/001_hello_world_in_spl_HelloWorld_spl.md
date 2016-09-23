---
layout: samples
title: 001_hello_world_in_spl
---

### 001_hello_world_in_spl

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/002_source_sink_at_work_sample_source_sink_at_work_spl/"> > </a>
</div>

~~~~~~
/*
This example is the simplest possible SPL application.
It uses a Beacon operator to generate tuples that carry
"Hello World" messages. A custom sink operator receives
the tuples from Beacon and displays it on the console.
*/
composite HelloWorld {
	graph
		stream <rstring message> Hi = Beacon() {
			param
				iterations: 5u;
				
			output
				Hi: message = "Hello World!";
		} // End of Beacon.
		
		() as Sink = Custom(Hi) {
			logic	
				onTuple	Hi:
					// In the standalone build, you will see this message on your console.
					// In the distributed build, you will see this message inside the
					// console log file written on the machine where this Custom operator is running.
					// /tmp/Streams-<domain_id>/logs/<host_name>/instances/<streams_instance_name>/jobs/<job_id>/pec.pe.<pe_id>.stdouterror
					printStringLn(message);
		} // End of Custom.
} // End of HelloWorld composite.
~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/002_source_sink_at_work_sample_source_sink_at_work_spl/"> > </a>
</div>

