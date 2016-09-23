---
layout: samples
title: 043_import_export_filter_at_work
---

### 043_import_export_filter_at_work

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/043_import_export_filter_at_work_importing_exporting_filter_export_with_filter_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/044_streams_checkpointing_at_work_checkpointing_example_streams_checkpointing_at_work_spl/"> > </a>
</div>

~~~~~~
/*
This example shows how to use the SPL feature to apply a filter for what gets
exported and what gets imported. This powerful feature lets the downstream
import operators to specify what kind of tuples they want to receive by
specifying conditional expressions involving tuple attributes. That lets the
Streams runtime to apply content-based filtering at the point of export. Those who
need such a feature to control what information should be sent downstream based on
the tuple contents can make use of this flexible feature. This can be done on the
fly without stopping and restarting the application.

The main composite below imports the exported stream using a filter expression.
In order to test this, always launch the export_with_filter first in distributed mode.
After that, launch the import_with_filter in distributed mode.
*/
namespace importing.exporting.filter;

composite import_with_filter {
	type
		SimpleTransaction = tuple<int64 number, rstring string>;
	
	graph
		// Import the stream emitted by the dynamic_export main composite.
		stream<SimpleTransaction> ImportedSimpleTxStream = Import() {
			param
				
				// To begin with, set an import filter expression that will not find a match with the exported stream from another composite.
				filter: number < 0l;
				subscription: exportedStreams == 1l;
		} // End of ImportedSimpleTxStream = Import()
		
		// Let us have a Beacon to periodically send a signal to change the input port import filter expression.
		stream<int32 filterExpressionChangeSignal> ImportFilterExpressionChangeSignal = Beacon() {
			param
				period: 5.0;
		} // End of ImportFilterExpressionChangeSignal = Beacon()
		
		// Let us change the import subscription value in this Custom operator.
		stream<SimpleTransaction> SimpleTxStreamForOutput = Custom(ImportFilterExpressionChangeSignal as IFECS; 
			ImportedSimpleTxStream as ISTS) {
			logic
				state: {
					mutable int32 _secondsElapsedSinceImportFilterExpressionWasChanged  = 0l;
					mutable boolean _matchExportedStreamAttributeValues = false;
					mutable rstring _newFilterExpression = "";
				} // End of state
				
				onTuple IFECS: {
					// The other main composite in this application (export_with_filter) will keep sending
					// one exported tuple every 5 seconds. That tuple contains two attributes: int64 number, rstring string.
					// Every tuple will carry increasing value for the number attribute.
					//
					//
					// Similarly, in the current main composite, where you are now (import_with_filter), we will
					// write some code below to demonstrate how import filter expression can also be 
					// dynamically changed using a new API available in Streams 3.0.
					// In order to do that, after every 20 seconds, we will arbitrarily change the
					// filter expression so as to toggle the matching of the exported stream tuple attribute.
					// i.e. for one 20 second block, we will not match any exported stream tuple attribute values and
					// in the next 20 second block, we will match with the exported stream tuple attribute values.
					// We are doing this logic just to show the reader of this application, how the
					// import filter expression can be changed dynamically.
					_secondsElapsedSinceImportFilterExpressionWasChanged += 5;					
					
					if (_secondsElapsedSinceImportFilterExpressionWasChanged >= 20) {
						// It is time to a change the import filter expression value.
						// Reset the timer flag to 0 to wait for the next 20 seconds of time to pass by.
						_secondsElapsedSinceImportFilterExpressionWasChanged = 0;
						
						// On every import filter expression change event, toggle either to match or not match with the exported stream tuple attribute.
						if (_matchExportedStreamAttributeValues == false) {
							// Set the import filter expression such that we will match the exported stream tuple attribute.
							_matchExportedStreamAttributeValues = true;
							_newFilterExpression = "number > 0"; 
						} else {
							// Set the import filter expression such that we will not match the exported stream tuple attribute.
							// Please note that, we are doing this arbitrary logic just to showcase
							// SPL change filter expression API.
							_matchExportedStreamAttributeValues = false;
							_newFilterExpression = "number < 0"; 
						} // End of if (_matchExportedStreamAttributeValues == false)
					
						// Let us keep changing the import filter expression value periodically.
						int32 rc = setInputPortImportFilterExpression(_newFilterExpression, 1u);
	
						if (rc != 0) {
							// Log the error and abort the application.
							log(Sys.error, "New Filter Expression=" + _newFilterExpression);
							log(Sys.error, "setInputPortImportFilterExpression API failed with return code " + (rstring)rc);
							abort();
						} // End of if (rc != 0)
					} // End of if (_secondsElapsedSinceImportFilterExpressionWasChanged >= 30)
				} // End of onTuple IFECS
				
				onTuple ISTS: {
					// Send it on the first output port index (New submit API in Streams 3.0)
					submit(ISTS, 0u);				 
				} // End of onTuple ISTS
				
		} // End of SimpleTxStreamForOutput = Custom(ImportedSimpleTxStream as ISTS)
		
		() as Sink1 = Custom(SimpleTxStreamForOutput as STSFO) {
			logic
				onTuple STSFO: {
					printStringLn("SimpleTxStream = " + (rstring) STSFO);
				} // End of onTuple STSFO
		} // End of Sink1 = Custom(SimpleTxStreamForOutput as STSFO)
}

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/043_import_export_filter_at_work_importing_exporting_filter_export_with_filter_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/044_streams_checkpointing_at_work_checkpointing_example_streams_checkpointing_at_work_spl/"> > </a>
</div>

