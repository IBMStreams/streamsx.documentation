---
layout: samples
title: 007_split_at_work
---

### 007_split_at_work

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/006_barrier_at_work_sample_barrier_at_work_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/008_get_submission_time_value_Main_spl/"> > </a>
</div>

~~~~~~
/*
This example shows how a Split operator can be used to split the
incoming tuples based on a key. In this example, the split
criteria (i.e. which tuples will come out on which port) is 
pre-configured through a text file. Alternatively, one can 
compute the index of the output port on the fly inside the
Split operator parameter section.

It also gives a gentle introduction to the simple use of the
mixed mode programming by combining PERL code inside SPL code.
*/
namespace sample;

composite split_at_work {
	type 
		StockReportSchema = tuple <rstring symbol, rstring dateTime, float64 closingPrice, uint32 volume>;

	graph
		stream<StockReportSchema> StockReport = FileSource() {
			param
				file: "stock_report.dat";
				format: csv;
				hasDelayField: true;
		} // End of FileSource.

		// Create a PERL loop to emit 26 output streams.
		
		(
			stream<StockReportSchema> StockReportOutput1
 
			
				;
			
		
			stream<StockReportSchema> StockReportOutput2
 
			
				;
			
		
			stream<StockReportSchema> StockReportOutput3
 
			
				;
			
		
			stream<StockReportSchema> StockReportOutput4
 
			
				;
			
		
			stream<StockReportSchema> StockReportOutput5
 
			
				;
			
		
			stream<StockReportSchema> StockReportOutput6
 
			
				;
			
		
			stream<StockReportSchema> StockReportOutput7
 
			
				;
			
		
			stream<StockReportSchema> StockReportOutput8
 
			
				;
			
		
			stream<StockReportSchema> StockReportOutput9
 
			
				;
			
		
			stream<StockReportSchema> StockReportOutput10
 
			
				;
			
		
			stream<StockReportSchema> StockReportOutput11
 
			
				;
			
		
			stream<StockReportSchema> StockReportOutput12
 
			
				;
			
		
			stream<StockReportSchema> StockReportOutput13
 
			
				;
			
		
			stream<StockReportSchema> StockReportOutput14
 
			
				;
			
		
			stream<StockReportSchema> StockReportOutput15
 
			
				;
			
		
			stream<StockReportSchema> StockReportOutput16
 
			
				;
			
		
			stream<StockReportSchema> StockReportOutput17
 
			
				;
			
		
			stream<StockReportSchema> StockReportOutput18
 
			
				;
			
		
			stream<StockReportSchema> StockReportOutput19
 
			
				;
			
		
			stream<StockReportSchema> StockReportOutput20
 
			
				;
			
		
			stream<StockReportSchema> StockReportOutput21
 
			
				;
			
		
			stream<StockReportSchema> StockReportOutput22
 
			
				;
			
		
			stream<StockReportSchema> StockReportOutput23
 
			
				;
			
		
			stream<StockReportSchema> StockReportOutput24
 
			
				;
			
		
			stream<StockReportSchema> StockReportOutput25
 
			
				;
			
		
			stream<StockReportSchema> StockReportOutput26
 
			
		) 
		= Split(StockReport) {
			param
			// index: hashCode(toCharacterCode(symbol, 0) - toCharacterCode("A", 0));
			file: "mapping.txt";
			key:  symbol;
		} // End of Split

		// Let us randomly tap into 3 out of 26 output streams, and write them to file sinks.
		() as FileWriter1 = FileSink(StockReportOutput1) {
			param 
				file: "split_ticker_output_stream_1.result";
		} // End of FileSink(StockReportOutput1)

		() as FileWriter2 = FileSink(StockReportOutput7) {
			param 
				file: "split_ticker_output_stream_7.result";
		} // End of FileSink(StockReportOutput7)

		() as FileWriter3 = FileSink(StockReportOutput9) {
			param 
				file: "split_ticker_output_stream_9.result";
		} // End of FileSink(StockReportOutput9)
} // End of composite split_at_work

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/006_barrier_at_work_sample_barrier_at_work_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/008_get_submission_time_value_Main_spl/"> > </a>
</div>

