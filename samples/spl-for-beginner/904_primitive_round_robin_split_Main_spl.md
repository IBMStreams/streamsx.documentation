---
layout: samples
title: 904_primitive_round_robin_split
---

### 904_primitive_round_robin_split

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/903_unique_my_util_Uniq_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/905_gate_load_balancer_my_sample_Main_spl/"> > </a>
</div>

~~~~~~
/*
This example is the same code that can be found in the SPL introductory tutorial PDF file.
Please see that PDF file for a description about what this application does.
*/
use my.util::RoundRobinSplit;

composite Main {
	graph
		stream <int32 count> Input = Beacon() {
			logic
				state: mutable int32 n = 0;
				
			param
				iterations:	10u;
				
			output Input:
				count = n++;			
		} // End of Beacon.
		
		(stream <int32 count> A0; stream <int32 count> A1) = RoundRobinSplit(Input) {
			param
				batch: 2u;
		} // End of RoundRobinSplit.
		
		stream <int32 count, int32 path> B0 = Functor(A0) {
			output B0:
				path = 1;
		} // End of Functor(B0)
		
		stream <int32 count, int32 path> B1 = Functor(A1) {
			output B1:
				path = 2;
		} // End of Functor(B1)
		
		stream <int32 count, int32 path> Output = Pair(B0; B1) {
		} // End of Pair.
		
		() as Sink = FileSink(Output) {
			param
				file: "round_robin_split.txt";
		} // End of FileSink.
} // End of composite Main.

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/903_unique_my_util_Uniq_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/905_gate_load_balancer_my_sample_Main_spl/"> > </a>
</div>

