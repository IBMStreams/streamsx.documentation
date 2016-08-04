---
layout: samples
title: 086_jms_source_sink_using_activemq
---

### 086_jms_source_sink_using_activemq

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/085_user_defined_parallelism_12_com_acme_test_UDP12_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/087_email_alerts_via_java_native_function_com_acme_test_EmailAlerts_spl/"> > </a>
</div>

~~~~~~
/*
This example shows how Streams can be used to write to the Apache ActiveMQ queues and
then read from those queues.  It employs two operators (JMSSource and JMSSink) from the
Streams messaging toolkit to demonstrate how Streams can work with ActiveMQ.
 
In order to test this example, please ensure you have done the following steps.

1) Download ActiveMQ 5.7 from here: http://activemq.apache.org/download-archives.html
   (apache-activemq-5.7.0-bin.tar.gz)

2) Unzip the downloaded tar.gz file in your home directory. That is it. 
   Your ActiveMQ installation is done.

3) Now change directory to the ActiveMQ directory (apache-activemq-5.7.0)

4) Start ActiveMQ:  ./bin/activemq start

5a) Point your Linux Firefox browser here and see it takes you to the 
    ActiveMQ admin console:  http://localhost:8161/admin
 
5b) Another way to check the running instance of your Active MQ is where you can run the 
     following command:
     netstat -an | grep -i 61616
     
     If you see a process with this TCP address, then your Active MQ is
     running fine. Otherwise, it is not.

6) If step (5) worked fine, then you may stop ActiveMQ: ./bin/activemq stop
   (OR) you may want to keep it running to test this example.

7) In order for this example to work, please ensure you have the following environment
   variable set to your Active MQ installation directory in your .bashrc file when you
   started the Stream Studio:

   export STREAMS_MESSAGING_AMQ_HOME=<Full path to your Active MQ install directory>
  
8) If your Active MQ is running on a different machine from this example, then you
   are required to edit the ./etc/connections.xml file in this example project and
   change all the occurrences of localhost with the correct machine name where your
   Active MQ instance is running.   

9) In the Streams Explorer view of your Streams Studio, you must add the messaging
   toolkit directory location so that it points to $STREAMS_INSTALL/toolkits/com.ibm.streams.messaging
   That step is required to satisfy the compiler dependency on the messaging toolkit.
 
After ensuring all the steps mentioned above, you will be able to run this example either
from within the Streams Studio or from a Linux terminal window.
*/

namespace com.acme.test;

use com.ibm.streamsx.messaging.jms::*;

composite JMSSourceSink {
	type
		FlightData = tuple<rstring carrier, rstring model, int32 tarmacId, rstring arrivingFrom, int32 gateNumber, int32 passengerCnt>;
		
	graph
		// Let us generate test data.
		stream<FlightData> MyFlightData = Beacon() {
			param
				iterations: 10u;
				initDelay: 7.0;
		}
		
		// Enrich the flight data.
		stream<FlightData> EnrichedFlightData = Custom(MyFlightData as MFD) {
			logic
				state: {
					mutable int32 _tupleCnt = 0;
				}
				
			onTuple MFD: {
				_tupleCnt++;
				mutable EnrichedFlightData oTuple = {};
				
				if (_tupleCnt == 1) {
					oTuple = {carrier="American", model="Boeing 747", tarmacId=5, arrivingFrom="LAX", gateNumber=5, passengerCnt=178};
				} else if (_tupleCnt == 2) {
					oTuple = {carrier="Delta", model="Boeing 757", tarmacId=8, arrivingFrom="EWR", gateNumber=7, passengerCnt=195};
				} else if (_tupleCnt == 3) {
					oTuple = {carrier="British Airways", model="Airbus 320", tarmacId=14, arrivingFrom="LHR", gateNumber=8, passengerCnt=195};
				} else if (_tupleCnt == 4) {
					oTuple = {carrier="United", model="Boeing 757", tarmacId=11, arrivingFrom="JFK", gateNumber=10, passengerCnt=153};
				} else if (_tupleCnt == 5) {
					oTuple = {carrier="Singapore Airlines", model="Boeing 757", tarmacId=2, arrivingFrom="SIN", gateNumber=17, passengerCnt=212};
				} else if (_tupleCnt == 6) {
					oTuple = {carrier="Eva Air", model="Airbus 320", tarmacId=6, arrivingFrom="TPE", gateNumber=34, passengerCnt=194};
				} else if (_tupleCnt == 7) {
					oTuple = {carrier="Lufthansa", model="Airbus 320", tarmacId=23, arrivingFrom="FRA", gateNumber=15, passengerCnt=176};
				} else if (_tupleCnt == 8) {
					oTuple = {carrier="Japan Airlines", model="Boeing 757", tarmacId=19, arrivingFrom="HND", gateNumber=4, passengerCnt=168};
				} else if (_tupleCnt == 9) {
					oTuple = {carrier="Southwest", model="Boeing 737", tarmacId=31, arrivingFrom="ORD", gateNumber=12, passengerCnt=135};
				} else if (_tupleCnt == 10) {
					oTuple = {carrier="Air Tran", model="Boeing 737", tarmacId=34, arrivingFrom="BOS", gateNumber=18, passengerCnt=126};
				} 
			
				submit(oTuple, EnrichedFlightData);
			}
		}
		
		// Send it to the Active MQ's queue.
		// We are using the easiest possible configuration by
		// using dynamicQueues/MapQueue. (Please refer to ./etc/connections.xml file)
		// If needed, we can also use ActiveMQ's dynamicTopics/myTopic
		// 
		// In a standard messaging platform, queues will load balance messages across 
		// multiple consumers and topics will broadcast messages to all active subscribers.
		() as MyJmsSink1 = JMSSink(EnrichedFlightData) {
			param
				// connectionDocument: default is ./etc/connections.xml
				connection: "flightConnection1";
				access: "flightAccess1";
		}
		
		// Have a JMS Source operator read from the active MQ's queue.
		stream<FlightData> QueuedFlightData = JMSSource() {
			param
				// connectionDocument: default is ./etc/connections.xml
				connection: "flightConnection1";
				access: "flightAccess1";		
		}
		
		// Let us display the messages read from the Active MQ on the console screen.
		() as MySink1 = Custom(QueuedFlightData as QFD) {
			logic
				onTuple QFD: {
					printStringLn((rstring)QFD);
				}
		}
}

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/085_user_defined_parallelism_12_com_acme_test_UDP12_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/087_email_alerts_via_java_native_function_com_acme_test_EmailAlerts_spl/"> > </a>
</div>

