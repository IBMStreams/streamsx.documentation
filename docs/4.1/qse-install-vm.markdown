---
layout: docs
title:  Installing and Starting the Quick Start Edition VM Image
---

# Installing and Starting the Quick Start Edition (QSE) VM Image

The Streams Quick Start Editor VMware can help you get started with Streams quickly, without having to install a Streams cluster environment. These images are available [here](http://www.ibm.com/analytics/us/en/technology/stream-computing/).

This guide takes you through the process of installing and starting the QSE VM image.

## Before you begin

Your Streams ID for the Quick Start Edition is **streamsadmin**, and your password is **passw0rd**. The root ID password is also **passw0rd**.

The Quick Start Edition is only available in English.

**Performance notes:**

* By default, the Quick Start Edition virtual machine is configured to have two processor cores and 4 GB of memory. Depending on your system resources and the applications that you develop and deploy, you might be able to improve performance by allocating more processor cores and memory to the virtual machine. You can adjust the processor and memory configuration by updating your virtual machine settings. For example, to update these settings for the VMware Player, click *Player > Manage > Virtual Machine Settings*.

* If you import the VMware image into a non-VMware virtualization product and have performance problems with the image, enable any available options that can reduce guest disk input/output latency. For example, in the VirtualBox program from Oracle, select the Use Host I/O Cache option in the Storage Controller settings for the virtual machine.

## Procedure

1.  Download the vmware-streamsVxxx.zip file (where Vxxx is the version number of the Quick Start Edition).

1.  Extract the contents of the vmware-streamsVxxx.zip file.

    This .zip file contains the following files:

    ~~~~~~
    vmware-streamsVxxx-qse-v1.vmx, which is in the vmware-streamsVxxx-qse-v1.vmwarevm directory
    ~~~~~~

    Several Virtual Disk-snumber.vmdk files, which are in the vmware-streamsVxxx-qse-v1.vmwarevm directory

1.  Start the Quick Start Edition VMware image by double-clicking the vmware-streamsVxxx-qse-v1.vmx file.

    The first time that you start the image, several messages and prompts are displayed. Otherwise, the Quick Start Edition VMware image desktop opens.

1.  The first time that you start the image, respond to the following prompts:

    1.  Select **I copied it** to indicate that the virtual machine was copied. Red Hat Enterprise Linux splash screen is displayed, and then followed by several screens of status messages.

    1.  To continue, accept all of the following license agreements:
    
        * Red Hat Enterprise Linux
        * VMware tools
        * IBM® Streams

    To navigate in the license agreement screens, use the **Tab** and **Arrow** keys. Press the **Enter** key to continue.

    After you accept the license agreements, status messages are displayed and the Quick Start Edition VMware image desktop opens.

## What to do next

Explore the Streams QSE VMWare image following the [Quick Start Edition VM Getting Started Guide](/streamsx.documentation/docs/4.1/qse-getting-started/)