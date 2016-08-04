---
layout: samples
title: 042_dynamic_import_export_api_at_work
---

### 042_dynamic_import_export_api_at_work

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/041_real_time_streams_merger_real_time_merger_real_time_streams_merger_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/042_dynamic_import_export_api_at_work_dynamic_importing_exporting_dynamic_import_spl/"> > </a>
</div>

~~~~~~
/*
This example shows how to use the SPL APIs for dynamically importing and exporting streams.
This is achieved by changing the import and export properties on the fly. This powerful
feature in Streams provides a way to change the streams producing and consuming operators
to change the way in which they publish and subscribe to streams while the application is running.

The main composite below dynamically changes the exported stream property value after every minute.
In order to test this, always launch the dynamic_export composite first in distributed mode.
After that, launch the dynamic_import composite in distributed mode.  You can watch this whole
thing working inside the Streams Instance Graph by starting it from the Streams Explorer view.
*/
namespace dynamic.importing.exporting;

composite dynamic_export {
	type
		SimpleTransaction = tuple<int32 number, rstring string>;
	
	graph
		// Create a Beacon signal every 10 seconds.
		stream<SimpleTransaction> SimpleTxStream = Beacon() {
			param
				iterations: 7000;
				period: 10.0;
		} // End of SimpleTxStream = Beacon()


		// Receive the Beacon signal and customize the tuple attributes and send it for export.
		stream<SimpleTransaction> ModifiedSimpleTxStream = Custom(SimpleTxStream as STS) {
			logic
				state: {
					mutable int32 _tupleCnt = 0;
					mutable int32 _secondsElapsedSinceExportPropertyWasChanged = 0;
				} // End of state
				
				onTuple STS: {
					// Modify the tuple attributes and send it away.
					STS.number = ++_tupleCnt;
					STS.string = "String " + (rstring)_tupleCnt;
					// Before submitting this tuple, let us change the exported property value using 
					// the new API available in Streams 3.0 and later releases. 
					// This is an arbitrary change just to showcase a new SPL API.
					// It demonstrates how output port export properties can be dynamically changed.
					// Let us do this dynamic change periodically.
					// After every minute, we will dynamically change the exported stream property value by 
					// changing the property value to the current value of one of the attributes of the exported stream.
					// Beacon triggers every 10 seconds. Hence, we will advance the elapsed time by 10 seconds.
					_secondsElapsedSinceExportPropertyWasChanged += 10;
					
					if (_secondsElapsedSinceExportPropertyWasChanged >= 60) {
						// It is time to a change the exported stream property value.
						// Reset the timer flag to 0 to wait for the next minute of time to pass by.
						_secondsElapsedSinceExportPropertyWasChanged = 0;
						// We will change the exported property value by setting it to the current value of the "number" tuple attribute.
						int32 rc = setOutputPortExportProperties({AllowedMinimumNumber=(int64)STS.number}, 0u);
					
						if (rc != 0) {
							// Log the error and abort the application.
							log(Sys.error, "SetOutputPortExportProperties API failed with return code " + (rstring)rc);
							abort();
						} // End of if (rc != 0)
					} // End of if (_secondsElapsedSinceExportPropertyWasChanged >= 60)
					
					// Send it on the first output port index (New submit API in Streams 3.0)
					submit(STS, 0u);
				} // End of onTuple STS
		} // End of ModifiedSimpleTxStream = Custom(SimpleTxStream as STS)
		
		// Export the modified simple Tx stream.
		() as ExportedSimpleTxStream = Export(ModifiedSimpleTxStream as MSTS) {
			param
				// To begin with, set the exported stream property value to a default of 0.
				// This property value will be dynamically changed after every minute using the new SPL API.
				properties: {AllowedMinimumNumber = 0l};
		} // End of ExportedSimpleTxStream = Export(ModifiedSimpleTxStream)		 
} // End of composite dynamic_export
~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/041_real_time_streams_merger_real_time_merger_real_time_streams_merger_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/042_dynamic_import_export_api_at_work_dynamic_importing_exporting_dynamic_import_spl/"> > </a>
</div>

