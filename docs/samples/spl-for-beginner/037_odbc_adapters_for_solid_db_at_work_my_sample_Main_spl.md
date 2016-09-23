---
layout: samples
title: 037_odbc_adapters_for_solid_db_at_work
---

### 037_odbc_adapters_for_solid_db_at_work

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/036_shared_lib_primitive_operator_at_work_my_sample_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/038_spl_built_in_functions_at_work_test_scratch_Main_spl/"> > </a>
</div>

~~~~~~
/*
This example shows the use of the three Streams ODBC adapters for connecting to 
a SolidDB in-memory database. Those operators are ODBCSource, ODBCAppend, and 
ODBCEnrich. The code was tested with Solid-DB 7.0. You have to create your own SolidDB database and 
tables to make this application work in your environment.

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
At first, you have to create two tables in a Solid-DB database for this program to work.
Please read the file "create_037_solid_db_tables.txt" in this application's
directory for details about creating those two tables in a Solid-DB database.
This application expects two Solid-DB tables named "Order" and "OrderResults".

The other file that should be read is "./etc/connections.xml" file, where the connection and
access specifications required by the ODBC operators are defined. You have to change this XML file
to specify your actual Solid DB userid and Solid DB password in place of USERID and PASSWD.

This application was tested using a Solid-DB V7.0 database on April/30/2012 and all the
three ODBC operators used below worked fine. In order to build and run this application,
you have to do the following UnixODBC driver configuration.

SPL ODBC adapters use the UnixODBC drivers to work with SolidDB.
UnixODBC requires the following configuration. Please create the following files (steps a through d below).

a) You have to create ~/.odbcinst.ini with the following contents.
[my_solid_db]
Description = ODBC driver for Solid DB 7.0
Driver = /opt/solidDB/soliddb-7.0/lib/libsacl2x6470.so

b) You have to create ~/.odbc.ini with the following contents.
[my_solid_db]
Description = Solid DB for use with Streams
Driver = my_solid_db

c) Ensure that you have a valid ~/solid.ini file with the following contents that are valid if you are
using the IBM internal use only RHEL+Streams VM. If you are using your own Linux server, then you have to
replace the localhost with your SolidDB server name and 2315 with your correct SolidDB port.
[Data Sources]
my_solid_db = tcp localhost 2315

d) Create a file called ~/solid-db-odbc.sh with the following contents.
# Set the required environment variables for using the SPL SolidDB ODBC adapters.
#
# First let us unset the DB2  environment variable that may be already there.
unset STREAMS_ADAPTERS_ODBC_DB2
#
# Go ahead take care of the SolidDB environment settings.
export STREAMS_ADAPTERS_ODBC_SOLID=1
# Point to the UnixODBC include and lib directories. Because, for SolidDB access,
# Streams ODBC adapters need them to compile and run SPL applications that need SolidDB.
# (On some Linux servers, this could be /usr/local/include and /usr/local/lib. Please verify that.)
export STREAMS_ADAPTERS_ODBC_INCPATH=/usr/include
export STREAMS_ADAPTERS_ODBC_LIBPATH=/usr/lib64
# Export the filename that has the UnixODBC driver configuration for SolidDB ODBC resources.
export ODBCINI=~/.odbcinst.ini
# Export the directory where the solid.ini file is located.
export SOLIDDIR=~/

After configuring the above (a, b, c, d), Please do the following.

i)   Close Eclipse.
ii)  In a terminal window, run this: source ~/solid-db-odbc.sh
iii) Run "odbcinst -j" at the shell prompt.
iv)  You can also type "odbcinst -q -s" or "obdcinst -q -d" and see what you get.

At this time, you will be able to use the SolidDB tool called "solsql" to issue
database creation/deletion and other SQL commands (with the uid: solid, pwd: solid if you are using the
IBM internal use only RHEL+Streams VM).

solsql my_solid_db

After trying out a few SQL commands, you can exit from the solsql shell.

All of the above information is well documented in this URL:
http://publib.boulder.ibm.com/infocenter/soliddb/v7r0/index.jsp?topic=/com.ibm.swg.im.soliddb.programmer.doc/doc/unixODBC.html

From the same terminal window, you can now start Eclipse, build and run this example.
=============================================================================================
What does this example demonstrate?

1) It shows how to read rows from a Solid-DB database table and convert them into 
   Streams tuples using a ODBCSource operator.

2) It shows how to store Streams tuples into a Solid-DB database table using the 
   ODBCAppend operator.

3) It shows how to enrich Streams tuples with the rows of data in a Solid-DB database table. 
   This merged result is the product of the incoming tuple attributes and
   the data read from the Solid-DB table. This is done by using the ODBCEnrich operator.
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
	} // End of OrderResultRecord = Functor(OrderRecord)

	// Write the Order Result tuples to a seprate Solid-DB table named OrderResults.
	()as SinkOp1 = ODBCAppend(OrderResultRecord) {
		param
			connectionDocument : "./etc/connections.xml" ;
			connection : "SenTestConnection" ;
			access : "writeToOrderResultsTable" ;
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
	} // End of OrderShipmentStatus = FileSource()

	// Let us now enrich the data read from the Order table.
	stream<OrderRecord, tuple<int32 ShipmentStatus, rstring ShippingDate>> EnrichedOrderRecord = ODBCEnrich(OrderShipmentStatus) {
		param
			connectionDocument : "./etc/connections.xml" ;
			connection : "SenTestConnection" ;
			access : "readFromOrderTableForEnrich" ;
			orderId : OrderId ;
	}

	// Let us now write the enriched order records coming out of the ODBCEnrich into a result file.
	()as SinkOp2 = FileSink(EnrichedOrderRecord) {
		param
			file : "odbc_enrich.result" ;
			format : csv ;
			flush : 1u ;
			writePunctuations : true ;
	} // End of SinkOp2 = FileSink(EnrichedOrderRecord)

	config
		logLevel: error;
		placement: host(Pool1);
		hostPool: Pool1 = ["localhost"];
} // End of composite Main

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/036_shared_lib_primitive_operator_at_work_my_sample_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/038_spl_built_in_functions_at_work_test_scratch_Main_spl/"> > </a>
</div>

