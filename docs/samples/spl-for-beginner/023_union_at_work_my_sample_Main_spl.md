---
layout: samples
title: 023_union_at_work
---

### 023_union_at_work

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/022_deduplicate_at_work_my_sample_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/024_threaded_split_at_work_my_sample_Main_spl/"> > </a>
</div>

~~~~~~
/*
This example demonstrates an utility operator called Union. This operator
combines all the tuples from several input ports as they arrive and emits a
single output stream. All the input ports must have a schema that contains
attributes of the same name and type as that of the output port. The order
of the attributes in the input ports need not match the order in the output port.
*/
namespace my.sample;

composite Main {
	type
		employee = tuple<rstring name, uint32 id>;
		department = tuple<uint32 id, rstring name>;
		orders = tuple<uint32 id, rstring name, rstring orderDate, rstring product, uint32 quantity>;
		inventory = tuple<uint32 id, rstring name, uint32 quantity, float32 price>;
		// Some random combination of attributes that will form the 
		// output tuple of the Union operator. (Just for testing.)
		allCombined = tuple<rstring name, uint32 id>;

	graph
		stream <employee> EmployeeRecord = FileSource() {
			param
				file:	"EmployeeRecords.txt";
				format:	csv;
				hasDelayField: true;
				initDelay: 1.0;
		} // End of EmployeeRecord = FileSource()
				
		stream <department> DepartmentRecord = FileSource() {
			param
				file:	"DepartmentRecords.txt";
				format:	csv;
				hasDelayField: true;
				initDelay: 1.0;
		} // End of DepartmentRecord = FileSource()

		stream <orders> OrderRecord = FileSource() {
			param
				file:	"orders.txt";
				format:	csv;
				hasDelayField: true;
				initDelay: 1.0;
		} // End of OrderRecord = FileSource()
		
		stream <inventory> InventoryRecord = FileSource() {
			param
				file:	"inventory.txt";
				format:	csv;
				hasDelayField: true;
				initDelay: 1.0;
		} // End of InventoryRecord = FileSource()		

		// Some random combination of attributes that will form the 
		// output tuple of the Union operator. (Just for testing.)
		stream <allCombined> AllCombined = Union(EmployeeRecord; DepartmentRecord; OrderRecord; InventoryRecord) {		

		} // End of AllCombined = Union(EmployeeRecord; ...)	
		
		() as ScreenWriter1= Custom(AllCombined) {
			logic
				state: 
					mutable int32 combinedTupleCnt = 0;
				
				onTuple AllCombined: {
					if (combinedTupleCnt++ == 0) {
						printStringLn("\na)Combined tuples from the Union operator:");
					} // End of if (combinedTupleCnt++ == 0)
					
					printStringLn ((rstring) combinedTupleCnt + "a)" + (rstring) AllCombined);
				} // End of onTuple AllCombined
		} // End of ScreenWriter1 = Custom(AllCombined)
} // End of the composite main.

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/022_deduplicate_at_work_my_sample_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/024_threaded_split_at_work_my_sample_Main_spl/"> > </a>
</div>

