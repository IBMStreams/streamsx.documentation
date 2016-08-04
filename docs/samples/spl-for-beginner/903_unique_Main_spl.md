---
layout: samples
title: 903_unique
---

### 903_unique

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/902_word_count_word_count_WordCount_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/903_unique_my_util_Uniq_spl/"> > </a>
</div>

~~~~~~
/*
This example is the same code that can be found in the SPL introductory tutorial PDF file.
Please see that PDF file for a description about what this application does.
*/
use my.util::Uniq;

composite Main {
	type
		KeyType = tuple <int32 j>;
	
	graph
		stream <int32 i, int32 j> DefaultAll = Beacon() {
			param
				iterations: 10u;
		} // End of Beacon.

		// In this custom operator, we are going to set the
		// tuple attribute values.
		stream<DefaultAll> All = Custom(DefaultAll as DA) {
			logic
				state: mutable int32 n = 0;
			
			onTuple DA: {
				++n;
				DA = {i = n, j = n/3};
				submit(DA, All);
			} // End of onTuple DA		
		} // End of Custom(DefaultAll as DA)
		
		stream <All> Some = Uniq(All) {
			param
				key: KeyType;
		} // End of Uniq.
		
		() as PrintAll = Custom(All) {
			logic
				state: mutable int32 err = 0;
				
				onTuple All	: {
					printStringLn("All " + (rstring)All);
					spl.file::fflush (0ul, err);
				} // End of onTuple All
		} // End of Custom(All)
		
		() as PrintSome = Custom(Some) {
			logic	
				state: mutable int32 err = 0;
				
				onTuple Some: {
					printStringLn("Some " + (rstring)Some);
					spl.file::fflush (0ul, err);
				} // End of onTupe Some
		} // End of Custom(Some)	
		
		config
			logLevel		: error;	
			// You have to change this hostname with a hostname that is valid on your network.
			placement		: host("localhost");
} // End of composite Main

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/902_word_count_word_count_WordCount_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/903_unique_my_util_Uniq_spl/"> > </a>
</div>

