---
layout: samples
title: 019_import_export_at_work
---

### 019_import_export_at_work

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/018_directory_scan_at_work_my_sample_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/019_import_export_at_work_my_sample2_Main_spl/"> > </a>
</div>

~~~~~~
/*
This example demonstrates how two different SPL applications can
share streams between them. This is an important feature that is 
elegantly done using the two pseudo operators called Export and Import.
This application also shows how two different main composites can be
part of the same application by using two different namespaces.
As an aside, there is also a demonstration of using a Custom operator
to customize the Beacon generated tuples by involving state variables. 

Note: This application doesn't work in the Standalone launch mode.
Since Export and Import operators are involved, you must start your
Streams instance from the Streams Explorer view and then submit
the two composites using the Distributed launch configuration.

You can verify the results of this application either in the PE log
files or via the Streams instance graph from the Streams Explorer view.

In Streams 4.x onwards, PE log files are available for viewing in a new location:
/tmp/Streams-<domain_id>/logs/<host_name>/instances/<streams_instance_name>/jobs/<job_id>/pec.pe.<pe_id>.stdouterror 

*/
namespace my.sample;
// This file imports a stream from another application.
// In order to wait for the other application to be started,
// this application's source operator waits with an initDelay of 30 seconds.
composite Main {
	type
		employee = tuple<rstring name, uint32 employeeDepartment>;
		department = tuple<uint32 departmentId, rstring departmentName>;
		ticker = tuple<rstring symbol, float32 price, uint32 quantity, rstring tradeType>;

	graph
		stream <employee> EmployeeRecord = FileSource() {
			param
				file:	"EmployeeRecords.txt";
				format:	csv;
				hasDelayField: true;
				initDelay: 30.0;
		} // End of EmployeeRecord = FileSource()
		
		() as ExportedEmployeeRecord = Export(EmployeeRecord) {
			param
				streamId: "ExportedEmployeeRecord";
		} // End of ExportedEmployeeRecord = Export(EmployeeRecord)
		
		stream <department> DepartmentRecord = Import() {
			param
				applicationName: "my.sample2::Main";
				streamId: "ExportedDepartmentRecord";
		} // End of DepartmentRecord = Import()

		// Inner Join of two streams.
		stream <employee, department> InnerJoin1 = Join(EmployeeRecord; DepartmentRecord) {
			window
				EmployeeRecord: sliding, count(14);
				DepartmentRecord: sliding, count(14);
				
			param
				match: EmployeeRecord.employeeDepartment == DepartmentRecord.departmentId;
				algorithm: inner;
		} // End of InnerJoin1 = Join(EmployeeRecord; DepartmentRecord)
		
		() as ScreenWriter1 = Custom(InnerJoin1) {
			logic
				state: 
					mutable int32 joinedTupleCnt = 0;
				
				onTuple InnerJoin1: {
					if (joinedTupleCnt++ == 0) {
						printStringLn("\na)Tuples joined during Inner Join with sliding count(14)");
					} // End of if (joinedTupleCnt++ == 0)
					
					printStringLn ((rstring) joinedTupleCnt + "a)" + (rstring) InnerJoin1);
				} // End of onTuple InnerJoin1
		} // End of Custom(InnerJoin1)		
		
		// Beacon automotive and pharma ticker tuples now.
		// They will be exported later.
		stream <ticker> BeaconedTicker = Beacon() {
			param
				initDelay: 30.0f;
				iterations: 80000u;
		} // End of Beacon()
		
		// Enrich the Beacon generated tuple now.
		stream <ticker> Ticker = Custom(BeaconedTicker) {
			logic
				state: {
					mutable uint32 cnt = 0;
					list<rstring> symbols = ["GM", "PFE", "F", "LLY", "BMS"];
					mutable list<float32> prices = [170.34f, 23.12f, 620.34f, 54.67f, 68.34f];
					list<float32> priceIncrements = [0.34f, 0.03f, 0.14f, 0.08f, 0.12f];
					mutable list<uint32> quantities = [156u, 215u, 100u, 165u, 178u];
					list<uint32> quantityIncrements = [6u, 3u, 2u, 5u, 4u];
					list<rstring> tradeTypes = ["buy", "sell"];
					mutable uint32 tradeTypeIndicator = 0; 
					mutable tuple<ticker> result = {};  	
				} // End of state:
			
			onTuple BeaconedTicker: { 
				cnt = ((uint32) (random()*100.0))%5u;
				prices[cnt] = prices[cnt] + priceIncrements[cnt];
				quantities[cnt] = quantities[cnt] + quantityIncrements[cnt];
				
				// Alternate between "buy" and "sell".
				if (tradeTypeIndicator == 0u) {
					tradeTypeIndicator = 1u;
				} else {
					tradeTypeIndicator = 0u;
				}
				
			    result.symbol = symbols[cnt];
				result.price = prices[cnt];
				result.quantity = quantities[cnt];
				result.tradeType = tradeTypes[tradeTypeIndicator];
				//Send this tuple away.
				submit(result, Ticker);
			} // End of BeaconedTicker:
		} // End of Ticker = Custom(BeaconedTicker)
		
		// Filter the automotive stocks separately.
		stream <ticker> AutomotiveTicker = Functor(Ticker) {
			param
				filter: symbol == "GM" || symbol == "F";
		} // End of AutomotiveTicker = Functor(Ticker)

		// Filter the pharam stocks separately.
		stream <ticker> PharmaTicker = Functor(Ticker) {
			param
				filter: symbol == "PFE" || symbol == "LLY" || symbol == "BMS";
		} // End of AutomotiveTicker = Functor(Ticker)		
		
		// Export the Automotive tickers now.
		// Let us export them via properties.
		// They will be imported in the other main composite in my,sample2 namespace.
		() as ExportedAutomativeTickers = Export(AutomotiveTicker) {
			param
				properties: {sector = "Automotive", symbols = ["GM", "F"]};
		} // End of ExportedAutomativeTickers = Export(AutomotiveTicker)
		
		// Export the Pharma tickers now.
		// Let us export them via properties.
		// They will be imported in the other main composite in my,sample2 namespace.
		() as ExportedPharmaTickers = Export(PharmaTicker) {
			param
				properties: {sector = "Pharma", symbols = ["PFE", "LLY", "BMS"]};
		} // End of ExportedPharmaTickers = Export(PharmaTicker)
		
} // End of the main composite

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/018_directory_scan_at_work_my_sample_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/019_import_export_at_work_my_sample2_Main_spl/"> > </a>
</div>

