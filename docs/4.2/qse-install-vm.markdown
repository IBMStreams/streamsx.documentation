---
layout: docs
title:  Installing Streams Quick Start Edition VM Image
description:  Installation Guide for IBM Streams Quick Start Edition VM
weight:  20
published: true
tag: 42qse
prev:
  file: qse-intro
  title:  Download the Quick Start Edition (QSE)
next:
  file: qse-getting-started
  title: Getting Started with IBM Streams v4.2 Quick Start Edition
---

The Streams Quick Start Editor can help you get started with Streams quickly, without having to install a Streams cluster environment.

{% include download.html%}
<br>
This guide takes you through the process of installing and starting the QSE VM image.

## System Requirements

| Components  | Minimum Requirements | Comments |
| ----------- | -------------------- | -------------|
| Operating System  | 64-bit operating system that supports VMware  | VMware is supported on the following operating systems: <br>- Apple Mac OS X <br>- Linux <br>- Microsoft Windows
| Memory	  |8 GB	                 |The amount of memory that is required by IBM Streams is dependent on the applications that are developed and deployed.  This minimum requirement is based on the memory requirements of the Commodity Purchasing sample application and other samples that are provided with the product.     
| Disk space  | 20 GB |  |
| Virtualization software | Virtualization product that runs on a 64-bit operating system	| To run the Quick Start Edition VMware image, install one of the following products on your system:<br>- For Apple Mac OS X, VMware Fusion 4, or later<br>- For Microsoft Windows or Linux, one of the following products:  VMware Player 5.0 +; VMware Workstation 8.0 +; VMware Server <br>**Tip:** You can use other virtualization software that supports VMDK formats, such as Oracle VirtualBox.

## Before you begin

Your Streams ID for the Quick Start Edition is **streamsadmin**, and your password is **passw0rd**. The root ID password is also **passw0rd**.

The Quick Start Edition is available only in English.

**Performance notes:**

* By default, the Quick Start Edition virtual machine is configured to have two processor cores and 4 GB of memory. Depending on your system resources and the applications that you develop and deploy, you might be able to improve performance by allocating more processor cores and memory to the virtual machine. You can adjust the processor and memory configuration by updating your virtual machine settings. For example, to update these settings for the VMware Player, click **Player > Manage > Virtual Machine Settings**.

* If you import the VMware image into a non-VMware virtualization product and have performance problems with the image, enable any available options that can reduce guest disk input/output latency. For example, in the Oracle VM VirtualBox Manager, select the **Use Host I/O Cache** option in the Storage Controller settings for the virtual machine.

## Procedure

### VMware Player/Workstation

1.  Download the vmware-streamsVxxx.zip file (where Vxxx is the version number of the Quick Start Edition).

1.  Extract the contents of the vmware-streamsVxxx.zip file.

    This .zip file contains the following files:

    ~~~~~~
    vmware-streamsVxxx-qse-v1.vmx, which is in the vmware-streamsVxxx-qse-v1.vmwarevm directory
    ~~~~~~

    Several Virtual Disk-snumber.vmdk files, which are in the vmware-streamsVxxx-qse-v1.vmwarevm directory

1.  Start the Quick Start Edition VMware image by double-clicking the vmware-streamsVxxx-qse-v1.vmx file.

1.  The first time that you start the image, respond to the following prompts:

    1.  Select **I copied it** to indicate that the virtual machine was copied. CentOS splash screen is displayed, and then followed by several screens of status messages.

    1.  To continue, accept all of the following license agreements:

        * CentOS
        * VMware tools
        * IBM® Streams

    To navigate in the license agreement screens, use the **Tab** and **Arrow** keys. Press the **Enter** key to continue.

    After you accept the license agreements, status messages are displayed and the Quick Start Edition VMware image desktop opens.

## Oracle VirtualBox

1. Download and extract the vmware-streamsVxxx.zip file (where Vxxx is the version number of the Quick Start Edition).

1. In Oracle VM VirtualBox Manager, click **New** and follow the instructions in the wizard:
    1. Specify a name of your virtual machine and select the **Linux Red Hat (64 bit)** operating system.
    1. Set the amount of memory to use for your virtual machine. The optimal setting depends on your hardware and usage. The more you allocate, the faster your virtual machine will run. You can adjust the setting later, if necessary.
    1. Select to use an existing virtual hard disk file, then browse for the vmware-streamsV#.#-qse-v1.vmdk file that you extracted earlier and click **Open**.
    1. Click **Create**. Now your new virtual machine is listed in the Oracle VM VirtualBox Manager.

1.  From the list, select your new virtual machine and click **Settings**:
    1. Select **System > Processor** and specify 2 virtual CPUs.
    1. Select the **Storage** tab and make sure that the **Use Host I/O Cache** option is selected.
    1. Click **OK** to save your settings.

1. To run your virtual machine, select it and click **Start**.


## What to do next

Explore the Streams QSE VMWare image following the [Quick Start Edition VM Getting Started Guide](/streamsx.documentation/docs/4.2/qse-getting-started/)
