---
layout: docs
title: Cybersecurity Toolkit - Getting Started
description:  Getting Started Guide for IBM Streams Cybersecurity Toolkit
weight: 10
---

## Introduction
The Cybersecurity Toolkit provides operators that are capable of analyzing network traffic and detecting suspicious behaviour.

In order to get started with using the Cybersecurity Toolkit, it is ***highly recommended*** that the sample applications be used as a baseline for building cybersecurity applications. In many cases, the data must be pre-processed (filtered and enriched) prior to be being analyzed, otherwise the analytics will not work correctly. The sample applications contain the necessary pre-processing operators that enable the analytics to work properly. The three introductory sample projects are:

 - **DomainProfiling** - Detects suspicious behaviour based on profiles built using domains found in DNS response traffic.
 - **HostProfiling** - Detects suspicious behaviour based on profiles built using hosts found in DNS response traffic.
 - **PredictiveBlacklisting** - Predicts where a domain should be added to a blacklist.


Since the cybersecurity toolkit is focused on analyzing network traffic, you must download and install the com.ibm.streamsx.network toolkit, found in the [streamsx.network](https://github.com/IBMStreams/streamsx.network) GitHub repository. The build.xml file contained in each of the sample applications will automatically download the latest release of the com.ibm.streamsx.network toolkit and place it in the same directory as the samples.


## Download Quick Start Edition VM
See the [Installing Streams Quick Start Edition VM Image]({{ site.url }}/docs/4.1/qse-install-vm/) for more information.

<!--
## Download Docker
See the [Installing Streams Docker Image]({{ site.url }}/docs/4.1/qse-install-docker/) for more information
-->

## Install Dependencies - Quick Start Edition VM
If you are using the Quick Start VM, you will need to download and build the following dependencies in order to use the cybersecurity toolkit:

 - GNU Bison
 - Flex
 - libpcap


#### GNU Bison
 1. Navigate to [http://ftp.gnu.org/gnu/bison/](http://ftp.gnu.org/gnu/bison/) and download the latest version of GNU Bison to the Quick Start VM. As of the time of this writing, the latest version of GNU Bison was 3.0.4.
 2. Execute the following commands to extract the tarball and run the install:

	<pre class="terminal">
	<span class="command">tar -xvf bison-3.0.4.tar.gz</span>
	<span class="command">cd bison-3.0.4</span>
	<span class="command">./configure</span>
	<span class="command">make</span>
	<span class="command">sudo make install</span></pre>


#### Flex
 1. Navigate to [http://flex.sourceforge.net](http://flex.sourceforge.net) and download the latest version of Flex to the Quick Start VM. When this guide was written, the latest version of flex was 2.5.39.
 2. Execute the following commands to extract the tarball and run the install:

	<pre class="terminal">
	<span class="command">tar -xvf flex-2.5.39.tar.gz</span>
	<span class="command">cd flex-2.5.39</span>
	<span class="command">./configure</span>
	<span class="command">make</span>
	<span class="command">sudo make install</span></pre>


#### libpcap
 1. Navigate to [http://www.tcpdump.org](http://www.tcpdump.org) and download the latest version of libpcap to the Quick Start VM. When this guide was written, the latest version of libpcap was 1.7.4.
 2. Execute the following commands to extract the tarball and run the install:

	<pre class="terminal">
	<span class="command">tar -xvf libpcap-1.7.4.tar.gz</span>
	<span class="command">cd libpcap-1.7.4</span>
	<span class="command">./configure</span>
	<span class="command">make</span>
	<span class="command">sudo make install</span></pre>


<!--
## Install Dependencies - Docker Image
The Docker Image requires you to install the following applications:

 - git
 - ant
 - wget

These applications can be installed at the same time using the following commands:

<pre class="terminal">
<span class="command">sudo yum install -y git ant wget</span>
<span class="output">...</span>
<span class="output">Installed:</span>
<span class="output">   ant.x86_64 0:1.7.1-13.el6   git.x86_64 0:1.7.1-3.el6_4.1   wget.x86_64 0:1.12-5.el6_6.1</span>                      
<span class="output"> </span>
<span class="output">Dependency Installed:</span>
<span class="output">   perl-Git.noarch 0:1.7.1-3.el6_4.1</span>
<span class="output"> </span>
<span class="output">Complete!</span></pre>


Furthermore, you will need to download and build the following dependencies. See the section entitled **Install Dependencies - Quick Start Edition VM** for details on how to download and build these dependencies.

 - GNU Bison
 - Flex
 - libpcap
-->

## Install SPSS (Optional)
The SPSS Modeler Solution Publisher is only required if you want to run the PredictiveBlacklistingSample application. In order to download and install this version of SPSS, you need to a license for the product.

 1. Download and install SPSS Modeler Solution Publisher into the Quick Start VM
 2. Modify the `/home/streamsadmin/.bashrc` file and set the `CLEMRUNTIME` environment variable to the SPSS install path:

	<pre class="terminal">
	<span class="command">echo "export CLEMRUNTIME=/usr/IBM/SPSS/ModelerSolutionPublisher/17.0/" >> /home/streamsadmin/.bashrc</span>
	<span class="command">source ~/.bashrc</span></pre>

 3. Download and extract the **com.ibm.spss.streams.analytics** toolkit using the following commands:

	<pre class="terminal">
	<span class="command">cd Downloads</span>
	<span class="command">wget https://github.com/IBMPredictiveAnalytics/streamsx.spss.v4/raw/master/com.ibm.spss.streams.analytics.tar.gz</span>
	<span class="command">tar -xvf com.ibm.spss.streams.analytics.tar.gz</span></pre>

 4. At this point, the PredictiveBlacklisting sample application can be compiled using the steps below.

**NOTE:** When building the PredictionBlacklistingSample using ant, you must specify the `spss.toolkit.path` property on the command-line and set the value to the toolkit path. For example: `ant -Dspss.toolkit.path=/home/streamsadmin/Downloads/com.ibm.spss.streams.analytics`.


## Sample Applications
The cybersecurity toolkit sample applications should be used as a baseline for building cybersecurity applications on Streams. The samples contain the necessary filter and enrichment operators that allow the analytics to work properly.

By default, the sample applications will use the PacketFileSource operator (found in the com.ibm.streamsx.network toolkit) to read sample PCAP files packaged with the toolkit. However, this operator can easily be replaced with the PacketLiveSource operator, which allows for ingesting and parsing live data.


### Download/Build/Run
The following steps can be taken to download, compile and run the cybersecurity samples:

 1. From the command-line, clone the samples github repository and navigate to the 'cybersecurity' directory. Here you will find directories containing the sample applications:

	<pre class="terminal">
	<span class="command">git clone https://github.com/IBMStreams/samples.git</span>
	<span class="command">cd samples/cybersecurity</span>
	<span class="command">ls -l</span>
	<span class="output">DomainProfilingSamples  HostProfilingSamples  PredictiveBlacklistingSamples</span></pre>

 2. Navigate to the DomainProfilingSamples directory. The directory contains a build.xml file that will download any necessary dependencies (including the networking toolkit) and compile one of the applications. Run the `ant` command to kick off the build.

	<pre class="terminal">
	<span class="command">ant</span></pre>

 3. Use the Streams Console to submit the application to the instance. To get the URL for the Streams Console, run the following command:

	<pre class="terminal">
	<span class="command">streamtool geturl</span>
	<span class="output">https://streamsqse.localdomain:8443/streams/domain/console</span></pre>

 4. Once the Streams Console is open, you should be presented with a screen that looks like the following:

	<a href="#/" class="pop">
		<img src="../../../../images/cybersecurity/console_start.png" style="width:45%; height: 25%; margin-left:auto; margin-right:auto; display: block;" />
	</a>

 5. At the top of the Streams Console, switch to the Application Dashboard, which allows you submit, cancel and monitor applications.

	<a href="#/" class="pop">
		<img src="../../../../images/cybersecurity/streams-console1.png" style="width:45%; height: 25%; margin-left:auto; margin-right:auto; display: block;" />
	</a>

 6. With the Application Dashboard open, click the **Submit Job** icon <img src="../../../../images/cybersecurity/console_submit_icon.png" />. Select the *.sab file found in the 'output/' directory in the sample application. For example, for the DomainProfilingSample application, you would select this file: `/path/to/DomainProfilingSample/output/DomainProfilingBasic_Output/com.ibm.streams.cybersecurity.sample.DomainProfilingBasic.sab`

	<a href="#/" class="pop">
	<img src="../../../../images/cybersecurity/console_submit_job.png" style="width:25%; height: 25%; margin-left:auto; margin-right:auto; display: block;" />
	</a>

 7. Once the application has been submitted, the Streams Console should display the running application:

	<a href="#/" class="pop">
		<img src="../../../../images/cybersecurity/console_running.png" style="width:45%; height: 25%; margin-left:auto; margin-right:auto; display: block;" />
	</a>


### Analyze Output
The sample applications will output the results of the analytics to the data directory. There will be two files generated in this directory:

 - **dpresults_suspicious.csv** - lists the domains that were classified as suspicious
 - **dpresults_benign.csv** - lists the domains that were classified as benign

For the DomainProfilingBasic application, only the classified domains are written to the file. However, generally you will want to output additional information, such as the IP addresses of the hosts that accessed these domains. The 'DomainProfilingExtended' sample application demonstrates how to collect a set of the unique IPs that accessed the domain.


### Importing into Streams Studio
The cybersecurity sample applications can be imported into Streams Studio as SPL Projects. When importanting the cybersecurity samples, you must add the **com.ibm.streamsx.network** toolkit location to Streams Explorer. If you are planning on using the PredictiveBlacklisting samples, you must add the **com.ibm.spss.streams.analytics** toolkit to Streams Explorer as well.

<!--
### Additional Information

 - Cybersecurity Documentation - Knowledge Center - COMING SOON!
 - Cybersecurity Article - COMING SOON!
-->


<script type="text/javascript">
$(function() {
		$('.pop').on('click', function() {
			$('.imagepreview').attr('src', $(this).find('img').attr('src'));
			$('#imagemodal').modal('show');   
		});		
});
</script>

<!-- Modal -->
<div class="modal fade" id="imagemodal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog" data-dismiss="modal" style="width: auto" >
    <div class="modal-content"  >              
      <div class="modal-body">
      	<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
        <img src="" class="imagepreview"  style="margin-left:auto; margin-right:auto; display: block; max-width: 100%">
      </div>
      <div class="modal-footer">
          <div class="col-xs-12">
          </div>
      </div>
    </div>
  </div>
</div>
