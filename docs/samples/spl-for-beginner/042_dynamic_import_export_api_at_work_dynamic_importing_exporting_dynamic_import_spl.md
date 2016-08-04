---
layout: samples
title: 042_dynamic_import_export_api_at_work
---

### 042_dynamic_import_export_api_at_work

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/042_dynamic_import_export_api_at_work_dynamic_importing_exporting_dynamic_export_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/043_import_export_filter_at_work_importing_exporting_filter_export_with_filter_spl/"> > </a>
</div>

~~~~~~
/*
This example shows how to use the SPL APIs for dynamically importing and exporting streams.
This is achieved by changing the import and export properties on the fly. This powerful
feature in Streams provides a way to change the streams producing and consuming operators
to change the way in which they publish and subscribe to streams while the application is running.

This main composite dynamically changes the imported stream subscription value after every minute.
In order to test this, always launch the dynamic_export composite first in distributed mode.
After that, launch the dynamic_import composite in distributed mode. You can watch this whole
thing working inside the Streams Instance Graph by starting it from the Streams Explorer view.
*/
namespace dynamic.importing.exporting;

composite dynamic_import {
	type
		SimpleTransaction = tuple<int32 number, rstring string>;
	
	graph
		// Import the stream emitted by the dynamic_export main composite.
		stream<SimpleTransaction> ImportedSimpleTxStream = Import() {
			param
				// To begin with, set an import subscription that will not find a match with the exported stream from another composite.
				subscription: AllowedMinimumNumber < 0l;
		} // End of ImportedSimpleTxStream = Import()
		
		// Let us have a Beacon to periodically send a signal to change the input port import subscription.
		stream<int32 subscriptionChangeSignal> ImportSubscriptionChangeSignal = Beacon() {
			param
				period: 5.0;
		} // End of ImportSubscriptionChangeSignal = Beacon()
		
		// Let us change the import subscription value in this Custom operator.
		stream<SimpleTransaction> SimpleTxStreamForOutput = Custom(ImportSubscriptionChangeSignal as ISCS; 
			ImportedSimpleTxStream as ISTS) {
			logic
				state: {
					mutable int32 _secondsElapsedSinceImportSubscriptionWasChanged  = 0l;
					mutable boolean _matchExportedStreamProperty = false;
					mutable rstring _newSubscription = "";
				} // End of state
				
				onTuple ISCS: {
					// The other main composite in this application (dynamic_export) will keep sending
					// one exported tuple every 10 seconds. After every minute of time passes by, that application also
					// changes its exported stream property to the value of one of its tuple attributes (int32 number).
					// It does that just to show how an output port export property can be 
					// dynamically changed on the fly.
					//
					//
					// Similarly, in the current main composite, where you are now (dynamic_import), we will
					// write some code below to demonstrate how import subscription can also be 
					// dynamically changed using a new API available in Streams 3.0.
					// In order to do that, after every 30 seconds, we will arbitrarily change the
					// import subscription so as to toggle the matching of the exported stream property.
					// i.e. for one 30 second block, we will not match any exported stream property and
					// in the next 30 second block, we will match with the exported stream property.
					// We are doing this logic just to show the reader of this application, how both
					// the export property and import subscription can be changed dynamically.
					_secondsElapsedSinceImportSubscriptionWasChanged += 5;					
					
					if (_secondsElapsedSinceImportSubscriptionWasChanged >= 30) {
						// It is time to a change the import subscription value.
						// Reset the timer flag to 0 to wait for the next 30 seconds of time to pass by.
						_secondsElapsedSinceImportSubscriptionWasChanged = 0;
						
						// On every import subscription change event, toggle either to match or not match with the exported stream property.
						if (_matchExportedStreamProperty == false) {
							// Set the import subscription such that we will match the exported stream property.
							_matchExportedStreamProperty = true;
							_newSubscription = "AllowedMinimumNumber >= 0"; 
						} else {
							// Set the import subscription such that we will not match the exported stream property.
							// Please note that, we are doing this arbitrary logic just to showcase
							// SPL subscription API.
							_matchExportedStreamProperty = false;
							_newSubscription = "AllowedMinimumNumber < 0"; 
						} // End of if (_matchExportedStreamProperty == false)
					
						// Let us keep changing the import subscription value periodically.
						int32 rc = setInputPortImportSubscription(_newSubscription, 1u);
	
						if (rc != 0) {
							// Log the error and abort the application.
							log(Sys.error, "New Subscription=" + _newSubscription);
							log(Sys.error, "SetInputPortImportSubscription API failed with return code " + (rstring)rc);
							abort();
						} // End of if (rc != 0)
					} // End of if (_secondsElapsedSinceImportSubscriptionWasChanged >= 30)
				} // End of onTuple ISCS
				
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
} // End of composite dynamic_import


~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/042_dynamic_import_export_api_at_work_dynamic_importing_exporting_dynamic_export_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/043_import_export_filter_at_work_importing_exporting_filter_export_with_filter_spl/"> > </a>
</div>

