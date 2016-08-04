---
layout: samples
title: 059_dynamic_scaleout_of_streams_application
---

### 059_dynamic_scaleout_of_streams_application

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/058_data_sharing_between_non_fused_spl_custom_and_cpp_primitive_operators_com_acme_test_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/059_dynamic_scaleout_of_streams_application_com_ibm_streams_pricing_test_DynamicScaleOut_spl/"> > </a>
</div>

~~~~~~
/*
==========================================================================
First created on: Nov/28/2011
Last modified on: Aug/17/2013
 
This SPL composite is the self contained application that makes up
the price calculation engine. This composite provides the
code for importing the price calculation requests coming from 
the DynamicScaleout composite. It also calls the C++ primitive operator
that encapsulates the price calculation code. Finally, this
composite exports the result stream coming from the pricer
operator. Binary code for this composite can be deployed and run in
parallel as multiple pricing engine instances on several machines.
But, this example is configured to scale multiple pricing engines across
several CPU cores on a single machine. This can be easily reconfigured
to run on individual server machines.

 This application is built, run, and stopped using bash script files.
 For complete details about building, running, and stopping this application,
 please look inside the file named "readme.txt" available at the root of the 
 "dynamic_scaleout" project directory.
==========================================================================
*/
// Perl Arguments in effect for mixed-mode processing
// Argument count: 0

namespace com.ibm.streams.pricing;



composite Pricer {
	type
		pricerData = tuple<uint32 tickerSequenceNumber, uint32 targettedPricerId, uint32 respondingPricerId, 
			timestamp tickerEntryTime, int64 tickerResidencyTimeFromSourceToSink, timestamp applicationStartTime,
			int64 totalProcessingTimeForAllTickers, timestamp tickerEntryTimeInsideThePricer, 
			int64 priceCalculationTimeForThisTicker, rstring hostName, float32 spotPrice,
			float32 price, float32 delta, float32 gamma, float32 theta, float32 vega, float32 aoxb, float32 rho>;
			
	graph
		// Let us import the PricerInput stream that is exported by 
		// the DynamicScaleOut job meant to be received by specific pricers via an export operator property.
		// These exported streams will carry an export property that will carry the pricerId for which each
		// exported stream is targeted to. In the pricer code here, every pricer will hook with a 
		// particular stream that is exported for it by subscribing to its pricer id. Streams runtime
		// will do the magic of matching up every subscription with the corresponding exported stream.
		// The match key here is the pricer id.
		//
		// Note
		// ---- 
		// Pricer id for every worker pricer is dynamically assigned at the time when that pricer job
		// is submitted using the "streamtool submitjob" command. There is a -P option that allows 
		// the job submitter to pass any key=value combination to the job.
		// For example, in our case it will be -P pricerId=15
		stream <pricerData> ImportedPricerInput = Import(){
			param
				// We will dynamically change this subscription value during runtime when this pricer job is started.
				// Whoever is going to submit this pricer Streams job, he or she or that (a script!!!) must
				// provide a submissionTimeValue named "pricerId". (e-g: pricerId=15)
				subscription: pricerInputForPricerId == "DummyPricerId";
		} // End of Import

		// Let us have a Beacon to send a signal to change the input port import subscription.
		stream<int32 subscriptionChangeSignal> ImportSubscriptionChangeSignal = Beacon() {
			param
				initDelay: 3.0;
				iterations: 1;
		} // End of ImportSubscriptionChangeSignal = Beacon()

		// Let us dynamically change the stream import subscription value to the
		// current pricer id assigned via a job submission parameter.
		stream <ImportedPricerInput> PricerInput = Custom(ImportSubscriptionChangeSignal as ISCS;
			ImportedPricerInput as IPI) {
			logic
				onTuple ISCS: {
					// Let us change the import subscription value to the 
					// pricerId to this pricer assigned during application launch time.
					mutable rstring _newSubscription = 
						"pricerInputForPricerId == " + getSubmissionTimeValue("pricerId");
					// Please note the use of 1u for the second parameter. It denotes that
					// we want to change the import subscription for our input port 1 which
					// receives the imported pricer input stream.
					int32 rc = setInputPortImportSubscription(_newSubscription, 1u);
		
					if (rc != 0) {
						// Log the error and abort the application.
						appTrc(Trace.error, "New Subscription=" + _newSubscription);
						appTrc(Trace.error, "SetInputPortImportSubscription API failed with return code " + (rstring)rc);
						abort();
					} // End of if (rc != 0)				
				}	
				
				onTuple IPI: {
					// Simply forward this imported stream via the correct output stream.
					submit(IPI, PricerInput);
				}
		}

		// Let us add a timestamp to indicate when the ticker entered here for price calculation.
		// That will aid us in calculating the queuing delays in the upstream operators.
		stream<pricerData> TimeStampedPricerInput = Functor(PricerInput) {
			param
				filter: true;
				
			output
				TimeStampedPricerInput: tickerEntryTimeInsideThePricer = getTimestamp();
		} // End of TimeStampedPricerInput = Functor(PricerInput)

		// Inovoke the price calculation C++ primitive operator that in turn wraps the 
		// price calculation C++ code.
		stream<pricerData> PricerResult = DummyPricer(TimeStampedPricerInput) {
		} // End of PricerResult = DummyPricer(PricerInput)

		// Before we send the pricer results back to the downstream operator,
		// let us calculate the time it took inside the pricer logic. 		
		stream<pricerData> PricerFinalResult = Custom(PricerResult as FDR) {
			logic
				onTuple FDR: {
					mutable pricerData fddTuple = FDR;
					fddTuple.respondingPricerId = (uint32)getSubmissionTimeValue("pricerId");
					fddTuple.hostName = getConfiguredHostName();
				    fddTuple.priceCalculationTimeForThisTicker = ((getSeconds(getTimestamp()) * (int64)1000000000) + (int64)getNanoseconds(getTimestamp())) - 
				                    							 ((getSeconds(FDR.tickerEntryTimeInsideThePricer) * (int64)1000000000) + (int64)getNanoseconds(FDR.tickerEntryTimeInsideThePricer));
			    	submit(fddTuple, PricerFinalResult);
				} // End of onTuple FDR
		} // End of PricerFinalResult = Custom(PricerResult as FDR)

		// Export the pricerResult stream so that the DynamicScaleOut composite can receive it to
		// do further processing.
		() as ExportedPricerResult = Export(PricerFinalResult) {
			param
				properties: {pricerResult = "Done"};			
		} // End of Export(PricerFinalResult)

	config
		// Place all the operators in this composite in a single PE and
		// place that PE (which is generally known as the pricing engine) on a 
		// user-specified host.
		placement: partitionColocation("pricerEngine"), host("pricer_dummy_machine");
} // End of composite Pricer

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/058_data_sharing_between_non_fused_spl_custom_and_cpp_primitive_operators_com_acme_test_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/059_dynamic_scaleout_of_streams_application_com_ibm_streams_pricing_test_DynamicScaleOut_spl/"> > </a>
</div>

