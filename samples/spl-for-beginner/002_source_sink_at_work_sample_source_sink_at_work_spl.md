---
layout: samples
title: 002_source_sink_at_work
---

### 002_source_sink_at_work

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/001_hello_world_in_spl_HelloWorld_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/003_sink_at_work_sample_sink_at_work_spl/"> > </a>
</div>

~~~~~~
/*
This example shows how a FileSource operator can be used to
read CSV formatted records from a file and then receive those 
tuples in a FileSink to be written to another file in the data 
directory of this application.
*/
namespace sample;

composite source_sink_at_work {
	type 
		EmployeeSchema = tuple<rstring name, rstring title, rstring department, float64 salary>;

	graph
		stream<EmployeeSchema> Employee = FileSource() {
			param
				file: "Employee.dat";
				format: csv;
				initDelay: 4.0;
	} // End of Employee = FileSource()

	// Write the arriving tuples to a File sink.
	() as FileWriter = FileSink(Employee) {
		param
			file: "MyResults.txt";
	} // End of FileSink.

} // End of Composite source_sink_at_work

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/001_hello_world_in_spl_HelloWorld_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/003_sink_at_work_sample_sink_at_work_spl/"> > </a>
</div>

