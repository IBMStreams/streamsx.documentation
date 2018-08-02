---
layout: docs
title:  I/O sample applications for IBM Streams Runner for Apache Beam
navtitle: I/O sample apps
description:  You can use sample applications to learn how to use IBM Message Hub for input and output.
weight:  10
published: true
tag: beam
prev:
  file: objstor
  title: FileStreamSample sample app
next:
  file: monitor
  title: Monitoring
---

You can use the IBM® Streams Runner for Apache Beam I/O sample applications to learn how to use IBM Message Hub® for input and output. Message Hub sample applications are provided in the `$STREAMS_RUNNER_HOME/examples/io`directory.

## Before you start

Before you run the Apache Beam 2.4 I/O sample applications, you must configure and run the following service on IBM Cloud®:

- IBM Message Hub.
   - Create the service if you don't already have one. For more information, see [Creating a Message Hub service on IBM Cloud](../io/#creating-a-message-hub-service-on-ibm-cloud).
   - Set up credentials for the service. **Remember**: Make sure the environment variables are configured. For more information, see [Setting up credentials for the Message Hub  service](../io/#setting-up-credentials-for-the-message-hub-service).

## Running the sample application

1. Go to the `$STREAMS_RUNNER_HOME/examples/io` directory.
2. In the `io` directory, compile the I/O sample apps into an uber JAR file by entering the following command:

    `mvn package`

    The `beam-examples-io-<runner-version>.jar` uber JAR file is generated in the `$STREAMS_RUNNER_HOME/examples/io/target` directory.
3. Start the producer by running the following command:
   ```
   java -cp $STREAMS_BEAM_TOOLKIT/lib/com.ibm.streams.beam.translation.jar:$STREAMS_INSTALL/lib/com.ibm.streams.operator.samples.jar:target/beam-examples-io-<runner-version>.jar \
        com.ibm.streams.beam.examples.io.mh.Producer\
        --runner=StreamsRunner \
        --contextType=DISTRIBUTED \
        --jarsToStage=target/beam-examples-io-<runner-version>.jar \
        --topic=<your message hub topic> \
        --cred=<path to the message hub credential file>
  ```
4. Start the consumer by running the following command:
  ```
  java -cp $STREAMS_BEAM_TOOLKIT/lib/com.ibm.streams.beam.translation.jar:$STREAMS_INSTALL/lib/com.ibm.streams.operator.samples.jar:target/beam-examples-io-<runner-version>.jar \
        com.ibm.streams.beam.examples.io.mh.Consumer\
        --runner=StreamsRunner \
        --contextType=DISTRIBUTED \
        --jarsToStage=target/beam-examples-io-<runner-version>.jar \
        --topic=<your message hub topic> \
        --cred=<path to the message hub credential file>
  ```
5. If both the producer and the consumer are running correctly, the consumer prints numbers to `System.out`, one integer per line.
