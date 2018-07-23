---
layout: docs
title:  Installing the Streams Quick Start Edition for Linux
description:  Installation Guide for IBM Streams Quick Start Edition for Linux
weight:  40
published: true
tag: 43qse
prev:
  file: qse-intro
  title:  Try Quick Start Edition
next:
  file: qse-getting-started
  title: Getting started

---

The Streams Quick Start Edition can help you get started with Streams quickly, without having to install a Streams cluster environment.

{% include download.html%}
<br>
This guide takes you through the process of installing Streams Quick Start Edition  Linux Edition.

## Hardware requirements

<table>
<thead class="thead" align="left"><tr class="row" valign="bottom"><th class="entry" valign="bottom">Component</th>
<th class="entry" align="left">Minimum requirements</th>
<th class="entry" valign="bottom">Comments</th>
</tr>
</thead>
<tbody class="tbody"><tr class="row"><td class="entry" rowspan="2" valign="top">System</td>
<td class="entry" align="left" valign="top">x86_64 (64-bit) </td>
<td class="entry" valign="top"><span class="keyword">IBM Streams</span> supports Red Hat Enterprise Linux (RHEL)</td>
</tr>
<tr class="row"><td class="entry" align="left" valign="top">IBM® Power Systems™ (64-bit)</td>
<td class="entry" valign="top" >RHEL systems that are running little endian support on POWER8 processor.</td>
</tr>
<tr class="row"><td class="entry" valign="top">Display</td>
<td class="entry" align="left" valign="top" >1280 x 1024</td>
<td class="entry" valign="top" >Lower resolutions are supported but not preferred
for Streams Studio.</td>
</tr>
<tr class="row"><td class="entry" valign="top" >Memory</td>
<td class="entry" align="left" valign="top" >2 GB</td>
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
installation packages, see <a class="xref" href="http://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.install.doc/doc/ibminfospherestreams-install-programs-packages.html">Main and domain host installation
packages for <span class="keyword">IBM Streams</span></a>.</td>
</tr>
<tr class="row"><td class="entry" align="left" valign="top">2 GB, if installing the <span class="keyword">domain host installation package</span></td>
</tr>
</tbody>
</table>

## Software requirements

<table>
<thead class="thead" align="left"><tr class="row" valign="bottom"><th class="entry" align="left" valign="bottom">Operating system</th>
<th class="entry" align="left" valign="bottom">System hardware and architecture</th>
<th class="entry" align="left" valign="bottom">Supported operating system versions</th>
</tr>
</thead>
<tbody class="tbody"><tr class="row"><td class="entry" rowspan="5" align="left" valign="top">RHEL</td>
<td class="entry" rowspan="2" align="left" valign="top">x86_64 (64-bit)</td>
<td class="entry" align="left" valign="top">Version 6.6, or later</td>
</tr>
<tr class="row"><td class="entry" align="left" valign="top">Version 7.0, or later</td>
</tr>
<tr class="row"><td class="entry" rowspan="1" align="left" valign="top">IBM Power
Systems (64-bit)<p class="p"><span class="keyword">IBM Streams</span> supports the POWER8™ processors (little endian).</p>
</td>
<td class="entry" align="left" valign="top">Version 7.1, or later</td>
</tr>
</tbody>
</table>

## Installing Quick Start Edition for Linux

For detailed instructions for installing Streams Quick Start Edition for Linux, see
[Installing the Quick Start Edition for Linux](http://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.qse.doc/doc/ibminfospherestreams-qse-linux-container.html)

## Resources

For details about system requirements for Streams Quick Start Edition for Linux, see [System requirements for the Quick Start Edition for Linux](http://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.qse.doc/doc/ibminfospherestreams-qse-before-you-begin.html).

## What to do next

Explore Streams Quick Start Edition with [Getting started with IBM Streams v4.3](/streamsx.documentation/docs/4.3/qse-getting-started/)
