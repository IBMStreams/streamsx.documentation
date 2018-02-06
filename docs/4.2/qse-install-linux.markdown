---
layout: docs
title:  Installing the Streams Quick Start Edition for Linux
description:  Installation Guide for IBM Streams Quick Start Edition for Linux
weight:  40
published: true
tag: 42qse
prev:
  file: qse-intro
  title:  Download the Quick Start Edition (QSE)
next:
  file: qse-getting-started
  title: Getting Started with IBM Streams v4.2 Quick Start Edition

---

The Streams Quick Start Edition (QSE) can help you get started with Streams quickly, without having to install a Streams cluster environment.

{% include download.html%}
<br>
This guide takes you through the process of installing QSE Linux Edition.

## Hardware Requirements

<table>
<thead class="thead" align="left"><tr class="row" valign="bottom"><th class="entry" valign="bottom">Component</th>
<th class="entry" align="center">Minimum requirements</th>
<th class="entry" valign="bottom">Comments</th>
</tr>
</thead>
<tbody class="tbody"><tr class="row"><td class="entry" rowspan="2" valign="top">System</td>
<td class="entry" align="center" valign="top">x86_64 (64-bit) </td>
<td class="entry" valign="top"><span class="keyword">IBM Streams</span> supports Red Hat Enterprise Linux (RHEL)</td>
</tr>
<tr class="row"><td class="entry" align="center" valign="top">IBM® Power Systems™ (64-bit)</td>
<td class="entry" valign="top" >RHEL systems that are running little endian support on POWER8 processor.</td>
</tr>
<tr class="row"><td class="entry" valign="top">Display</td>
<td class="entry" align="center" valign="top" >1280 x 1024</td>
<td class="entry" valign="top" >Lower resolutions are supported but not preferred
for Streams Studio.</td>
</tr>
<tr class="row"><td class="entry" valign="top" >Memory</td>
<td class="entry" align="center" valign="top" >2 GB</td>
<td class="entry" valign="top" ><span class="ph">The amount
of memory that is required by <span class="keyword">IBM Streams</span> is dependent on the applications that are developed
and deployed.</span><p class="p" >This minimum
requirement is based on the memory requirements of the Commodity Purchasing
sample application and other samples that are provided with the product.</p>
</td>
</tr>
<tr class="row"><td class="entry" rowspan="2" valign="top">Disk space</td>
<td class="entry" align="left" valign="top">7.5 GB, if installing the <span class="keyword">main installation package</span></td>
<td class="entry" rowspan="2" valign="top">Includes disk space required for
installation and development resources. For more information about
installation packages, see <a class="xref" href="http://www-01.ibm.com/support/knowledgecenter/?lang=en#!/SSCRJU_4.2.0/com.ibm.streams.install.doc/doc/ibminfospherestreams-install-programs-packages.html">Main and domain host installation
packages for <span class="keyword">IBM Streams</span></a>.</td>
</tr>
<tr class="row"><td class="entry" align="left" valign="top">2 GB, if installing the <span class="keyword">domain host installation package</span></td>
</tr>
</tbody>
</table>

## Software Requirements

<table>
<thead class="thead" align="left"><tr class="row" valign="bottom"><th class="entry" align="center" valign="bottom">Operating system</th>
<th class="entry" align="center" valign="bottom">System hardware and architecture</th>
<th class="entry" align="center" valign="bottom">Supported operating system versions</th>
</tr>
</thead>
<tbody class="tbody"><tr class="row"><td class="entry" rowspan="5" align="center" valign="top">RHEL</td>
<td class="entry" rowspan="2" align="center" valign="top">x86_64 (64-bit)</td>
<td class="entry" align="center" valign="top">Version 6.6, or later</td>
</tr>
<tr class="row"><td class="entry" align="center" valign="top">Version 7.0, or later</td>
</tr>
<tr class="row"><td class="entry" rowspan="1" align="center" valign="top">IBM Power
Systems (64-bit)<p class="p"><span class="keyword">IBM Streams</span> supports the POWER8™ processors (little endian).</p>
</td>
<td class="entry" align="center" valign="top">Version 7.1, or later</td>
</tr>
</tbody>
</table>

## Installation Instructions

Refer to the Knowledge Center for install instructions:
[Install Instructions for Quick Start Edition for Linux](http://www-01.ibm.com/support/knowledgecenter/SSCRJU_4.2.0/com.ibm.streams.qse.doc/doc/ibminfospherestreams-qse-install.html?lang=en)

## Resources

For details on system requirements for Streams QSE for Linux, refer to the [Knowledge Center](http://www-01.ibm.com/support/knowledgecenter/?lang=en#!/SSCRJU_4.2.0/com.ibm.streams.qse.doc/doc/ibminfospherestreams-qse-before-you-begin.html).

## What to do next

Explore the Streams QSE following the [Quick Start Edition VM Getting Started Guide](/streamsx.documentation/docs/4.2/qse-getting-started/)
