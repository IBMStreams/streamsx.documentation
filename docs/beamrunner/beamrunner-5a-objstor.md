---
layout: docs
title:  Using Bluemix Object Storage Swift with IBM Streams Runner for Apache Beam
navtitle: Object Storage
description:  
weight:  10
published: true
tag: beam
prev:
  file: beamrunner-5-ref
  title: Reference
next:
  file: beamrunner-6-issues
  title: Limitations and known issues
---

IBM® Streams Runner for Apache Beam can use the Bluemix Object Storage Swift_ object store for I/O. This is most useful when running Apace Beam 2.0 applications on the Streaming Analytics service on IBM Bluemix, where direct access to output files from Beam applications is difficult.

This document describes the swift:// scheme and then shows how to set up Bluemix Object Storage Swift and use the scheme with one of the sample applications from Streams Runner. It assumes you have already set up and run other samples on the Bluemix Streaming Analytics service.

## The swift:// scheme

The _Bluemix Object Storage Swift_ service stores objects in containers; see the [documentation](https://console.stage1.bluemix.net/docs/services/ObjectStorage/index.html) for more details. Beam I/O uses URIs to name files, and Streams Runner interprets the URI in the format swift://_<container>_/_<object>_ to read and write these objects.

The object storage system does not allow the forward slash (/) character in the container name, but does allow it in the object name. While slash is not special to object storage, the Streams Runner will treat it as a directory separator in a logical path.

For example if a container named MyContainer contains objects named top.txt and dir/nested.txt the object storage system will show these together in the list of objects in MyContainer. In Beam, the URIs swift://MyContainer/foo.txt and swift://MyContainer/dir/nested.txt refer to these two objects but Beam will also consider swift://MyContainer/dir/ to be a logical directory that contains a resource named nested.txt. "Glob" patterns for resources (for example swift://MyContainer/dir/\*) are not currently supported.

See the [Beam I/O documentation](https://beam.apache.org/documentation/sdks/javadoc/2.0.0/org/apache/beam/sdk/io/package-summary.html) for more information on managing filesystems and resources with Beam.

## Creating the Bluemix Object Storage Swift service

If you already have the _Bluemix Object Storage Swift_ service set up you can skip to the next section. Note that it must be the _Bluemix Object Storage Swift_ service and **not** the _Cloud Object Storage – S3_ service.

1. On the [Bluemix dashboard](https://console.bluemix.net/dashboard) main menu, choose **Storage**.
2. Click **Create Storage Service**.
3. Click **Cloud Object Storage**.
`missing image`
4. Select **Bluemix Object Storage Swift** if it is not already selected.  
  Note: the _Cloud Object Storage – S3_ service is not supported by the Streams Runner and will not work with this tutorial.
`missing image`
5. Click **Create**.
6. For this sample change the Service name to Object Storage Demo. You may also change the region, organization, and space as appropriate but the defaults will work.
7. Select the Free plan for the sample.
8. Click **Create**. Bluemix returns to the Dashboard while the service is being provisioned.

## Setting up credentials for the service

1. Once the service has been provisioned, select the service from the Dashboard to open the _Manage_ page for the service. From here you manage the files that you create. The Streams Runner will create containers and files as required.
2. To use the storage from Beam applications, service credential information is required. Click **Service credentials**.
3. Click **New credential** and **Add**.
4. On the newly created credential, click **View Credentials**.
5. On the computer with the Streams Runner installed, create the following environment variables from the fields shown in the credentials:

| Environment variable | Credentials field | Example |
| --- | --- | --- |
| OS\_USER\_ID | userId | export OS\_USER\_ID="2b670d77432e4cf2bd128ef9ff61fa56" |
| OS\_PASSWORD | password | export OS\_PASSWORD=" f1H/~BIO.=s0wuT9" |
| OS\_PROJECT\_ID | projectId | export OS\_PROJECT\_ID="80301e24254f4ffb81d53f0cddccad78" |
| OS\_REGION\_NAME | region | export OS\_REGION="dallas" |

These environment variables are also used by the command-line Swift client.
See [Configuring the CLI to use Swift and Cloud Foundry commands](https://console.stage1.bluemix.net/docs/services/ObjectStorage/os_configuring.html) for more details.
For MacOS, the swift command of OpenStack might collide with the existing Xcode swift command. To avoid the conflicts, create a python virtual environment, and install swift client in the virtual environment.

$ virtualenv my\_project
$ cd my\_project
$ source bin/activate
$ pip install python-swiftclient
$ pip install python-keystoneclient

## Running the sample application

1. Change directory to the samples directory in the Streams Runner, and set up environment variables for the runner:

    ```
$ cd <installdir>/samples
$ . bin/streams-runner-env.sh
```

2. Set the environment variables VCAP\_SERVICES to point to the VCAP file containing your Bluemix Streaming Analytics Service credentials and STREAMING\_ANALYTICS\_SERVICE\_NAME to the service name within that file, for example:

    ```
$ export VCAP\_SERVICES=$HOME/sample.vcap
$ export STREAMING\_ANALYTICS\_SERVICE\_NAME="sample-service"
```

3. Run the following command to run the FileStreamSample Beam application:

    ```
java -cp \
$STREAMS\_BEAM\_TOOLKIT/lib/com.ibm.streams.beam.translation.jar:\
lib/com.ibm.streams.beam.samples.jar \
com.ibm.streams.beam.sample.FileStreamSample \
--runner=StreamsRunner \
--contextType=STREAMING\_ANALYTICS\_SERVICE \
--jarsToStage=lib/com.ibm.streams.beam.samples.jar:\
$STREAMS\_BEAM\_TOOLKIT/lib/com.ibm.streams.beam.sdk.jar \
--filesToStage=&#39;{"README.md":"sample/README.md"}&#39; \
--input=streams://sample/README.md \
--output=swift://out/README.md
```

    The command should submit the application to the Streaming Analytics Service, copy the file to object storage, and then exit. If it does not submit successfully, check your VCAP\_SERVICES and STREAMING\_ANALYTICS\_SERVICE\_NAME. If it submits but does not complete, download and inspect the job logs from the Streams Console on Bluemix.

    The command is similar to the one used in the README.md for this sample application, but there are a few important differences:

    - The --jarsToStage option includes more jars. The swift:// scheme support is in the $STREAMS\_BEAM\_TOOLKIT/lib/com.ibm.streams.beam.sdk.jar which is not staged by default and so must be included here
    - The --filesToStage  option is used to move the local md file to the runtime environment on Bluemix to be used as input for the sample. Alternatively, this file could have been uploaded to _Bluemix Object Storage Swift_ using the web UI or command-line Swift client and referenced with the swift:// scheme but staging it this way allows using it without that extra step.
    - The --input option uses the streams:// scheme to refer to the file staged above.
    - The --output option uses the swift:// scheme to direct the application to write the output file into an object named md in a container named ut.

  When the job completes successfully, the Streams Console will show the job as healthy (green) and the copied file will be available in the _Bluemix Object Storage Swift_ web management page:

`missing image`

Note that whether the job is successful or not it will stay running on the Streaming Analytics service to allow for inspection by the Streams Console. When you are done with the tutorial, make sure to use the Streams Console to cancel any jobs you started.
