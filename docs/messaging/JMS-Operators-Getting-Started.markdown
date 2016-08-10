## Introduction
IBM  Streams messaging toolkit provides several operators allowing users to source and sink messages from and to different types of messaging systems. This article will focus on explaining how to configure JMS operators to work with either WebSphere MQ or ActiveMQ messaging systems.

## Skill Level
Readers of this article is expected to have basic understanding in JMS and WebSphere MQ or ActiveMQ.

## Requirements
Prior to using JMS operators, the following software must be installed and configured.

-  Streams - a quick start edition VM is available, see the [Installing Streams Quick Start Edition VM Image](../4.1/Install-VM) for more information.
- Messaging Toolkit - a official version of the toolkit is shipped with  Streams or download it from [IBM Streams Github Messaging Toolkit Repository](https://github.com/IBMStreams/streamsx.messaging)
- Messaging server and client - JMS operators supports both WebSpehre MQ and ActiveMQ, depending on the target messaging system, install either WebSphere MQ or ActiveMQ. If  Streams is running on a different machine than messaging server, install WebSphere MQ client libraries for Java or ActiveMQ on the same machine where  Streams is running as JMS operators looks up certain jar files from these messaging clients at runtime.
  - WebSphere MQ: a trial version of [WebSphere MQ](https://www-01.ibm.com/marketing/iwm/iwm/web/pick.do?pkgid=&S_SRCID=ESD-WSMQ-EVAL&source=ESD-WSMQ-EVAL&S_TACT=109J84RW&S_PKG=CR9H9ML&lang=en_US&lang=en_US) is available.
  - ActiveMQ: download a supported version of [ActiveMQ](http://activemq.apache.org/download.html)
- Bindings file (WebSphere MQ only) – see [Example - create WebSphere MQ objects and bindings file](MQ-Create-Object-Binding-Guide).

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
*  Set environment variable that is required by JMS operators.

&nbsp;&nbsp;&nbsp;&nbsp;WebSphere MQ

```bash
echo "export STREAMS_MESSAGING_WMQ_HOME=/opt/mqm" >> /home/streamsadmin/.bashrc
```
&nbsp;&nbsp;&nbsp;&nbsp;ActiveMQ

```bash
echo "export STREAMS_MESSAGING_AMQ_HOME=/home/streamsuser/ApacheActiveMQ" >> /home/streamsadmin/.bashrc
```

*  Configure the SPL compiler to find the messaging toolkit directory. Use one of the following methods.

&nbsp;&nbsp;&nbsp;&nbsp;Set the STREAMS_SPLPATH environment variable to the root directory of a toolkit or multiple toolkits (with : as a separator)*

```bash
echo "export STREAMS_SPLPATH=$STREAMS_INSTALL/toolkits/com.ibm.streamsx.messaging" >> /home/streamsadmin/.bashrc
```

&nbsp;&nbsp;&nbsp;&nbsp;Specify the -t or --spl-path command parameter when you run the sc command.*

     `sc -t $STREAMS_INSTALL/toolkits/com.ibm.streamsx.messaging -M MyMain`

&nbsp;&nbsp;&nbsp;&nbsp; **Note:** If  Streams Studio is used to compile and run SPL application, add messaging toolkit to toolkit locations in Streams Explorer.

* Source .bashrc and verify the appropriate environment variable is set for the messaging system you use.
    * Source .bashrc: `source $HOME/.bashrc`

    * Verify required environment variables
```bash
    # For ActiveMQ
    env | grep STREAMS_MESSAGING_AMQ_HOME
    # For WebSphere MQ
    env | grep STREAMS_MESSAGING_WMQ_HOME
```

* Start  Streams domain and instance.

* Create a connections.xml file, which will be used by JMS operators to establish connection to messaging system. You can name this file anything you like. Replace the value for provider_url, connection_factory and destination identifier with the actual value you obtained earlier. For example


&nbsp;&nbsp;&nbsp;&nbsp;**Sample connection document for WebSphere MQ**
```xml
<?xml version="1.0" encoding="UTF-8"?>
	<st:connections xmlns:st="http://www.ibm.com/xmlns/prod/streams/adapters"
                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
		<connection_specifications>
			<connection_specification name="wmq">
				<JMS initial_context="com.sun.jndi.fscontext.RefFSContextFactory" provider_url = "file:///homes/streamsadmin/bindings" connection_factory="confact"/>
			</connection_specification>
		</connection_specifications>
		<access_specifications>
			<access_specification name="access_wmq">
				<destination identifier="dynamicQueues/STREAMS.MapQueue" delivery_mode="persistent" message_class="map" />
				<uses_connection connection="wmq"/>
				<native_schema>
			    	<attribute name="id" type="Int" />
			    	<attribute name="name" type="String" length="15" />
				</native_schema>
			</access_specification>
		</access_specifications>  
	</st:connections>
```

&nbsp;&nbsp;&nbsp;&nbsp;**Sample connection document for ActiveMQ**

```xml
<?xml version="1.0" encoding="UTF-8"?>
	<st:connections xmlns:st="http://www.ibm.com/xmlns/prod/streams/adapters"
                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
		<connection_specifications>
			<connection_specification name="activemq">
				<JMS initial_context="org.apache.activemq.jndi.ActiveMQInitialContextFactory" provider_url = "tcp://activeMqHost:port" connection_factory="ConnectionFactory"/>
			</connection_specification>
		</connection_specifications>
		<access_specifications>
			<access_specification name="access_activemq">
				<destination identifier="dynamicQueues/STREAMS.MapQueue" delivery_mode="persistent" message_class="map" />
				<uses_connection connection="activemq"/>
				<native_schema>
			    	<attribute name="id" type="Int" />
			    	<attribute name="name" type="String" length="15" />
				</native_schema>
			</access_specification>
		</access_specifications>  
	</st:connections>
```

   See more details about [connection document](http://ibmstreams.github.io/streamsx.messaging/com.ibm.streamsx.messaging/doc/spldoc/html/tk$com.ibm.streamsx.messaging/tk$com.ibm.streamsx.messaging$2.html)

* Next, create a SPL application and add JMS operator to it. Make sure the “use” directive is present in the SPL source file. If  Streams Studio is used, these directive is automatically added when dragging and dropping a JMS operator to SPL application.

```
use com.ibm.streamsx.messaging.jms::*;
```

&nbsp;&nbsp;&nbsp;&nbsp;or
```
use com.ibm.streamsx.messaging.jms::JMSSink;
use com.ibm.streamsx.messaging.jms::JMSSource;
```
* At minimum, both JMSSink and JMSSource operators requires two parameters to be specified namely “access” and “connection”, they are respectively referring to the name of access_specification and connection_specification elements in the connection document. <br><br>Please note that the attribute name, type and their order defined in streams schema for JMS operator must match the attribute name, type and order defined in native_schema section of connection document. See all [supported native attribute type and mapping to SPL type](http://ibmstreams.github.io/streamsx.messaging/com.ibm.streamsx.messaging/doc/spldoc/html/tk$com.ibm.streamsx.messaging/tk$com.ibm.streamsx.messaging$12.html)

```
    stream<int32 id, rstring name> myInputStream = JMSSource()
    {
	    param
	    	connection : "wmq" ;
	    	access : "access_wmq" ;
    }
```

* Another important optional parameter is the connectionDocument, the value of this parameter tells JMS operators where to locate the connection document. Below are supported scenarios for placing connection document in a SPL application for JMS operators.

    * *Default case*: by default, if connectionDocument parameter is not present for the JMS operator, then it is assumed that a file named "connections.xml" under etc directory of the SPL application will be used.
    * *Absolute path*: the connection document can be placed outside of a SPL application, in this case specify the full path to the connection document as value of connectionDocument parameter, for example, `connectionDocument: "/path/to/connection.xml";`.
    * *Relative path*: relative path is also supported only if the connection document resides inside of the SPL application. For example a connection file named "myConnections.xml" is placed under etc directory of a SPL application, then specify `connectionDocument: "./etc/myConnections.xml";`.

8. Build your SPL application. You can use the `sc` command or let  Studio build it.
9. Run the application. You can submit the application as a job by using the `streamtool submitjob` command or by using Streams Studio.

## Additional Resources
* [IBM MQ Knowledge Center](http://www-01.ibm.com/support/knowledgecenter/SSFKSJ_8.0.0/com.ibm.mq.helphome.v80.doc/WelcomePagev8r0.htm)
* [ActiveMQ website](http://activemq.apache.org/)
* [ Streams Messaging Toolkit SPLDoc](http://ibmstreams.github.io/streamsx.messaging/com.ibm.streamsx.messaging/doc/spldoc/html/index.html)
