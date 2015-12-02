---
layout: samples
title: 903_unique
---

### 903_unique

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/903_unique_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/904_primitive_round_robin_split_Main_spl/"> > </a>
</div>

~~~~~~
namespace my.util;

public composite Uniq (output Out; input In) {
	param 
		type $key;
	
	graph
		stream <In> Out = Custom(In) {
			logic	state: 	{
								mutable boolean first = true;
								mutable $key prev;
							} // End of logic state				
							
			onTuple	In:		{
								$key curr = ($key)In;
								
								if (first || prev != curr) {
									submit (In, Out);
									first = false;
									prev = curr;
								} // End of if (first ...
							} // End of onTuple											
		} // End of Custom(In)
} // End of composite Uniq

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/903_unique_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/904_primitive_round_robin_split_Main_spl/"> > </a>
</div>

