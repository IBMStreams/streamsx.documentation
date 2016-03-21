---
layout: docs
title:  Installing Streams Quick Start Edition for Linux
description:  Installation Guide for IBM Streams Quick Start Edition for Linux
weight:  40
---

# Installing the Streams Quick Start Edition for Linux

The Quick Start Edition (QSE) for Linux can help you get started with Streams quickly, without having to install a Streams cluster environment. 

{% include download.html%}
<br>
This guide takes you through the process of installing QSE for Linux.

## Hardware Requirements

<div class="tablenoborder"><table cellpadding="4" cellspacing="0" summary="This table lists the system, display, memory, and disk space requirements for InfoSphere Streams." class="table" width="100%" rules="all" frame="border" border="1"><thead class="thead" align="left"><tr class="row" valign="bottom"><th class="entry thleft thbot" valign="bottom" width="10.795454545454545%" id="d68e56">Component</th>
<th class="entry thcenter thbot" align="center" valign="bottom" width="30.113636363636363%" id="d68e58">Minimum requirements</th>
<th class="entry thleft thbot" valign="bottom" width="59.09090909090909%" id="d68e60">Comments</th>
</tr>
</thead>
<tbody class="tbody"><tr class="row"><td class="entry" rowspan="2" valign="top" width="10.795454545454545%" headers="d68e56 ">System</td>
<td class="entry tdcenter" align="center" valign="top" width="30.113636363636363%" headers="d68e58 ">x86_64 (64-bit) </td>
<td class="entry" valign="top" width="59.09090909090909%" headers="d68e60 "><span class="keyword">InfoSphere
Streams</span> supports Red Hat Enterprise Linux (RHEL), the Community Enterprise Operating
System (CentOS), and SUSE Linux Enterprise
Server (SLES).</td>
</tr>
<tr class="row"><td class="entry tdcenter" align="center" valign="top" width="30.113636363636363%" headers="d68e58 ">IBM® Power Systems™ (64-bit)</td>
<td class="entry" valign="top" width="59.09090909090909%" headers="d68e60 ">On RHEL systems that are running <span class="keyword">big endian</span>, <span class="keyword">InfoSphere
Streams</span> supports the POWER7® and POWER8® processors.<p class="p">RHEL systems
that are running <span class="keyword">little
endian</span> support
the POWER8 processor only.</p>
</td>
</tr>
<tr class="row"><td class="entry" valign="top" width="10.795454545454545%" headers="d68e56 ">Display</td>
<td class="entry tdcenter" align="center" valign="top" width="30.113636363636363%" headers="d68e58 ">1280 x 1024</td>
<td class="entry" valign="top" width="59.09090909090909%" headers="d68e60 ">Lower resolutions are supported but not preferred
for Streams Studio.</td>
</tr>
<tr class="row"><td class="entry" valign="top" width="10.795454545454545%" headers="d68e56 ">Memory</td>
<td class="entry tdcenter" align="center" valign="top" width="30.113636363636363%" headers="d68e58 ">2 GB</td>
<td class="entry" valign="top" width="59.09090909090909%" headers="d68e60 "><span class="ph" id="ibminfospherestreams-qse-hardware__d32e2110">The amount
of memory that is required by <span class="keyword">InfoSphere
Streams</span> is dependent on the applications that are developed
and deployed.</span><p class="p" id="ibminfospherestreams-qse-hardware__d32e2114">This minimum
requirement is based on the memory requirements of the Commodity Purchasing
sample application and other samples that are provided with the product.</p>
</td>
</tr>
<tr class="row"><td class="entry" rowspan="2" valign="top" width="10.795454545454545%" headers="d68e56 ">Disk space</td>
<td class="entry tdleft" align="left" valign="top" width="30.113636363636363%" headers="d68e58 ">7.5 GB, if installing the <span class="keyword">main installation
package</span></td>
<td class="entry" rowspan="2" valign="top" width="59.09090909090909%" headers="d68e60 ">Includes disk space required for
installation and development resources.</td>
</tr>
<tr class="row"><td class="entry tdleft" align="left" valign="top" width="30.113636363636363%" headers="d68e58 ">2 GB, if installing
the <span class="keyword">domain host installation
package</span> or <span class="keyword">resource installation
package</span>.</td>
</tr>
</tbody>
</table>
</div>

## Software Requirements

