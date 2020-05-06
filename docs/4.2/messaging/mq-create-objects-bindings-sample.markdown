---
layout: docs
title: WebSphere MQ - Sample steps for creating queues and bindings file
description:  Sample scripts for creating MQ objects and bindings.
weight: 80
publisehd: true
---

## Introduction
 Streams messaging toolkit provides operators for sending and receiving messages from WebSphere MQ. This article shows a simple sample for creating WebSphere MQ administered objects and generating bindings file.

## Skill Level
Readers of this article is expected to have basic understanding WebSphere MQ.

## Requirements
- You must have already installed WebSphere MQ. A evaluation version of [WebSphere MQ](https://www-01.ibm.com/marketing/iwm/iwm/web/pick.do?pkgid=&S_SRCID=ESD-WSMQ-EVAL&source=ESD-WSMQ-EVAL&S_TACT=109J84RW&S_PKG=CR9H9ML&lang=en_US&lang=en_US) is available.
- Create an OS user on the machine where WebSphere MQ server is running and make sure the user name is same as the user that will run SPL application.

## Steps

* Create WebSphere MQ administered objects (assuming WebSphere MQ is installed at /opt/mqm/)
  1. Log into the WebSphere MQ server as mqm user.
  2. Set up WebSphere MQ environment `source /opt/mqm/bin/setmqenv -s`.
  3. Creating a new queue manager named "QM1" `crtmqm QM1`.
  4. Start QM1 `strmqm QM1`.
  5. Run MQSC command on QM1 `runmqsc QM1`.
  6. Create a local queue Q1 `define qlocal(Q1)`.
  7. Create a listener `define listener(L1) trptype(tcp) port(1416)`.
  8. Start listener L1 `start listener(L1)`.
  9. Create a channel named "JMS.STREAMS.SVRCONN" `def channel (JMS.STREAMS.SVRCONN) chltype(SVRCONN)`.
  10. Add a channel authentication record for the new OS user, assuming the username is "streamsadmin" `SET CHLAUTH('JMS.STREAMS.SVRCONN') TYPE(USERMAP) CLNTUSER('streamsadmin') USERSRC(CHANNEL) DESCR('streamsadmin record') ACTION(ADD)`.
  11. From a command prompt, provide the following authorities for user "streamsadmin".

      `setmqaut -m QM1 -t qmgr -p "streamsadmin" -all`

	  `setmqaut -m QM1 -t qmgr -p "streamsadmin" +setall +setid +altusr +connect +inq`

	  `setmqaut -m QM1 -n "Q1" -t q -p "streamsadmin" -remove`

	  `setmqaut -m QM1 -n "Q1" -t q -p "streamsadmin" +passall +passid +setall +setid +browse +get +inq +put +set`

  12. perform a security refresh in MQSC command line `refresh security TYPE (AUTHSERV)`.


* Generate bindings file using JMSAdmin script
  1. Log into the WebSphere MQ server as mqm user.
  2. Open MQ_INSTALLATION_PATH/java/bin/JMSAdmin.config file with text editor.
  3. Edit the following lines. Choose a accessible directory for the PROVIDER_URL parameter, where the .bindings file will be generated.

     `INITIAL_CONTEXT_FACTORY=com.sun.jndi.fscontext.RefFSContextFactory`

     `PROVIDER_URL=file:///homes/user/bindings`

  4. Set the CLASSPATH for running JMSAdmin tool

     `export CLASSPATH=$CLASSPATH:/opt/mqm/java/lib:/opt/mqm/java/lib/com.ibm.mq.jar:/opt/mqm/java/lib/com.ibm.mq.jms.Nojndi.jar:/opt/mqm/java/lib/com.ibm.mq.soap.jar:/opt/mqm/java/lib/com.ibm.mqetclient.jar:/opt/mqm/java/lib/com.ibm.mqjms.jar`

  5. Run JMSAdmin tool `MQ_INSTALLATION_PATH/java/bin/JMSAdmin`
  6. Run following commands in JMSAdmin tool for defining queue connection factory and queue. Replace <host name> with the actual host name.

     `DEFINE QCF(confact) QMGR(QM1) tran(client) chan(JMS.STREAMS.SVRCONN) host(<host name>) port(1416)`

     `DEFINE Q(dest) QUEUE(Q1) QMGR(QM1)`

     `end`
  7. A file named .bindings has been generated under the directory specified for the PROVIDER_URL parameter.

## Additional Resources
[WebSphere MQ Knowledge Center](https://www-01.ibm.com/support/knowledgecenter/SSFKSJ_8.0.0/com.ibm.mq.helphome.v80.doc/WelcomePagev8r0.htm?lang=en)
