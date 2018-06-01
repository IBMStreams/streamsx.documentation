---
layout: docs
title:  Installing IBM Streams Runner for Apache Beam from an IBM Streams on-premises installation
navtitle: Installing
description: Installing IBM® Streams Runner for Apache Beam from an installation of IBM Streams involves extracting the Streams Runner toolkit and configuring environment variables.
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

Installing IBM® Streams Runner for Apache Beam from an installation of IBM Streams involves extracting the Streams Runner toolkit and configuring environment variables.

## Before you start
The on-premises installation of Streams Runner supports Apache Beam 2.4
applications, so your application must use the [Apache Beam SDK for Java API version 2.4](https://beam.apache.org/documentation/sdks/javadoc/2.4.0/).

Before you run the installation program, ensure that the `STREAMS_INSTALL` environment variable is set. If it is not, you
can set it in the `bash` shell by using the `cd` command to change to the Streams
installation directory and entering the following command:
```bash
. bin/streamsprofile.sh
```

## Installing and configuring Streams Runner

1. Go to a directory where you have permission to create files.
1. Extract the toolkit by entering the following command, where `<runner-version>` is the version of Streams Runner:
```bash
tar -zxvf $STREAMS_INSTALL/etc/beam/com.ibm.streams.beam-<runner-version>.tar.gz
```
1. (Optional) Create the Streams Runner environment variables.

    Tip: Although the variables are not required, the documentation refers to them for convenience. If you do not set the environment variables, you must use the full paths when you run the sample applications.
    1. Go to the `examples` directory in the expanded toolkit and run the `streams-runner-env.sh` command to set up environment variables for the runner:
    ```bash
    cd com.ibm.streams.beam-<runner-version>/examples
    . bin/streams-runner-env.sh
    ```
1. Set up IBM Streams for use with Streams Runner.
    1. Set the `STREAMS_DOMAIN_ID` and `STREAMS_INSTANCE_ID` environment
    variables to the Streams domain and instance you will use with
    Streams Runner.
    1. Verify that the Streams domain and instance are running:
    ```bash
    streamtool getinstancestate
    ```
    If the `getinstancestate` output includes the error `CDISC5005E`, start the instance:
    ```bash
    streamtool startinstance
    ```
    If the `getinstancestate` includes the error `CDISA5056E`, start
    the domain and instance:
    ```bash
    streamtool startdomain && streamtool startinstance
    ```
    1. Configure your certificates and keystore.

    Important: Streams Runner uses
    the Streams REST API for Beam metrics and job status, and Java rejects the connection if the certificate is not trusted or does not
    match the host name.

    Creating and configuring certificates is beyond
    the scope of this installation guide. For more information, see [Setting up client certificate authentication for IBM Streams users](https://www.ibm.com/support/knowledgecenter/SSCRJU_4.2.1/com.ibm.streams.cfg.doc/doc/setting-up-certificate-authentication.html).


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
