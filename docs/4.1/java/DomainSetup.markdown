# Streams domain and instance
To run your application in distributed mode, you need a Streams domain and a Streams instance. A domain is a logical grouping of resources (or containers) in a network for common management and administration. It can contain one or more instances that share a security model and a set of domain services. An instance is the Streams distributed runtime environment. It is composed of a set of interacting services running across one or multiple resources. 

The Streams instance is responsible for running Streams applications. When an application is submitted onto a Streams instance, the instance distributes the application code onto each of the resources. It coordinates with the instance services to execute the processing elements.

# Setting up a development domain and instance
To set up a development domain and instance, follow these steps. A development domain and instance runs on a single host. You can dynamically add further hosts to the domain later. 

1. First, if you have not already done so, set up the necessary environment variables by running the **streamsprofile.sh**.
  ``` bash
    $  source  <Streams_Install>/bin/streamsprofile.sh
  ```	
  
2. Start **streamstool** by typing the following command:
  ``` bash
    $  streamtool
  ```	
  **streamtool** is an interactive tool. To get content assist and auto-complete, press the Tab key.

3. When prompted to provide a ZooKeeper ensemble, enter the ZooKeeper ensemble string if you have a ZooKeeper server set up. Otherwise, press enter to use the embedded ZooKeeper. 

4. To make a new domain, enter this command:
  ``` bash
    $  mkdomain -d <domainName>
  ```	
 
5. Generate public and private keys for Streams, so you do not have to keep logging in:
  ``` bash
    $  genkey
  ```	

6. Start the domain:
  ``` bash
    $  startdomain
  ```	
  **Tip:** If the domain fails to start because a port is in use, you can change the port number by the using setdomainproperty command. For example, if JMX and SWS ports are in use, you can change the port numbers like this:
  ``` bash
    $  setdomainproperty jmx.port=<jmxPort> sws.port=<sws.Port>
  ```	

7. To make a new instance, enter this command:
  ``` bash
    $  mkinstance -i <instance-id>
  ```	

8. Start the instance:
  ``` bash
    $  startinstance
  ```	

9. Exit the interactive **streamtool** interface.

# Running Streams applications in distributed mode
Now that you have a domain and instance started, you can run your compiled application in distributed mode. To submit a job, find the application bundle file (*.sab) and run the following command:
``` bash
  $  streamtool submitjob appBundleName.sab
```	

To submit our sample application, let's change into the output directory of the application and submit the application bundle:
``` bash 
  $  cd output/application.TradesAppMain/
  $  streamtool submitjob application.TradesAppMain.sab
```	
**_Question IG: This sample application was never mentioned before. Can't we refer to one of the samples provided with the topology toolkit? Maybe the Kafka one that's described in one of the other articles?_**

# Querying for job status
You can query the job status from your Streams instance by using streamtool commands. If you work with the embedded ZooKeeper, enter the following command:
``` bash
  $  streamtool lsjob -d <streamsDomainName> -i <instanceName> --embeddedzk
```	

If you work with an external ZooKeeper ensemble, enter the following command:
``` bash
  $  streamtool lsjob -d <streamsDomainName> -i <instanceName> --zkconnect <zooKeeperHost>:<zooKeeperPort>
```	

You will see a job status similar to this:
```
    [streamsadmin@streamsqse Distributed]$ streamtool lsjobs -d StreamsDomain -i StreamsInstance --embeddedzk
    Instance: StreamsInstance
    Id State Healthy User Date Name Group
    6 Running yes streamsadmin 2015-04-30T18:32:48-0400 application::TradesAppMain_6 default
```	
