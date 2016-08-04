---
layout: samples
title: 041_real_time_streams_merger
---

### 041_real_time_streams_merger

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/040_ingest_data_generation_in_spl_my_sample_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/042_dynamic_import_export_api_at_work_dynamic_importing_exporting_dynamic_export_spl/"> > </a>
</div>

~~~~~~
/*
This example shows how two or more incoming streams with a common schema can be merged to 
flow in a sequence one after the other.
This merger will be done by using a common tuple attribute in those multiple streams as a key.
We will use a C++ primitive operator called OrderedMerger that is included in this project.
In order for the OrderedMerger to work correctly, it is assumed that the two or more input
streams for this primitive operator should already be in sorted order based on the key used to
merge and sequence them together. (In the three input files, we deliberately have missing data.
10 to 19 missing in the first file, 20 to 29 missing in the second file, and 30 to 39 missing
in the 3rd file. You can see the correct ordered merger behavior in the
final output from this application.)

This OrderedMerger C++ primitive operator uses the PriorityQueue mechanism for its inner workings.
A file named impl/include/PriorityQueue.h contains the implementation for PriorityQueue. That
facility and the C++ operator were built by my friend and our fantastic Streams designer/developer Bugra.
*/
namespace real.time.merger;

// Make a declaration to use the Ordered merger primitive operator inside this SPL composite.
// You can look at the code for the C++ primitive operator inside the real.time.merger/OrderedMerger
// sub-directory inside this project.
use real.time.merger::OrderedMerger;

composite real_time_streams_merger {
	// Define the types used in this example.
    type
    	SrcT = tuple<int32 no, rstring name>;
    	
	graph
		// Read the first stream from a file.
	    stream<SrcT> Src1 = FileSource() 
	    {
	      param
	      	format: csv;
	        file: "source1.txt";
	    }
	    
		// Read the second stream from the file.
	    stream<SrcT> Src2 = FileSource() 
	    {
	      param
	        file: "source2.txt";
	    }

		// Read the third stream from the file.
	    stream<SrcT> Src3 = FileSource() 
	    {
	      param
	        file: "source3.txt";
	    }
    
		// Send the three streams to this primitive operator as input.
		// This operator expects the three input streams to be in sorted order for 
		// the merger to work correctly.
	    stream<SrcT> Res = OrderedMerger(Src1; Src2; Src3)
	    {
	      param 
	        key : Src1.no; 
	        bufferSize : 1000u;
	        // Note: if you do not specify a bufferSize, then you will have a
	        // non-blocking merger (useful for split/merge). 
	        // Otherwise, you have a blocking merger (useful for streams coming from independent sources).
	    }
	    	
		// Merged streams will enter this operator one after another in a sequence.
		// If all the three streams match in their keys, then they will come in a sequence.
		// If there are any streams with unmatched keys, then they will be interleaved
		// in the sorted order.	
		()as Sink = FileSink(Res){
			param
				// Write the results to stdout error.
				file : "/dev/stderr" ;
				flush : 1u ;
		}
}


~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/040_ingest_data_generation_in_spl_my_sample_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/042_dynamic_import_export_api_at_work_dynamic_importing_exporting_dynamic_export_spl/"> > </a>
</div>

