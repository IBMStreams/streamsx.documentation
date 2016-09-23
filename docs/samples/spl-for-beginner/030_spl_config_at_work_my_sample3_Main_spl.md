---
layout: samples
title: 030_spl_config_at_work
---

### 030_spl_config_at_work

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/029_spl_functions_at_work_my_sample_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/031_spl_mixed_mode_at_work_my_sample_Main_spl/"> > </a>
</div>

~~~~~~
/*
This example introduces one of the must-learn features of the SPL language.
SPL language offers an extensive list of options to do configuration at the
operator level as well as at the composite level. It attempts to sprinkle
many of the available configuration parameters such as the ones shown below.

a) host
b) hostColocation
c) partitionColocation
d) placement
e) threadedPort and queue
f) relocatable and many more.

In addition, this example also shows how to make this application toolkit
dependent on another SPL toolkit project (025_dynamic_filter_at_work). 


Since this example demonstrates distributing the application across
multiple machines, it is better if you have Streams installed on more than one machine.
*/
namespace my.sample3;

use my.sample::Writer;

// This application puts almost all of the SPL configuration tags to work.
// The partition information and the host information are arbitrarily done here.
// The goal of all this is to simply exercise the configuration options.
//
// This application also has a dependency on another toolkit (025_dynamic_filter_at_work)
// Toolkit dependencies are added or removed by editing the toolkit information file
// (info.xml) using the SPL info model editor.
//
composite Main {
	type
		flightRecord = tuple<rstring flightNumber, rstring airline, 
			rstring sourceAirport, rstring destinationAirport,
			rstring departureTime, rstring arrivalTime, boolean mealService>;
	
	graph
		// Define a Beacon and apply certain configuration values.
		stream <flightRecord> BeaconedFlightRecord = Beacon() {
			param
				initDelay: 3.5f;
				iterations: 5000u;
			
			// Let us configure a few things.
			config
				checkpoint: periodic(3000.0);
				restartable: true;
				relocatable: false;
				placement: host(Pool1[0]), hostIsolation, partitionColocation("Beacon"), hostColocation("Beacon");			
		} // End of FlightRecord = Beacon()
		
		// Let us customize the Beaconed tuples.
		stream <flightRecord> FlightRecord = Custom(BeaconedFlightRecord) {
			logic
				state: {
					mutable uint32 cnt = 0;
					list<rstring> varFlightNumber = ["452", "928", "712", "629", "42", "626", "769"];
					list<rstring> varAirline = ["Iran Air", "American Airlines", "Continental", "Delta", "SouthWest", "United Airlines", "Jet Blue"];
					list<rstring> varSourceAirport = ["JFK", "Newark", "LAX", "DFW", "Midway", "Dulles", "Atlanta"];
					list<rstring> varDestinationAirport = ["San Diego", "Seattle", "Boston", "Minneapolis", "Denver", "Orlando", "Phoenix"];
					list<rstring> varDepartureTime = ["12:34:56", "05:38:12", "11:30:23", "18:45:25", "21:45:00", "23:12:34", "07:10:34"];
					list<rstring> varArrivalTime = ["16:23:45", "05:23:45", "07:23:34", "08:34:36", "23:15:23", "15:34:18", "05:36:15"];
					mutable uint32 varMealService = 0; 
					mutable tuple<flightRecord> result = {};  	
				} // End of state:
			
			onTuple BeaconedFlightRecord: { 
				cnt = ((uint32) (random()*100.0))%7u;
				
				// Alternate between meal service available and not..
				if (varMealService == 0u) {
					varMealService = 1u;
					result.mealService = false;
				} else {
					varMealService = 0u;
					result.mealService = true;
				}
				
			    result.flightNumber= varFlightNumber[cnt];
				result.airline = varAirline[cnt];
				result.sourceAirport = varSourceAirport[cnt];
				result.destinationAirport = varDestinationAirport[cnt];
				result.departureTime = varDepartureTime[cnt];
				result.arrivalTime = varArrivalTime[cnt];
				//Send this tuple away.
				submit(result, FlightRecord);
			} // End of onTuple: BeaconedFlightRecord
			
			// Let us configure this operator to be placed with the Beacon.
			config
				// Let us add a queue between the input and output ports of this operator.
				threadedPort: queue(BeaconedFlightRecord, Sys.DropFirst, 175);
				placement: partitionColocation("Beacon"), hostColocation("Beacon");
		} // End of FlightRecord = Custom(BeaconedFlightRecord)		
		
		// Define a Functor to filter certain airlines.
		stream <flightRecord> VettedFlightRecord = Functor(FlightRecord) {
			param
				filter: airline != "Iran Air";
			
			// Let us configure this operator.
			config
				relocatable: true;
				restartable: true;
				placement: host(Pool1[1]), partitionColocation("Part1");
				// Let us add a queue between the input and output ports of this operator.
				threadedPort: queue(FlightRecord, Sys.DropLast, 150);			
		} // End of VettedFlightRecord = Functor(FlightRecord)
		
		// Let us split the the Vetted Flight record according to the airline.
		(stream <flightRecord> AmericanFlightRecord;
		 stream <flightRecord> UnitedFlightRecord;
		 stream <flightRecord> DeltaFlightRecord;
		 stream <flightRecord> ContinentalFlightRecord;
		 stream <flightRecord> SouthWestFlightRecord;
		 stream <flightRecord> JetBlueFlightRecord) = Split(VettedFlightRecord) {
		 	param
		 		file: "AirlinesSplitter.txt";
		 		key: airline;
		 	
		 	config
		 		placement: partitionColocation("Part1");
		 		restartable: true;
		 		relocatable: true;
				// Let us add a queue between the input and output ports of this operator.
				threadedPort: queue(VettedFlightRecord, Sys.Wait, 100);		 		
		} // End of (...) = Split(VettedFlightRecord)
		
		// Let us add some custom operators to process the streams of the individual airline streams.
		() as ScreenWriter1 = Writer(AmericanFlightRecord) {
			param
				writerIdentifier: "a";
				matchType: "Flight";
				displayOwner: "American Airlines";
				
			// Let us keep all the Writer operators in their own partition	
			config
				placement: partitionIsolation, partitionExlocation("Writer"), host(Pool1[1]), hostColocation("WriterHostGroup1");
		} // End of ScreenWriter1 = Writer(AmericanFlightRecord)
		
		() as ScreenWriter2 = Writer(UnitedFlightRecord) {
			param
				writerIdentifier: "b";
				matchType: "Flight";
				displayOwner: "United Airlines";
				
			// Let us keep all the Writer operators in their own partition	
			config
				placement: partitionExlocation("Writer"), hostColocation("WriterHostGroup1");
		} // End of ScreenWriter2 = Writer(UnitedFlightRecord)

		() as ScreenWriter3 = Writer(DeltaFlightRecord) {
			param
				writerIdentifier: "c";
				matchType: "Flight";
				displayOwner: "Delta";
				
			// Let us keep all the Writer operators in their own partition	
			config
				placement: partitionExlocation("Writer"), host(Pool1[2]), hostColocation("WriterHostGroup2");
		} // End of ScreenWriter3 = Writer(DeltaFlightRecord)
 
		() as ScreenWriter4 = Writer(ContinentalFlightRecord) {
			param
				writerIdentifier: "d";
				matchType: "Flight";
				displayOwner: "Continental";
				
			// Let us keep all the Writer operators in their own partition	
			config
				placement: partitionExlocation("Writer"), hostColocation("WriterHostGroup2");
		} // End of ScreenWriter4 = Writer(ContinentalFlightRecord)

		() as ScreenWriter5 = Writer(SouthWestFlightRecord) {
			param
				writerIdentifier: "e";
				matchType: "Flight";
				displayOwner: "South West";
				
			// Let us keep all the Writer operators in their own partition	
			config
				placement: partitionExlocation("Writer"), host(Pool1[3]), hostColocation("WriterHostGroup3");
		} // End of ScreenWriter5 = Writer(SouthWestFlightRecord)
		
		() as ScreenWriter6 = Writer(JetBlueFlightRecord) {
			param
				writerIdentifier: "f";
				matchType: "Flight";
				displayOwner: "Jet Blue";
				
			// Let us keep all the Writer operators in their own partition	
			config
				placement: partitionExlocation("Writer"), hostColocation("WriterHostGroup3");
		} // End of ScreenWriter6 = Writer(JetBlueStreamFlightRecord)

	// Let us do the composite-level configurations.
	config
		applicationScope: "ConfigurationTest";
		defaultPoolSize: 3;
		// These host names may have to be changed with your own node names.
		hostPool: Pool1 = ["d0701b01", "d0701b02", "d0701b03", "10.6.24.114"],
			Pool2 = createPool({size = 5u, tags=["boeing", "airbus"]}, Sys.Exclusive);
		inputTransport: TCP;
		outputTransport: TCP;
		logLevel: error;
		relocatable: false;
}

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/029_spl_functions_at_work_my_sample_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/031_spl_mixed_mode_at_work_my_sample_Main_spl/"> > </a>
</div>

