---
layout: samples
title: 019_import_export_at_work
---

### 019_import_export_at_work

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/019_import_export_at_work_my_sample_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/020_metrics_sink_at_work_my_sample_Main_spl/"> > </a>
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
*/
namespace my.sample2;

composite Main {
	type
		employee = tuple<rstring name, uint32 employeeDepartment>;
		department = tuple<uint32 departmentId, rstring departmentName>;
		ticker = tuple<rstring symbol, float32 price, uint32 quantity, rstring tradeType>;
		
	graph
		stream <department> DepartmentRecord = FileSource() {
			param
				file:	"DepartmentRecords.txt";
				format:	csv;
				hasDelayField: true;
				initDelay: 30.0;
		} // End of DepartmentRecord = FileSource()		

		() as ExportedDepartmentRecord = Export(DepartmentRecord) {
			param
				streamId: "ExportedDepartmentRecord";
		} // End of ExportedDepartmentRecord = Export(DepartmentRecord)
		
		stream <employee> EmployeeRecord = Import() {
			param
				applicationName: "my.sample::Main";
				streamId: "ExportedEmployeeRecord";
		} // End of EmployeeRecord = Import()		

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
						printStringLn("\nb)Tuples joined during Inner Join with sliding count(14)");
					} // End of if (joinedTupleCnt++ == 0)
					
					printStringLn ((rstring) joinedTupleCnt + "b)" + (rstring) InnerJoin1);
				} // End of onTuple InnerJoin1
		} // End of Custom(InnerJoin1)			
		
		
		// Let us import the automotive sector tickers exported by
		// the other main composite in the my.sample namespace.
		stream <ticker> ImportedAutomotiveTickers = Import() {
			param
				subscription: 
					(sector == "Automotive") &&
					("GM" in symbols || "F" in symbols); 
		} // End of ImportedAutomotiveTickers = Import()
		
		// Let us import the pharma sector tickers exported by
		// the other main composite in the my.sample namespace.
		stream <ticker> ImportedPharmaTickers = Import() {
			param
				subscription: 
					(sector == "Pharma") &&
					("PFE" in symbols || "LLY" in symbols || "BMS" in symbols); 
		} // End of ImportedAutomotiveTickers = Import()		

		() as ScreenWriter2 = Custom(ImportedAutomotiveTickers) {
			logic
				state: 
					mutable int32 automotiveTupleCnt = 0;
				
				onTuple ImportedAutomotiveTickers: {
					if (automotiveTupleCnt++ == 0) {
						printStringLn("\nc)Imported Automotive tuples from my.sample::Main");
					} // End of if (automotiveTupleCnt++ == 0)
					
					printStringLn ((rstring) automotiveTupleCnt + "c)" + (rstring) ImportedAutomotiveTickers);
				} // End of onTuple ImportedAutomotiveTickers
		} // End of Custom(ImportedAutomotiveTickers)		

		() as ScreenWriter3 = Custom(ImportedPharmaTickers) {
			logic
				state: 
					mutable int32 pharmaTupleCnt = 0;
				
				onTuple ImportedPharmaTickers: {
					if (pharmaTupleCnt++ == 0) {
						printStringLn("\nd)Imported Pharma tuples from my.sample::Main");
					} // End of if (pharmaTupleCnt++ == 0)
					
					printStringLn ((rstring) pharmaTupleCnt + "d)" + (rstring) ImportedPharmaTickers);
				} // End of onTuple ImportedPharmaTickers
		} // End of Custom(ImportedPharmaTickers)
} // End of the main composite.

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/019_import_export_at_work_my_sample_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/020_metrics_sink_at_work_my_sample_Main_spl/"> > </a>
</div>

