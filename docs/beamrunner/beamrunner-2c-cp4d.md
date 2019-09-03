---
layout: docs
title:  Installing IBM Streams Runner for Apache Beam from an IBM Cloud Pak for Data installation
navtitle: Installing
description: Installing IBM® Streams Runner for Apache Beam from an installation of IBM Cloud Pak for Data involves downloading and extracting the Streams Runner toolkit, and configuring environment variables.
weight:  10
published: true
tag: beam
prev:
  file: beamrunner-2-install
  title: Installing
next:
  file: using
  title: Using
---

** FIXME ** This page is a work-in-progress, as the final packaging has not
yet been fixed. It is based on the assumption the beam package will be
downloadable from the console, but this could change.

Installing IBM® Streams Runner for Apache Beam from an installation of IBM Cloud Pak for Data involves downloading and extracting the Streams Runner toolkit, and configuring environment variables.

## Before you start
The Cloud Pak for Data installation of Streams Runner supports Apache Beam 2.14
applications, so your application must use the [Apache Beam SDK for Java API version 2.14](https://beam.apache.org/releases/javadoc/2.14.0/).

Before you can download Streams Runner, you must have a Streams instance
provisioned and running in Cloud Pak for Data.
** FIXME ** add link to basic Streams CP4D docs.

In Cloud Pak for Data, open the Streams Console:

1. Click the menu icon in the top left and select **My Instances**.
2. Click the **Provisiond Instances** tab.
3. For any Streams instance (type `streams`), click the `...` options at
   the right and select **View Details**.
4. On the details page, copy the `externalConsoleEndpoint` URL and open it
   a new browser window or tab.

In the Streams Console:
1. Log into the console with your Cloud Pak for Data credentials.
2. In the Streams Console, click **Help > Download > Download Streams
   Runner for Apache Beam**.
3. Select **Save File**, specify a location if necessary, and click **OK**.

Extract the toolkit by entering the following command

Extract the toolkit by entering the following command where you downloaded the file, where `<runner-version>` indicates the version of the archive file:
```bash
tar -zxvf com.ibm.streams.beam-<runner-version>.tar.gz
```

**Recommended:** Configure the IBM Streams Runner environment variables.

Tip: Although the variables are not required, the documentation refers to them for convenience. If you do not set the environment variables, you must use the full paths when you run the sample applications.
1. Go to the `examples/bin` directory in the expanded toolkit and run the `streams-runner-env.sh` command to set up  environment variables for the runner:
```bash
cd com.ibm.streams.beam-<runner-version>/examples/bin
. streams-runner-env.sh
```

## Validating the Streams Runner installation

Streams Runner relies on preserving the `com.ibm.streams.beam` directory structure. To verify an installation, ensure that the `translation` and `sdk` JAR files appear as follows when you enter the following command:
```bash
ls $STREAMS_BEAM_TOOLKIT/lib
> com.ibm.streams.beam.sdk.jar  com.ibm.streams.beam.translation.jar
```

### The Streams Runner directory tree structure
```
com.ibm.streams.beam-<runner-version>/
| - template.vcap
| - README.html
| - README.md
| - com.ibm.streams.beam/
| | - info.xml
| | - toolkit.xml
| | - com.ibm.streams.beam.transforms/
| | - doc/
| | - opt/
| | - impl/
| | | - lib/
| | | | - com.ibm.streams.beam.runtime.jar
| | - lib/
| | | - com.ibm.streams.beam.sdk.jar
| | | - com.ibm.streams.beam.translation.jar
| - examples/
| | - README.html
| | - README.md
| | - pom.xml
| | - src/
| | - target/
| | | - site/
| | - bin/
| | | - streams-runner-env.sh
```