<div class="tablenoborder"><table cellpadding="4" cellspacing="0" summary="The first column of this table lists the Linux operating systems that are supported by InfoSphere Streams. The supported system hardware and architecture for each operating system is in the second column, and the supported operating system versions are in the third column." class="table" rules="all" frame="border" border="1"><thead class="thead" align="left"><tr class="row" valign="bottom"><th class="entry thcenter thbot" align="center" valign="bottom" width="15.753424657534246%" id="d68e79">Operating system</th>
<th class="entry thcenter thbot" align="center" valign="bottom" width="45.20547945205479%" id="d68e81">System hardware and architecture</th>
<th class="entry thcenter thbot" align="center" valign="bottom" width="39.04109589041096%" id="d68e83">Supported operating system versions</th>
</tr>
</thead>
<tbody class="tbody"><tr class="row"><td class="entry tdcenter" rowspan="5" align="center" valign="top" width="15.753424657534246%" headers="d68e79 ">RHEL</td>
<td class="entry tdcenter" rowspan="2" align="center" valign="top" width="45.20547945205479%" headers="d68e81 ">x86_64 (64-bit)</td>
<td class="entry tdcenter" align="center" valign="top" width="39.04109589041096%" headers="d68e83 ">Version 6.1, or later</td>
</tr>
<tr class="row"><td class="entry tdcenter" align="center" valign="top" width="39.04109589041096%" headers="d68e83 ">Version 7.0, or later</td>
</tr>
<tr class="row"><td class="entry tdcenter" rowspan="2" align="center" valign="top" width="45.20547945205479%" headers="d68e81 ">IBM Power
Systems (64-bit)<p class="p"><span class="keyword">InfoSphere
Streams</span> supports the POWER7® and POWER8® processors (<span class="keyword">big endian</span>).</p>
</td>
<td class="entry tdcenter" align="center" valign="top" width="39.04109589041096%" headers="d68e83 ">Version 6.3, or later</td>
</tr>
<tr class="row"><td class="entry tdcenter" align="center" valign="top" width="39.04109589041096%" headers="d68e83 ">Version 7.0, or later</td>
</tr>
<tr class="row"><td class="entry tdcenter" align="center" valign="top" width="45.20547945205479%" headers="d68e81 ">IBM Power Systems (64-bit)<p class="p"><span class="keyword">InfoSphere
Streams</span> supports the POWER8 processor
(<span class="keyword">little
endian</span>).</p>
</td>
<td class="entry tdcenter" align="center" valign="top" width="39.04109589041096%" headers="d68e83 ">Version 7.1, or later</td>
</tr>
<tr class="row"><td class="entry tdcenter" rowspan="2" align="center" valign="top" width="15.753424657534246%" headers="d68e79 ">CentOS</td>
<td class="entry tdcenter" rowspan="2" align="center" valign="top" width="45.20547945205479%" headers="d68e81 ">x86_64 (64-bit)</td>
<td class="entry tdcenter" align="center" valign="top" width="39.04109589041096%" headers="d68e83 ">Version 6.1, or later</td>
</tr>
<tr class="row"><td class="entry tdcenter" align="center" valign="top" width="39.04109589041096%" headers="d68e83 ">Version 7.0, or later</td>
</tr>
<tr class="row"><td class="entry tdcenter" align="center" valign="top" width="15.753424657534246%" headers="d68e79 ">SLES</td>
<td class="entry tdcenter" align="center" valign="top" width="45.20547945205479%" headers="d68e81 ">x86_64 (64-bit)</td>
<td class="entry tdcenter" align="center" valign="top" width="39.04109589041096%" headers="d68e83 ">Version 11.2, or later</td>
</tr>
</tbody>
</table>
</div>

## Resources

For more information about QSE for Linux system requirements, see the [Knowledge Center](http://www-01.ibm.com/support/knowledgecenter/SSCRJU_4.1.1/com.ibm.streams.qse.doc/doc/ibminfospherestreams-qse-before-you-begin.html?lang=en).

## Installation Instructions

To install QSE for Linux, see the 
[Knowledge Center](http://www-01.ibm.com/support/knowledgecenter/SSCRJU_4.1.1/com.ibm.streams.qse.doc/doc/ibminfospherestreams-qse-install.html?lang=en).


## What to do next

To explore QSE for Linux, see the [Getting Started Guide](/streamsx.documentation/docs/4.1/qse-getting-started/).
