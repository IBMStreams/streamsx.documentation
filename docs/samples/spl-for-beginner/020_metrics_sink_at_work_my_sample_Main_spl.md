---
layout: samples
title: 020_metrics_sink_at_work
---

### 020_metrics_sink_at_work

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/019_import_export_at_work_my_sample2_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/021_pair_at_work_my_sample_Main_spl/"> > </a>
</div>

~~~~~~
/*
This example shows how one can use the MetricsSink standard toolkit
operator to create application-specific custom metrics that can be
viewed in real-time when the application is running. The viewing of 
the custom metrics is typically done in the Streams Explorer view of
the Streams Studio or by using the capturestate option in streamtool. 

In order to test this example, you have to start your streams instance
from the Streams Explorer view. Then, you have to run this example by
using the Distributed launch configuration.
*/
namespace my.sample;

// You can view the metrics values produced by the MetricsSink in
// one of two ways.
// 1) Do "Show Metrics" on your instance in the Streams Explorer.
// 2) streamtool capturestate -i <instance_name> -j <job_id> --select jobs=metrics

composite Main {
	graph
		stream <int64 a, int64 b> A = Beacon() {
		} // End of A = Beacon()

		() as MyMetrics = MetricsSink(A) { 
			param 
				metrics : a, b, a + b, a * b; 
				names : "a", "b", "sum", "product"; 
				descriptions : "A", "B", "sum of A and B", "product of A and B"; 
				initialValues : 100l, 1000l, -900l, 5l; 
		} // End of MetricsSink(A)
} // End of the main composite


~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/019_import_export_at_work_my_sample2_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/021_pair_at_work_my_sample_Main_spl/"> > </a>
</div>

