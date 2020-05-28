
You can ingest data from Kafka, RabbitMQ, files, Hadoop File System (HDFS), HBase, IoT devices, and more.  You will need to find the right source operator for your data.

The table below lists common data sources and the corresponding Streams operators.

|**Data source**     | **Operator**              | **Toolkit**               |
|---------------------|---------------------|--------------------------------------------|
|IBM  Event Streams (formerly Message Hub)           | MessageHubConsumer  |  [streamsx.messagehub](https://github.com/IBMStreams/streamsx.messagehub)  |
|-----------------------|-----------------------|---------------------------------------------|
| MQTT                  | MQTTSource            | [streamsx.mqtt](https://github.com/IBMStreams/streamsx.mqtt)         |
|-----------------------|-----------------------|----------------------------------------------|
| Kafka                 | KafkaConsumer         | [streamsx.kafka](https://github.com/IBMStreams/streamsx.kafka)        |
|-----------------------|-----------------------|----------------------------------------------|
| HDFS                  | HDFS2FileSource       | [streamsx.hdfs](https://github.com/IBMStreams/streamsx.hdfs)         |
|                       |                       |                       |
|                       | HDFS2DirectoryScan    |                       |
|-----------------------|-----------------------|----------------------------------------------|
| HBase                 | HBaseScan/HBaseGet    | [streamsx.hbase](https://github.com/IBMStreams/streamsx.hbase)       |
|-----------------------|-----------------------|--------------------------------------------|
| Any JDBC compliant RDBMS   | JDBCRun               | [streamsx.jdbc](https://github.com/IBMStreams/streamsx.jdbc)         |
|-----------------------|-----------------------|------------------------------------|
| JMS              | JMSSource             | [streamsx.jms](https://github.com/IBMStreams/streamsx.jms)  |                     
|-----------------------|-----------------------|-----------------------|
|------------------------| --------------------| ---------------------- |


### Existing tutorials

* [Connect to Apache Kafka using the Kafka toolkit](/streamsx.documentation/docs/messaging/kafka-operators-getting-started)

* [Get started with the JMS toolkit](/streamsx.documentation/docs/messaging/kafka-operators-getting-started)

* [Connect to IBM Event Streams (formerly MessageHub)](https://www.ibm.com/cloud/blog/get-started-streaming-analytics-message-hub)
  
View the full list of [supported toolkits in the Streaming Analytics service](https://cloud.ibm.com/docs/services/StreamingAnalytics/compatible_toolkits.html#compatible_toolkits) and in a [local install](https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.toolkits.doc/spldoc/dita/toolkits/toolkits.html).