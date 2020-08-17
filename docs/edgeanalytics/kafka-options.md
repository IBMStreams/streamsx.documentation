---
layout: docs
title: Apache Kafka options for edge applications
navtitle: Apache Kafka options for edge applications
description:  Installing IBM® Streams Runner for Apache Beam involves downloading and extracting the Streams Runner toolkit, configuring environment variables, and creating a credentials file for your Streaming Analytics service.
weight:  10
published: true
tag: edge
---

This document provides different Apache Kafka options available to users developing edge applications.

Apache Kafka allows users to publish and subscribe to streams of records, similar to a message queue or enterprise messaging system. This makes it an effective tool for edge solutions to pass data from sensors and systems close to the edge to a large data processing system in a private or public cloud.

The rest of this document will cover how to install and deploy several flavors of Kafka and how to connect to the those deployments in IBM Streams applications using the `streamsx.kafka` or `streamsx.messagehub` toolkit.

## Before you begin: Streams application development

* **Python developers**: use the [`streamsx.kafka` Python package](https://streamsxkafka.readthedocs.io/en/latest/) regardless of Kafka deployment. Usage of `streamsx.eventstreams` is not recommended because it is no longer updated.

* **SPL developers**: use the `KafkaConsumer` and `KafkaProducer` operators in the [`streamsx.kafka` toolkit](https://ibmstreams.github.io/streamsx.kafka) for all Kafka deployments other than IBM Event Streams. For users planning to use IBM Event Streams, use the [`streamsx.messagehub` toolkit](https://ibmstreams.github.io/streamsx.messagehub/) instead.

***

## Using an existing Kafka deployment

If you already has a Kafka environment ready, use that environment by [configuring](https://ibmstreams.github.io/streamsx.kafka/docs/user/overview/) your `KafkaConsumer` and `KafkaProducer` operators and your property file for the Streams application to access the existing Kafka environment.

* **Python applications**: see [Connection examples](https://streamsxkafka.readthedocs.io/en/latest/#connection-examples).
* **SPL applications**: see [`streamsx.kafka` samples](https://ibmstreams.github.io/streamsx.kafka/docs/user/overview/#samples).

***

## Red Hat [AMQ Streams](https://access.redhat.com/products/red-hat-amq#streams)

Red Hat's version of the Apache Kafka and Strimzi projects which simplifies the process of running Apache Kafka in an OpenShift cluster.

For a full overview of AMQ Streams and Kafka concepts and architecture, see the [AMQ Streams overview documentation](https://access.redhat.com/documentation/en-us/red_hat_amq/7.6/html-single/amq_streams_on_openshift_overview/index)

### Installing and deploying AMQ Streams

AMQ Streams can be installed and deployed in the following environments:

* [OpenShift Container Platform 3.11 and 4.x](https://access.redhat.com/documentation/en-us/red_hat_amq/7.6/html/using_amq_streams_on_openshift/overview-str#con-streams-installation-methods_str)
* [Red Hat Enterprise Linux](https://access.redhat.com/documentation/en-us/red_hat_amq/7.6/html/using_amq_streams_on_rhel/index)

See their respective links for instructions on how to download, install, and deploy AMQ Streams.

### Quick Start for OpenShift 4.3

1. Go to the `OperatorHub` in the OCP console.
1. Select the installation mode to be a specific namespace.
1. Select a namespace where the AMQ Streams deployment will be (e.g. amq-streams).
    * If you need to create a new namespace, create a new project via the OCP console, or via CLI by running `oc new-project amq-streams`.
1. Click 'Subscribe' and wait for the AMQ Streams operator to be installed.
1. Once installed, click on the operator and click on 'Create Instance' for a 'Kafka' resource
1. Edit the YAML to add a route, change the name, or set the storage type of the Kafka or Zookeeper deployments
    1. Under `.spec.kafka.listeners`, add

       ```yaml
       external:
         type: route
       ```

    * The default YAML will create an emphimeral Kafka cluster named 'my-cluster'
    * If you need a persistent cluster, see the [AMQ Streams doc](https://access.redhat.com/documentation/en-us/red_hat_amq/7.6/html-single/using_amq_streams_on_openshift/index#assembly-storage-deployment-configuration-kafka) for more info.
1. Once done editing the Kafka YAML, click 'Create'.
1. Return back to the AMQ Streams Operator, click on 'Kafka Topic', and click 'Create KafkaTopic'
1. Set the name, partitions, and config for the topic as desired
1. Click 'Create'

### Connecting to AMQ Streams

1. In a terminal, run the commands below to get certificates and keystores necessary to connect:

    ```sh
    # Get Kafka bootstrap route; value will be referred to as <RouteURL> later
    oc get routes my-cluster-kafka-bootstrap -n amq-streams -o=jsonpath='{.status.ingress[0].host}{"\n"}'

    # Extract server public cert, client public cert, and client private key
    oc extract secret/my-cluster-cluster-ca-cert -n amq-streams --keys=ca.crt --to=- > ca.crt
    oc extract secret/my-cluster-client-ca-cert -n amq-streams --keys=ca.crt --to=- > user.crt
    oc extract secret/my-cluster-client-ca -n amq-streams --keys=ca.key --to=- > user.key
    ```

1. Use the methods depending on application type:

    * **Python applications**: use the [`streamsx-kafka-make-properties` command](https://ibmstreams.github.io/streamsx.kafka/docs/user/UsingRHAmqStreams/#when-you-have-a-python3-environment) to create a properties file.
    * **SPL applications**:

        1. Create the truststore and keystore manually:

            ```sh
            keytool -import -trustcacerts -alias root -file ca.crt -keystore truststore.jks -storepass trustpassword -noprompt

            openssl pkcs12 -export -in user.crt -inkey user.key -name client-alias -out ./keystore.pkcs12 -noiter -nomaciter -passout keypassword

            keytool -importkeystore -deststorepass password -destkeystore ./keystore.jks -srckeystore ./keystore.pkcs12 -srcstoretype pkcs12 -srcstorepass keypassword
            ```

        1. Populate a `kafka.properties` file with the following values:

            ```properties
            bootstrap.servers=<RouteURL>
            security.protocol=SSL
            ssl.keystore.type=JKS
            ssl.keystore.password=keypassword
            ssl.key.password=keypassword
            ssl.keystore.location={applicationDir}/etc/keystore.jks
            ssl.endpoint.identification.algorithm=https
            ssl.truststore.type=JKS
            ssl.truststore.password=trustpassword
            ssl.truststore.location={applicationDir}/etc/truststore.jks
            ```

        1. Copy the JKS files and `kafka.properties` to `etc/` in the SPL application workspace

For more information, see [Using streamsx.kafka with Red Hat AMQ Streams](https://ibmstreams.github.io/streamsx.kafka/docs/user/UsingRHAmqStreams/) documentation.

***

## Event Streams in IBM Cloud

[IBM Event Streams](https://www.ibm.com/cloud/event-streams) builds on top of open source Apache Kafka to offer enterprise-grade event streaming capabilities.

### Provisioning Event Streams

1. Log in to [IBM Cloud](https://cloud.ibm.com) or create an account if you do not have one.
1. Visit [Event Streams](https://cloud.ibm.com/catalog/services/event-streams) in the catalog.
1. Select a region (e.g. Dallas, Frankfurt)
1. Select a plan (e.g. Lite).
   * **Important**: The Lite plan only allows one topic which may not be enough for some samples to work.
1. Enter in a service name (e.g. Event Streams for Edge)
1. Click 'Create'

### Creating credentials and a topic

1. Go to 'Service credentials' in the navigation pane.
1. Click 'New credential'.
1. Give the credential a name so you can identify its purpose later. You can accept the default value.
1. Give the credential the Manager role so that it can access the topics, and create them if necessary.
1. Click 'Add'. The new credential is listed in the table in Service credentials.
1. For the newly created credentials, click the 'Copy to clipboard' icon.
1. Go to the Topics tab.
1. Go to 'Manage' in the navigation pane.
1. Click 'Create a topic'
1. Name your topic.
1. Keep the defaults set in the rest of the topic creation, click 'Next' and then 'Create topic'.

For any questions or details regarding Event Streams, see the [Event Streams documentation](https://cloud.ibm.com/docs/EventStreams?topic=EventStreams-getting_started#getting_started) for more information.

### Connecting to Event Streams

Use the copied credentials to save them to a file or create a [Streams application config](https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.admin.doc/doc/creating-secure-app-configs.html) with the credentials:

* **Python applications**: see [Connecting with the IBM Event Streams cloud service](https://streamsxkafka.readthedocs.io/en/latest/#connection-with-the-ibm-event-streams-cloud-service).
* **SPL applications**: see [`streamsx.messagehub` samples](https://ibmstreams.github.io/streamsx.messagehub/docs/user/overview/#samples) for connection configuration options.

***

## Vanilla Apache Kafka

Apache Kafka can be deployed on bare-metal or VM systems as well as Kubernetes, or OpenShift environments. Edge applications can leverage these Kafka installations; however, the edge systems where the edge application will be running must be able to connect to the system or environment where Kafka is running. Additionally, any cloud services or applications that consume Kafka topics must be able to access the system or environment.

Because users should already have access to a Kubernetes-like environment, the following install section will cover Helm charts and Operators to deploy Kafka servers.

### Installing and deploying Kafka

#### Helm

1. Download the latest [Helm 3 release](https://github.com/helm/helm/releases/latest)
1. Follow the [instructions for the Bitnami Kakfa Helm charts](https://hub.helm.sh/charts/bitnami/kafka)

#### Kubernetes Operator

To deploy Kafka using a Kubernetes operator, use the Strimzi Kafka Operator [here](https://operatorhub.io/operator/strimzi-kafka-operator).

Setup and configuration is nearly identical to [AMQ Streams](#red-hat-amq-streams). For full information, visit the [Strimzi doc](https://strimzi.io/docs/operators/latest/full/using.html#overview-str).

### Connecting to Kafka

* **Python applications**: see [Connection examples](https://streamsxkafka.readthedocs.io/en/latest/#connection-examples).
* **SPL applications**: see [`streamsx.kafka` samples](https://ibmstreams.github.io/streamsx.kafka/docs/user/overview/#samples).

## What to do next?

Build and test your application using your Streams service instance in Cloud Pak for Data. Once your application is ready to be built as an edge application, see [Building an edge application](https://www.ibm.com/support/knowledgecenter/SSQNUZ_3.0.1/svc-edge/developing-build.html) for more information.
