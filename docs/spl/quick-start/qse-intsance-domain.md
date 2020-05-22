
## Compiling and running Streams applications from commnad line

If you have a local installation of Streams, you can use the command line to build and submit your application, if you prefer. This is useful if you want to automate compilation for builds and continuous integration.

### Compiling with a local installation

**Before you begin:** Set up the necessary environment variables by running the following command:

<pre>source &lt;Streams_Install&gt;/bin/streamsprofile.sh</pre>

To build an application, use the `sc` command from the folder containing the project:

<pre>/opt/ibm/InfoSphere_Streams/4.3.1.1/bin/sc -M namespace::MainCompositeName --output-directory=output_dir --data-directory=data -a</pre>

*   The -M option specifies the name of the main composite to build
*   The --output-directory option specifies where to write the build output. Defaults to `output`.
*   The --data-directory option specifies the data directory of the application. A data directory is an optional directory where data may be read or written by your application.
*   The -a option specifies that the application should be compiled in optimized mode.

The application is built into a Streams Application Bundle file in the `output` directory. The bundle has a `.sab` extension.
The application bundle contains all file resources, libraries and dependencies required for running the application in distributed mode. 
For example, to compile the `TradesAppCloud` application:

`/opt/ibm/InfoSphere_Streams/4.3.1.1/bin/sc -M application::TradesAppCloud --output-directory=output/application.TradesAppCloud --data-directory=data -a`

### Launching the application

**Launch in standalone mode**

You can run the application as a standalone, single-process application. This is good for quick testing.

Run: `<path to output dir>/bin/standalone`

**Launch in distributed mode on Streams 4.3**

The application will be deployed as a distributed, multi-process job.
 
To run the application in distributed mode, you need to submit the application bundle to a _Streams Instance_.

<pre>streamtool submitjob [-i instance_name] [-d domain_name] appBundleName.sab</pre>

To submit our sample application, we will change into the output directory of the application and submit the application bundle:

<pre>cd output/application.TradesAppCloud/
streamtool submitjob application.TradesAppCloud.sab</pre>

<a name="querying_for_job_status"></a>

## Querying for Job Status

You may query job status from your Streams Instance using streamtool commands. If using embedded ZooKeeper:

<pre>streamtool lsjob -d <streamsDomainName> -i <instanceName> --embeddedzk</pre>

If using external ZooKeeper ensemble:

<pre>streamtool lsjob -d <streamsDomainName> -i <instanceName> --zkconnect <zooKeeperHost>:<zooKeeperPort></pre>

You will see job status similar to this:

<pre>[streamsadmin@streamsqse Distributed]$ streamtool lsjobs -d StreamsDomain -i StreamsInstance --embeddedzk
Instance: StreamsInstance
 Id State Healthy User Date Name Group
 6 Running yes streamsadmin 2015-04-30T18:32:48-0400 application::TradesAppCloud_6 default

</pre>

**Launch in distributed mode on Streams 5.x**


<a name="sample_application_output"></a>


## Streams runtime overview

The following is a brief overview of the components of the Streams runtime in Streams 4.3.

### Streams Instance 

An instance is the Streams distributed runtime environment. It is composed of a set of interacting services running across one or multiple resources. The Streams Instance is responsible for running Streams applications. When an application is submitted onto a Streams instance, it distributes the application code onto each of the resources. It coordinates with the instance services to execute the processing elements.


### Streams Domain (Streams 4.3 only)

In Streams 4.x, the runtime required _Streams Domain_ and a _Streams Instance_ to run in distributed mode. In Streams 5.x the domain no longer exists.

A domain is a logical grouping of resources (or containers) in a network for common management and administration. It can contain one or more instances that share a security model, and a set of domain services.  Domains are not used in Streams v5.x.

### Streams 4.3 only: Setting up a Development Domain and Instance 
*This information is provided as a quick reference. If you are using the Quick Start Edition, a domain and instance have already been set up for you.*

To set up a development domain and instance, follow these steps. A development domain and instance runs on a single host. You can dynamically add additional host to the domain later. First, if you have not already done so, set up the necessary environment variables by running the streamsprofile.sh.

<pre>source <Streams_Install>/bin/streamsprofile.sh</pre>

Next, start streamstool by typing the following command:

<pre>streamtool</pre>

When prompted to provide a ZooKeeper ensemble, enter the ZooKeeper ensemble string if you have a ZooKeeper server set up. Otherwise, press enter to use the embedded ZooKeeper. _streamtool_ is an interactive tool. To get content assist and auto-complete, press <Tab>.

### Domain

To make a new domain, enter this command in the _streamtool_ interactive command session:

<pre>mkdomain -d <domainName></pre>

Generate public and private key for Streams, so you do not have to keep logging in:

<pre>genkey</pre>

Start the domain:

<pre>startdomain</pre>

**Tip**: If the domain fails to start because a port is in use, you may change the port number by using setdomainproperty. For example, if JMX and SWS ports are in use:

<pre>setdomainproperty jmx.port=<jmxPort> sws.port=<sws.Port></pre>

### Instance

To make a new instance, enter this command:

<pre>mkinstance -i <instance-id></pre>

Start the instance:

<pre>startinstance</pre>

For information about domain and instance set up, refer to the following documentation:

*   [Enterprise Install and Setup Videos](https://developer.ibm.com/streamsdev/docs/streams-4-0-enterprise-install-and-setup-videos/)
*   [Multi-host environment: Installing to a shared file system](https://developer.ibm.com/streamsdev/docs/multi-host-environment-installing-shared-file-system/)
*   [Multi-host environment: Installing to each host and setting up a domain](https://developer.ibm.com/streamsdev/docs/multi-host-environment-installing-host-setting-domain/)

<a name="running_streams_applications_in_distributed_mode"></a>
