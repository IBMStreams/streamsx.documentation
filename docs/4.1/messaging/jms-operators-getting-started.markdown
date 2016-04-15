---
layout: docs
title: Getting Started with JMS operators
description:  Getting Started Guide for IBM Streams Messaging Toolkit - JMS operators
weight: 10
---

## Introduction
IBM  Streams messaging toolkit provides several operators allowing users to source and sink messages from and to different types of messaging systems. This article will focus on explaining how to configure JMS operators to work with either WebSphere MQ or ActiveMQ messaging systems.

## Skill Level
Readers of this article is expected to have basic understanding in JMS and WebSphere MQ or ActiveMQ.

## Requirements
Prior to using JMS operators, the following software must be installed and configured.

-  Streams - a quick start edition VM is available, see the [Installing Streams Quick Start Edition VM Image](http://ibmstreams.github.io/streamsx.documentation//docs/4.1/qse-install-vm/) for more information.
- Messaging Toolkit - a official version of the toolkit is shipped with  Streams or download it from [IBM Streams Github Messaging Toolkit Repository](https://github.com/IBMStreams/streamsx.messaging)
- Messaging server and client - JMS operators supports both WebSpehre MQ and ActiveMQ, depending on the target messaging system, install either WebSphere MQ or ActiveMQ. If  Streams is running on a different machine than messaging server, install WebSphere MQ client libraries for Java or ActiveMQ on the same machine where  Streams is running as JMS operators looks up certain jar files from these messaging clients at runtime.
  - WebSphere MQ: a trial version of [WebSphere MQ](https://www-01.ibm.com/marketing/iwm/iwm/web/pick.do?pkgid=&S_SRCID=ESD-WSMQ-EVAL&source=ESD-WSMQ-EVAL&S_TACT=109J84RW&S_PKG=CR9H9ML&lang=en_US&lang=en_US) is available.
  - ActiveMQ: download a supported version of [ActiveMQ](http://activemq.apache.org/download.html)
- Bindings file (WebSphere MQ only) – see [Example - create WebSphere MQ objects and bindings file](../mq-create-objects-bindings-sample/).

## Information to collect
Information about provider_url, connection_factory and destination identifier must be collected. These information will be entered into connections document for JMS operators to establish connection to message system.

- WebSphere MQ:
  - provider_url is the directory where the .bindings file is stored.
  - connection_factory is the name used when defining QCF via JMSAdmin tool, i.e confact.
  - destination identifier is the name used when defining the Q via JMSAdmin tool, i.e dest.

- ActiveMQ:
  - provider_url is typically a string starting with tcp protocal i.e tcp://hostname:port.
  - connection_factory use default name ConnectionFactory.
  - destination identifier is the name of the queue or topic.

## Steps
1. Set environment variable that is required by JMS operators.
   * *WebSphere MQ*

     `echo "export STREAMS_MESSAGING_WMQ_HOME=/opt/mqm" >> /home/streamsadmin/.bashrc`

   * *ActiveMQ*

     `echo "export STREAMS_MESSAGING_AMQ_HOME=/home/streamsuser/ApacheActiveMQ" >> /home/streamsadmin/.bashrc`
2. Configure the SPL compiler to find the messaging toolkit directory. Use one of the following methods.
   * *Set the STREAMS_SPLPATH environment variable to the root directory of a toolkit or multiple toolkits (with : as a separator)*

     `echo "export STREAMS_SPLPATH=$STREAMS_INSTALL/toolkits/com.ibm.streamsx.messaging" >> /home/streamsadmin/.bashrc`

   * *Specify the -t or --spl-path command parameter when you run the sc command.*

     `sc -t $STREAMS_INSTALL/toolkits/com.ibm.streamsx.messaging -M MyMain`

   * *If  Streams Studio is used to compile and run SPL application, add messaging toolkit to toolkit locations in Streams Explorer.*
3. Source .bashrc and verify the appropriate environment variable is set for the messaging system you use.
   * *Source .bashrc*

     `source $HOME/.bashrc`

   * *Verify required environment variable*

     `env | grep STREAMS_MESSAGING_AMQ_HOME` for ActiveMQ

     `env | grep STREAMS_MESSAGING_WMQ_HOME` for WebSphere MQ
4. Start  Streams domain and instance.
5. Create a connections.xml file, which will be used by JMS operators to establish connection to messaging system. You can name this file anything you like. Replace the value for provider_url, connection_factory and destination identifier with the actual value you obtained earlier. For example

   * *Sample connection document for WebSphere MQ*

   <pre class="terminal">
    <span class="output">&lt;?xml version="1.0" encoding="UTF-8"?&gt;
	&lt;st:connections xmlns:st="http://www.ibm.com/xmlns/prod/streams/adapters"
                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"&gt;
		&lt;connection_specifications&gt;
			&lt;connection_specification name="wmq"&gt;
				&lt;JMS initial_context="com.sun.jndi.fscontext.RefFSContextFactory" provider_url = "file:///homes/streamsadmin/bindings" connection_factory="confact"/&gt;
			&lt;/connection_specification&gt;
		&lt;/connection_specifications&gt;
		&lt;access_specifications&gt;
			&lt;access_specification name="access_wmq"&gt;
				&lt;destination identifier="dynamicQueues/STREAMS.MapQueue" delivery_mode="persistent" message_class="map" /&gt;
				&lt;uses_connection connection="wmq"/&gt;
				&lt;native_schema&gt;
			    	&lt;attribute name="id" type="Int" /&gt;
			    	&lt;attribute name="name" type="String" length="15" /&gt;
				&lt;/native_schema&gt;
			&lt;/access_specification&gt;
		&lt;/access_specifications&gt;  
	&lt;/st:connections&gt;</span></pre>

   * *Sample connection document for ActiveMQ*

   <pre class="terminal">
    <span class="output">&lt;?xml version="1.0" encoding="UTF-8"?&gt;
	&lt;st:connections xmlns:st="http://www.ibm.com/xmlns/prod/streams/adapters"
                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"&gt;
		&lt;connection_specifications&gt;
			&lt;connection_specification name="activemq"&gt;
				&lt;JMS initial_context="org.apache.activemq.jndi.ActiveMQInitialContextFactory" provider_url = "tcp://activeMqHost:port" connection_factory="ConnectionFactory"/&gt;
			&lt;/connection_specification&gt;
		&lt;/connection_specifications&gt;
		&lt;access_specifications&gt;
			&lt;access_specification name="access_activemq"&gt;
				&lt;destination identifier="dynamicQueues/STREAMS.MapQueue" delivery_mode="persistent" message_class="map" /&gt;
				&lt;uses_connection connection="activemq"/&gt;
				&lt;native_schema&gt;
			    	&lt;attribute name="id" type="Int" /&gt;
			    	&lt;attribute name="name" type="String" length="15" /&gt;
				&lt;/native_schema&gt;
			&lt;/access_specification&gt;
		&lt;/access_specifications&gt;  
	&lt;/st:connections&gt;</span></pre>

   See more details about [connection document](http://ibmstreams.github.io/streamsx.messaging/com.ibm.streamsx.messaging/doc/spldoc/html/tk$com.ibm.streamsx.messaging/tk$com.ibm.streamsx.messaging$2.html)
6. Create a SPL application and add JMS operator to it. Make sure the “use” directive is present in the SPL source file. If  Streams Studio is used, these directive is automatically added when dragging and dropping a JMS operator to SPL application.

   `use com.ibm.streamsx.messaging.jms::*;`

   or

   `use com.ibm.streamsx.messaging.jms::JMSSink;`

   `use com.ibm.streamsx.messaging.jms::JMSSource;`

7. At minimum, both JMSSink and JMSSource operators requires two parameters to be specified namely “access” and “connection”, they are respectively referring to the name of access_specification and connection_specification elements in the connection document.

   Please note that the attribute name, type and their order defined in streams schema for JMS operator must match the attribute name, type and order defined in native_schema section of connection document. See all [supported native attribute type and mapping to SPL type](http://ibmstreams.github.io/streamsx.messaging/com.ibm.streamsx.messaging/doc/spldoc/html/tk$com.ibm.streamsx.messaging/tk$com.ibm.streamsx.messaging$12.html)

    <pre>
    stream<int32 id, rstring name> myInputStream = JMSSource()
    {
	    param
	    	connection : "wmq" ;
	    	access : "access_wmq" ;
    }
    </pre>

    Another important optional parameter is the connectionDocument, the value of this parameter tells JMS operators where to locate the connection document. Below are supported scenarios for placing connection document in a SPL application for JMS operators.

    * *Default case*: by default, if connectionDocument parameter is not present for the JMS operator, then it is assumed that a file named "connections.xml" under etc directory of the SPL application will be used.
    * *Absolute path*: the connection document can be placed outside of a SPL application, in this case specify the full path to the connection document as value of connectionDocument parameter, for example, `connectionDocument: "/path/to/connection.xml";`.
    * *Relative path*: relative path is also supported only if the connection document resides inside of the SPL application. For example a connection file named "myConnections.xml" is placed under etc directory of a SPL application, then specify `connectionDocument: "./etc/myConnections.xml";`.

8. Build your SPL application. You can use the `sc` command or let  Studio build it.
9. Run the application. You can submit the application as a job by using the `streamtool submitjob` command or by using Streams Studio.

## Additional Resources
* [IBM MQ Knowledge Center](http://www-01.ibm.com/support/knowledgecenter/SSFKSJ_8.0.0/com.ibm.mq.helphome.v80.doc/WelcomePagev8r0.htm)
* [ActiveMQ website](http://activemq.apache.org/)
* [ Streams Messaging Toolkit SPLDoc](http://ibmstreams.github.io/streamsx.messaging/com.ibm.streamsx.messaging/doc/spldoc/html/index.html)
