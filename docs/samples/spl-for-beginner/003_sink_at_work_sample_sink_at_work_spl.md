---
layout: samples
title: 003_sink_at_work
---

### 003_sink_at_work

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/002_source_sink_at_work_sample_source_sink_at_work_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/004_delay_at_work_sample_delay_at_work_spl/"> > </a>
</div>

~~~~~~
/*
This example shows how FileSinks and Custom sinks can be employed
in applications. It also shows how a Beacon operator can be used
to customize tuple attributes. In addition, it introduces the 
Filter operator to route the incoming tuples by inspecting
their attributes using a filter statement. 
*/
namespace sample;

composite sink_at_work {
	type
		PersonSchema = tuple <rstring name, uint32 id>;
		SelectedPersonSchema = tuple <rstring name, uint32 id, rstring nameLower, boolean candidate>;

	graph
		stream <PersonSchema> Person = Beacon() {
			logic
				state: {
					// Declare a state variable here.
					mutable int32 n = 0;
				}
				
			param
				iterations : 200u;
			
			output
				Person : id = (uint32) (random()*100.0), name = upper("Test") + (rstring)++n;
		} // End of Beacon.
    
		stream<SelectedPersonSchema> SelectedPerson = Functor(Person) {
			param 
				// Allow those tuples with the following condition to flow to the next stage for processing.
				// Other tuples will be dropped.
				filter: id >= 20u;
			
			output 
				SelectedPerson: nameLower = lower(name), candidate = (id >= 25u);
		} // End of Functor(Person)

		() as FileWriter = FileSink(SelectedPerson) {
			param
				file : "myResults.txt";
		} // End of FileSink.

		() as ScreenWriter = Custom(SelectedPerson) {
			logic
				onTuple SelectedPerson : {
					println(SelectedPerson);         
				} // End of logic onTuple.
	} // End of Custom(SelectedPerson)
} // End of composite sink_at_work.

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/002_source_sink_at_work_sample_source_sink_at_work_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/004_delay_at_work_sample_delay_at_work_spl/"> > </a>
</div>

