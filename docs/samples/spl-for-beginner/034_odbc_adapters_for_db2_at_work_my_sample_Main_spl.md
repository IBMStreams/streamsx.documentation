---
layout: samples
title: 034_odbc_adapters_for_db2_at_work
---

### 034_odbc_adapters_for_db2_at_work

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/033_java_primitive_operator_at_work_my_sample_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/035_c++_primitive_operator_at_work_my_sample_Main_spl/"> > </a>
</div>

~~~~~~
/*
This example shows the use of the three Streams ODBC adapters. Those operators
are ODBCSource, ODBCAppend, and ODBCEnrich. The code in this example is written
to access a particular test DB2 database inside IBM. You have to create your own 
DB2 database and tables to make this application work in your environment.
After creating your own database and tables, you have to change the ./etc/connections.xml
file in this application's directory to match your database/table names, userid, and
password. You also have to make changes in the SPL code using your database information
for all the three ODBC operator invocations. 
*/
namespace my.sample;
// Include the namespace where the Database adapters are available.
// For running this example in the IDE, you have to add the DB toolkit directory
// in the Streams Explorer view. Then, in this application's info.xml file,
// you also have to add the DB toolkit name as a dependency (com.ibm.streams.db).
use com.ibm.streams.db::*;
/*
=============================================================================================
We have to create a test DB2 database and two tables for this program to work.
Please read the file "create_034_db2_tables.sql" in this application's
directory for details about creating that DB2 database and those two tables.
This application expects a DB2 database named "MYDB" and two tables named
"Order" and "OrderResults" available in that database.

The other file that should be read is "./etc/connections.xml" file, where the connection and
access specifications required by the ODBC operators are defined.

This application was tested using a DB2 V10.1 database on November/10/2012 and all the
three ODBC operators used below worked fine. In order to build and run this application,
you have to set the following environment variables.

export STREAMS_ADAPTERS_ODBC_DB2=1
export STREAMS_ADAPTERS_ODBC_INCPATH=/opt/ibm/db2/V10.1/include/
export STREAMS_ADAPTERS_ODBC_LIBPATH=/opt/ibm/db2/V10.1/lib64/
=============================================================================================
What does this example demonstrate?

1) It shows how to read rows from a DB2 database table and convert them into 
   Streams tuples using a ODBCSource operator.

2) It shows how to store Streams tuples into a DB2 database table using the 
   ODBCAppend operator.

3) It shows how to enrich Streams tuples with the rows of data in a DB2 database table. 
   This merged result is the product of the incoming tuple attributes and
   the data read from the DB2 table. This is done by using the ODBCEnrich operator.
=============================================================================================
*/

int64 timeStampToMicroseconds(timestamp ts){
	return(getSeconds(ts)* 1000l * 1000l * 1000l +(int64)(getNanoseconds(ts)))/ 1000l ;
} // End of timeStampToMicroseconds

stateful int64 timeMicroseconds(){
	return timeStampToMicroseconds(getTimestamp());
} // End of timeMicroseconds

rstring gmtime_(int64 micros){
	timestamp ts = createTimestamp(micros / 1000000l,(uint32)(micros % 1000000l * 1000l));
	mutable Sys.tm tms = { sec = 0, min = 0, hour = 0, mday = 0, mon = 0, year = 0, wday = 0, yday = 0, isdst = 0, gmtoff
	= 0, zone = "GMT" } ;
	gmtime(ts, tms);
	return strftime(tms, "%c");
} // End of gmtime_

composite Main {
	graph
	// Read the 10 rows available in the database table named "Order".
    stream<int32 OrderId, rstring CustomerName, int32 CustomerId, rstring ProductName, int32 ProductId, rstring Price> OrderRecord = ODBCSource() {
	param
		connectionDocument : "./etc/connections.xml";
		connection : "SenTestConnection";
		access : "readFromOrderTableForSource";
        initDelay : 5f;
	
	config
		placement: host(Pool1);
    } // End of OrderRecord = ODBCSource()
    
	// Using a Functor, add the shipment status of the order to the tuples read above by the ODBCSource.
	stream<OrderRecord, tuple<int32 ShipmentStatus, rstring ShippingDate>> OrderResultRecord = Functor(OrderRecord) {
		logic
			state: {
				mutable int32 _shipped = 0 ;
				mutable rstring _shipDate = "" ;
			} // End of state:

			onTuple OrderRecord: {
				if (_shipped == 0) {
					_shipped = 1 ;
					_shipDate = gmtime_(timeMicroseconds());
				} else {
					_shipped = 0 ;
					_shipDate = "None" ;
				} // End of if (_shipped == 0)
			} // End of onTuple OrderRecord

		param
			filter: true ;
			
		output
			OrderResultRecord : ShipmentStatus = _shipped, ShippingDate = _shipDate ;
			
		config
			placement: host(Pool1);
	} // End of OrderResultRecord = Functor(OrderRecord)

	// Write the Order Result tuples to a seprate DB2 table named OrderResults.
	()as SinkOp1 = ODBCAppend(OrderResultRecord) {
		param
			connectionDocument : "./etc/connections.xml" ;
			connection : "SenTestConnection" ;
			access : "writeToOrderResultsTable" ;
			
		config
			placement: host(Pool1);
	} // End of SinkOp1 = ODBCAppend(OrderResultRecord)

	// Let us also enrich the data using the ODBCEnrich operator.
	// In order to do that, let us read the rows from the Order table.
	// For each row, we will also enrich the ShipmentStatus and the ShippingDate from the
	// values read from an input file.
	//
	// Define a Source Operator to read the shipping status for different order ids.
	stream<int32 OrderId, int32 ShipmentStatus, rstring ShippingDate> OrderShipmentStatus = FileSource() {
		param
			file : "ShipmentStatus.txt" ;
			format : csv ;
			initDelay : 7f;

		config
			placement: host(Pool1);
	} // End of OrderShipmentStatus = FileSource()

	// Let us now enrich the data read from the Order table.
	stream<OrderRecord, tuple<int32 ShipmentStatus, rstring ShippingDate>> EnrichedOrderRecord = ODBCEnrich(OrderShipmentStatus) {
		param
			connectionDocument : "./etc/connections.xml" ;
			connection : "SenTestConnection" ;
			access : "readFromOrderTableForEnrich" ;
			orderId : OrderId ;
			
		config
			placement: host(Pool1);
	}

	// Let us now write the enriched order records coming out of the ODBCEnrich into a result file.
	()as SinkOp2 = FileSink(EnrichedOrderRecord) {
		param
			file : "odbc_enrich.result" ;
			format : csv ;
			flush : 1u ;
			writePunctuations : true ;
			
		config
			placement: host(Pool1);
	} // End of SinkOp2 = FileSink(EnrichedOrderRecord)

	config
		logLevel: error;
		hostPool: Pool1 = ["localhost"];
} // End of composite Main

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/033_java_primitive_operator_at_work_my_sample_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/035_c++_primitive_operator_at_work_my_sample_Main_spl/"> > </a>
</div>

