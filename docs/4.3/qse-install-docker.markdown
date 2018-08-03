---
layout: docs
title:  Installing Streams Quick Start Edition with Docker
description:  Installation Guide for IBM Streams Docker Quick Start Edition
weight: 30
published: true
tag: 43qse
prev:
  file: qse-intro
  title:  Try Quick Start Edition
next:
  file: qse-getting-started
  title: Getting started

---


IBM® Streams Quick Start Edition can help you get started with Streams quickly, without having to install a Streams cluster environment.

## Introduction

This document describes the installation, configuration, first steps,
and common Docker management scenarios for Streams Quick Start
Edition running in a Docker environment.

### Overview
Here's an overview of the steps to get up and running:
 * [Install and configure Docker](#installconfigdocker).
 * [Set up a mapped directory](#map) on your local host file system for the Docker container.
 * [Download and install Streams Quick Start Edition](#getqse).
 * [Configure your `hosts` file](#conf).
 * Access the Streams Quick Start Edition:
    * Use a [VNC client](#vnc).
    * Use a [Secure Shell (SSH)](#ssh).
 * [Manage the Docker container](#manage).
 * [View the known issues](#known-issues).

## Supported environments

The following operating system and Docker environments are supported for Streams Quick Start Edition 4.3.

|   Operating system      | Docker        |
| -------------------- | -------------------- |
| Windows 10 | Docker Community Edition 17.03.1-ce or later |
| MacOS El Capitan 10.11 or later | Docker Community Edition 17.03.1-ce or later  |
|Linux systemd-based distribution | Docker Community Edition 17.03.1-ce or later. <br><br>Note: If you use Standard Docker (Red Hat), you must adjust the Docker environment manually to allow for 50 GB of Docker storage.   |

## Docker configuration requirements

Configure your Docker environment as follows.


|    Setting                  | Minimum        | Recommended |
| -------------------- | -------------------- | ----------------|
| CPUs | 2 | 4 |
| Memory | 4 GB  | 8 GB |
|Disk space | 20 GB   | 50 GB or greater depending upon number and size of projects. |

<a id="installconfigdocker"></a>
## Installing and configuring Docker

<ul class="nav nav-tabs">


  <li class="active" ><a data-toggle="tab" href="#docker-windows-0"> Windows</a></li>  
  <li ><a data-toggle="tab" href="#docker-macos-0">MacOS</a></li>
  <li><a data-toggle="tab" href="#docker-linux-0">Linux</a></li>
</ul>

<div class="tab-content">
<div id="docker-windows-0" class="tab-pane fade in active">
<ol>
<li>Download and install Docker-CE 17.03.1 or later from:  
<p><a href="https://store.docker.com/editions/community/docker-ce-desktop-windows">https://store.docker.com/editions/community/docker-ce-desktop-windows</a></p>
    <p>Note: Installing Docker might conflict with settings required for other
 VM technologies such as Oracle VM VirtualBox. The installation might
 also require that you set your VM technology settings in your BIOS
 settings. If this is necessary, Docker warns you when you try to
 start it and tells you which settings to change.</p></li>
<li>After you install Docker, configure it as follows:
<ol>
<li>    Right-click the Docker icon in the system tray and select    <b>Settings</b>.</li>
<li>    Under <b>Setting</b>, select <b>Shared Drives</b>. Share your hard disk drive (usually your C: drive).</li>
<li>    Under <b>Settings</b>, select <b>Advanced</b> and  configure the CPUs (minimum 2, recommended 4) and memory (minimum 4 GB, recommended 8 GB).</li></ol>
</li>
<li>Open a PowerShell session from the Windows menu and test that Docker is set up correctly by running this command:
<pre>
    docker run hello-world
</pre>
<p>If Docker is set up correctly, you will receive a response that includes the following text:
<pre>
Hello from Docker!
This message shows that your installation appears to be working correctly.
</pre></p>
</li></ol>
    </div>


<div id="docker-macos-0" class="tab-pane fade">
<ol><li>
Download and install Docker Community Edition for Mac from:
<p><a href="https://store.docker.com/editions/community/docker-ce-desktop-mac">https://store.docker.com/editions/community/docker-ce-desktop-mac</a></p>
</li>
<li>
After you install Docker, configure it as follows:
<ol><li>
    From the Docker icon in the menu, select <b>Preferences >         Advanced</b>.
</li><li>
    Configure the CPUs (minimum 2, recommended 4) and memory         (minimum 4 GB, recommended 8 GB).</li></ol>
</li>
<li>
Open a Terminal session and test that Docker is set up correctly by
    running this command:
<pre>
    docker run hello-world
</pre>
    If Docker is set up correctly, you will receive a response that includes this text:
  <pre>
   Hello from Docker!
   This message shows that your installation appears to be working
   correctly.
    </pre>
</li></ol>  
</div>  
	<div id="docker-linux-0" class="tab-pane fade">
<ol>
	<li>Use the OS package manager to install Docker Community Edition. (For Red Hat, install Standard Docker).
	</li>
	<li>If necessary, increase the Docker installation storage space for
    the Streams Quick Start Edition image.
    <div style="border:1px solid black;padding:2em;">
    <p>Tip: The amount of storage space that is needed depends on whether you map
    directories to the local file system and the amount and the size of
    your applications and data.
		<ul>
			<li>The Red Hat Standard Docker storage space is set to 10 GB. In this case, you must increase the storage space.</li>
			<li>Storage space for Docker-ce is usually set to 20 GB. In this case, you might need to increase the storage space.</li>
		</ul></p></div>
		<ol>
			<li>To set the Docker default image size (<b>Base Device Size</b>), log in as <b>root</b> or use <code>sudo</code> to create or edit the <code>/etc/docker/daemon.json</code> file.
			</li>
			<li>Add or modify the following code, where <code>XX</code> represents the default image size in GB.
				<ul>
					<li>If you keep the <code>/home/streamsadmin/workspace</code> directory in the Docker image, set the storage space to at least 50 GB.
					</li>
					<li>If you map the <code>/home/streamsadmin/workspace</code> to a local host directory, you can set the Docker storage to 20 GB, because projects and data can be stored on your local drive instead of inside the Docker container.
					</li>
				</ul>
<pre>
{
  "storage-opts": ["dm.basesize=XXG"]
}
</pre>
			</li>
		 </ol>
	</li>
	<li>Restart the docker service:
<pre>
sudo systemctl restart docker</pre>
	</li>
	<li>Verify the default image size by entering the following command:
<pre>docker info |grep "Base Device Size:"</pre>
	</li>
</ol>
</div>
</div>

<a id="map"></a>

## Mapping Docker container directories to the local host file system
*(Optional, but recommended)*

During the Streams Quick Start Edition installation, you are
prompted to map two Docker directories,
`/home/streamsadmin/workspace` and `/home/streamsadmin/hostdir`, to
local host directories.

Because the container has limited space, in most cases the best option
is to map to external directories. Doing so will help prevent the
container from exceeding its internal disk limits and make it easier for
you to back up your project data and upgrade your Streams Docker
container in the future.

1.  Create a directory on your host machine where you can keep both
    mapped directories isolated from other host machine files. For
    example, you might create a directory called `mappedDockerFiles` in the home directory of your host machine:  

    `mkdir <HOME DIRECTORY>/mappedDockerFiles`

    Important: Do not map the Docker files directly to the top-level user home
    directory.

2.  Make note of the directory. You will provide it during the Quick Start Edition installation.

The installation creates the mapped directories in your local host
file system within  `mappedDockerFiles` for two directories, the
internal *workspace* and *hostdir* subdirectories. During
installation, you are prompted for the names that you want to use
under `~/mappedDockerFiles`.

The following explains the use of the two directories.
* The *workspace* directory:  Streams projects created using Streams Studio would be stored in  `/home/streamsadmin/workspace` on the Docker container. By mapping the *workspace* directory to a folder on your local host, the projects stored in `/home/streamsadmin/workspace` will be stored on the mapped workspace directory on your local host machine. Storing them here  instead of in the internal Docker container means that you can reuse this directory for easy recovery of your projects.  For example, if you later upgrade your Streams4Docker installation, you use the Import function of Streams Studio to import the projects from a previous Streams4Docker installation.   

* The *hostdir* directory: If this directory is mapped to the local host file system, it corresponds to `/home/streamsadmin/hostdir` in the Docker container. Use it to store files  that you want to share between your Docker container and your
local host. Keep any large files that are used in your Streams4Docker container
in this directory when possible, because files in this directory do not
use up space inside the Docker container.

<a id="getqse"></a>

## Download and install Streams Quick Start Edition
After you configure Docker and map your directories, you are ready to download and install Quick Start Edition.

You have two options:
 * [Download and install from Docker Hub](#hubinstall)
 * [Download the container manually](#manual)

<a id="hubinstall"></a>

### Download and install from Docker Hub
The following sections contain sample commands for downloading and installing Quick Start Edition from Docker Hub.

<ul class="nav nav-tabs">
  <li class="active" ><a data-toggle="tab" href="#qse-docker-hub-windows-0"> Windows</a></li>  
  <li ><a data-toggle="tab" href="#qse-docker-hub-macos-linux-0">MacOS/Linux</a></li>
</ul>

<div class="tab-content">
<div id="qse-docker-hub-windows-0" class="tab-pane fade in active">
<p>The commands that you use to download and install the container on Windows depend on whether you choose to map the container directories.</p>

<p><b>Container with mapped directories</b></p>
<p>This command is based on using the following mapped directories, replacing <i>user</i> with your user name:
<pre>
C:\<i>user</i>\Documents\DockerMapped\workspace
C:\<i>user</i>\Documents\DockerMapped\hostdir</pre>
</p>
<p>Enter the following command, replacing <i>user</i> with your user name:
<pre>
docker run --privileged -d -v /sys/fs/cgroup:/sys/fs/cgroup:ro -v //c/<i>user</i>/Documents/DockerMapped/workspace:/home/streamsadmin/workspace -v //c/<i>user</i>/Documents/DockerMapped/hostdir:/home/streamsadmin/hostdir -p 8443:8443 -p 9975:9975 -p 8006-8016:8006-8016 -p 8444:8444 -p 8080:80 -p 5905:5901 -p 4022:22 --name streamsdocker4240 -h 'streamsqse.localdomain' ibmcom/streams-qse:4.3.0.0 INSTALL
</pre></p>

<p><b>Container without mapped directories</b></p>
<p>Enter the following command:
<pre>
docker run --privileged -d -v /sys/fs/cgroup:/sys/fs/cgroup:ro -p 8443:8443 -p 9975:9975 -p 8006-8016:8006-8016 -p 8444:8444 -p 8080:80 -p 5905:5901 -p 4022:22 --name streamsdocker4240 -h 'streamsqse.localdomain' ibmcom/streams-qse:4.3.0.0 INSTALL
</pre></p>
</div>

<div id="qse-docker-hub-macos-linux-0" class="tab-pane fade">
<p>The commands that you use to download and install the container on Mac or Linux depend on whether you choose to map the container directories.</p>

<p><b>Container with mapped directories</b></p>

<p>This command is based on setting the <code>MAPPED_WORKSPACE</code> and <code>MAPPED_HOSTDIR</code> variables to the mapped directories you created, for example:
<pre>
export MAPPED_WORKSPACE=$HOME/Documents/DockerMapped/workspace
export MAPPED_HOSTDIR=$HOME/Documents/DockerMapped/hostdir
</pre></p>
<p>After you export the mapped drives, enter the following command:
<pre>
docker run --privileged -d -v /sys/fs/cgroup:/sys/fs/cgroup:ro -v $MAPPED_WORKSPACE:/home/streamsadmin/workspace -v $MAPPED_HOSTDIR:/home/streamsadmin/hostdir -p 8443:8443 -p 9975:9975 -p 8006-8016:8006-8016 -p 8444:8444 -p 8080:80 -p 5905:5901 -p 4022:22 --name streamsdocker4240 -h 'streamsqse.localdomain' ibmcom/streams-qse:4.3.0.0 INSTALL
</pre></p>

<p><b>Container without mapped directories</b></p>
<p>Enter the following command:
<pre>
docker run --privileged -d -v /sys/fs/cgroup:/sys/fs/cgroup:ro -p 8443:8443 -p 9975:9975 -p 8006-8016:8006-8016 -p 8444:8444 -p 8080:80 -p 5905:5901 -p 4022:22 --name streamsdocker4240 -h 'streamsqse.localdomain' ibmcom/streams-qse:4.3.0.0 INSTALL
</pre></p>
</div>  

</div>

<a id="manual"></a>

## Manual download and installation
Prerequisite: Make sure you are connected to the Internet.
{% include download.html%}

<ul class="nav nav-tabs">
  <li class="active" ><a data-toggle="tab" href="#qse-windows-0"> Windows</a></li>  
  <li ><a data-toggle="tab" href="#qse-macos-linux-0">MacOS/Linux</a></li>
</ul>

<div class="tab-content">

<div id="qse-windows-0" class="tab-pane fade in active">
<ol><li>
Click <b>Download Streams Quick Start Edition</b> to go to the IBM Streams Quick Start Edition page. Download IBM Streams Quick Start Edition V4.3.0 for Docker on Windows 10.
</li>
<li>
Extract the <code>Streams4WindowsDocker4300EL7.zip</code> file into a directory.
</li>
<li>
Open PowerShell and go to the <code>Streams4WindowsDocker4300EL7</code> directory.
</li>
<li>
Ensure that you have permissions to run a PowerShell script:
    <ol><li>
    In the PowerShell window, determine your PowerShell execution policy:
    <pre>get-executionpolicy</pre>
    </li>
    <li>
    If your permissions are restricted, change them to unrestricted:
    <pre>set-executionpolicy unrestricted</pre>
    <p>Tip: After you complete the installation, optionally reset your execution policy back to restricted by entering the following command:
    <pre>set-executionpolicy restricted</pre></p>
    </li></ol></li>
<li>
Run the install script by entering the following command:
<pre>./streamsdockerInstall.ps1</pre>
</li>
<li>
Follow the installation instructions.
    <ol><li>
    Read and accept the license agreement page and the Notices page.
    </li>
    <li>
    Choose whether to map host local directories into the Docker container.
 If you have not created a local directory for this purpose, see <a href="#mapping-docker-container-directories-to-the-local-host-file-system">Mapping Docker container directories to the local host
 file  system</a>.
    </li>
    <li>
    Confirm the directories and start the installation.
    </li>
    </ol>
</li>
</ol>

</div>

<div id="qse-macos-linux-0" class="tab-pane fade">
<ol><li>
Click <b>Download Streams Quick Start Edition</b> to go to the IBM Streams Quick Start Edition page and use the following instructions for your operating system.
</li>
<li>
Extract the <code>Streams4Docker4300EL7</code> file into a directory.
</li>
<li>
From your Terminal session, change to the <code>Streams4Docker4300EL7</code> directory.
</li>
<li>
Run the install script by entering the following command:
<pre>./streamsdockerInstall.sh</pre>
</li>
<li>
Follow the installation instructions.
    <ol><li>
    Read and accept the license agreement page and the Notices page.
    </li>
    <li>
    Choose whether to map host local directories into the Docker container.
 If you have not created a local directory for this purpose, see <a href="#mapping-docker-container-directories-to-the-local-host-file-system">Mapping Docker container directories to the local host
 file  system</a>.
    </li>
    <li>
    Confirm the directories and start the installation.
    </li>
    </ol>
</li>
</ol>
</div>  

</div>

The installation takes from 25 minutes
to an hour or more depending on your host system configuration. When
the installation is complete, you are returned to a `Streams4Docker`
command prompt.

<a id="conf"></a>
## Configuring the hosts file

Streams operates by using a host name and
expects DNS to provide the conversion from host name to IP
address. Because Streams Quick Start Edition does not have a DNS server,
you can simulate one by using the `hosts` file.
Before you can access Streams Quick Start Edition, you must set the
`hosts` file to point the host name **streamsqse.localdomain** to the
127.0.0.1 loopback address.

<ul class="nav nav-tabs">
  <li class="active" ><a data-toggle="tab" href="#hosts-windows-0"> Windows</a></li>  
  <li ><a data-toggle="tab" href="#hosts-macos-linux-0">MacOS/Linux</a></li>
</ul>

<div class="tab-content">
<div id="hosts-windows-0" class="tab-pane fade in active">
<ol>
<li>
Open a text editor as an administrator. For example, for Notepad, find Notepad in your Windows menu, right-click it, and
    select **Run as Administrator**.
</li>
<li>Open <code>C:\Windows\System32\drivers\etc\hosts</code>.
<p>Tip: Set the Notepad filename filter to "All Files" to see the `hosts`
file.</p>
</li>
<li>Append <code>streamsqse streamsqse.localdomain</code> to the line that has the
    loopback address. For example:
    <pre>
    127.0.0.1 localhost streamsqse streamsqse.localdomain
    </pre>
</li>
<li>
Save and close the file.
</li>
</ol>
</div>

<div id="hosts-macos-linux-0" class="tab-pane fade">
<ol>
<li>
Open a text editor with <b>root</b> authority.
</li>
<li>Open <code>/etc/hosts</code>.
</li>
<li>Append <code>streamsqse streamsqse.localdomain</code> to the line that has the
    loopback address. For example:
    <pre>
    127.0.0.1 localhost streamsqse streamsqse.localdomain
    </pre>
</li>
<li>
Save and close the file.
</li>
</ol>
</div>  

</div>

<a id="vnc"></a>
## Accessing Streams Quick Start Edition with a VNC client

Use port **5905** to access Streams Quick Start Edition in the Docker
container with a VNC client.

1.  Open your VNC Client and connect to the VNC server:

    **streamsqse.localdomain:5905**

2.  When you are prompted for a password, enter:

    **passw0rd**

 The default user name for the Streams Console is **streamsadmin**.

 On the Streams desktop, access the Streams applications from the
 **Applications** menu.


 <a id="ssh"></a>
## Accessing Streams Quick Start Edition with Secure Shell (SSH)

You can use **ssh** to access the container by specifying the **streamsqse.localdomain** and using port **4022**. For example:

`ssh -p 4022 streamsadmin@streamsqse.localdomain`

By default, all passwords are **passw0rd** within an ssh session. If you
use the user name **streamsadmin** and you want to run a command
as **root**, you can use one of two methods:

-   **sudo \[command\]** Provide your **streamsadmin** password when you are
    prompted. You run commands by using **sudo** and return to streamsadmin ID
    after the command is completed.

-   **sudo su -** Provide your **streamsadmin** password when you are prompted.
    You will be logged in as **root**. To return to the **streamsadmin**
    user ID, enter: **exit**.

<a id="manage"></a>
## Managing the Docker container

The following commands are useful for managing your Docker container
with Streams Quick Start Edition.

### Opening a session on Docker

You can use the **attach** command or the **exec** command to open a
session on Docker.

The difference between the **attach** and **exec** commands is that the
**attach** command takes you into the main root session. The main root session which might be
busy doing other functions (for example, it might be in the process of
starting streams), which will prevent you from doing useful work, but
will allow for better troubleshooting in case of a problem. The
**exec** command opens a new separate root session.

**Attaching to a running Docker container**

1.  Open PowerShell (Windows) or Terminal (MacOS or Linux).

2.  Determine the name of the session by entering **docker ps**. The container **streamsdocker4300** is displayed with a status of `running`.

3.  Attach to the container by entering this command:

    `docker attach streamsdocker4300`

    This command takes you to the Docker container Linux prompt.

**Running a command in a running container with the exec command**

Enter the Docker **exec** command:

  `docker exec -ti streamsdocker4300 /bin/bash`

### Detaching from the container

From within your attached Docker session, you can detach from the
session and still leave session active.

1. Use the appropriate key combination for your environment:
    -  Windows or Linux: **Ctrl-q-p**
    -  MacOS: **command-q-p**

    Important: If you are attached to a container and enter **exit**, it might cause the
container to stop.

2. (Optional) Close the PowerShell or Terminal session.

### Pausing and restarting the container

You can pause a container when it is not in use. The container pauses and all activity inside the container stops. You can unpause the container to use it again.

1.  If you are running external programs that are connected to the
    container, close them.

1.  From a PowerShell (Windows) or Terminal (MacOS or Linux) session, enter the appropriate command:
    -   To pause the container:
        ```
        docker pause streamsdocker4300
        ```

    -   To unpause the container:
        ```
        docker unpause streamsdocker4300
        ```

### Stopping and restarting the container

Typically, you manage a container by pausing and unpausing it. But sometimes you might need to stop and restart the container, for
example, for a reboot.

From a PowerShell (Windows) or Terminal (MacOS or Linux) session, enter the appropriate command:

-   To stop a container:

    ```
    docker stop streamsdocker4300
    ```

-   To restart a container:

    ```
    docker restart streamsdocker4300
    ```

    Tip: When a container is restarted, it takes a few minutes for the system to come back up and start the domains. To see the status, you can use
    VNC to access the desktop, where you can see the yellow desktop icon
    (Streams Domain Starting) while the domain is starting. The icon
    turns green (Streams Domain Started) when the domain is ready. The icon
    eventually disappears.

## Adjusting the desktop screen size for VNC

When you first access Streams Quick Start Edition with VNC, you will see
the Streams desktop.

If you are accustomed to earlier versions of Streams Quick Start
Edition, you will notice that there are no longer any desktop icons. All
Streams Quick Start Edition resources have been moved to the
**Applications \> Favorites** menu, which you can access from the top
left of the screen. There you will find the Streams applications and
links to resource web pages.

To adjust the display size to closer match your physical display, follow
these steps:

1.  Go to **Applications \> System Tools \> Settings**.

2.  Click **Devices > Displays**.

3.  In the **Displays** app, click **Resolution**.

4.   Select the resolution that best matches your physical display. Close the **Resolution** list by clicking 'x' in the corner.  Click **Apply**.

5.  Click **Keep Changes.**

## Known issues

#### **Description**: Running `streamsdockerInstall.sh` fails with the following message:

  ```
  TASK [install Streams prereq packages with yum] ********************************
  changed: [streamsqse.localdomain] => (item=readline)
  failed: [streamsqse.localdomain] (item=requests) => {“changed”: false, “cmd”: “/usr/bin/pip2 install -U requests”, “item”: “requests”, “msg”: “stdout: Collecting requests\n
  ...<snip>...
  Installing collected packages: certifi, chardet, idna, urllib3, requests\n  Found existing installation: chardet 2.2.1\n    Uninstalling chardet-2.2.1:\n      Successfully uninstalled chardet-2.2.1\n  Found existing installation: idna 2.4\n    Uninstalling idna-2.4:\n      Successfully uninstalled idna-2.4\n  Found existing installation: urllib3 1.10.2\n    Uninstalling urllib3-1.10.2:\n      Successfully uninstalled urllib3-1.10.2\n

  Found existing installation: requests 2.6.0\n\n:stderr: ipapython 4.5.0 requires pyldap>=2.4.15, which is not installed.\nrtslib-fb 2.1.63 has requirement pyudev>=0.16.1, but you’ll have pyudev 0.15 which is incompatible.\nipapython 4.5.0 has requirement dnspython>=1.15, but you’ll have dnspython 1.12.0 which is incompatible.\nCannot uninstall ‘requests’. It is a distutils installed project and thus we cannot accurately determine which files belong to it which would lead to only a partial uninstall.\n”}

  changed: [streamsqse.localdomain] => (item=future)
  changed: [streamsqse.localdomain] => (item=dill)
      to retry, use: --limit @/root/ansible/streamsdockerCentos7.retry

  PLAY RECAP *********************************************************************
  streamsqse.localdomain     : ok=41   changed=32   unreachable=0    failed=1  
  ```

**Cause**: This might be caused by a change in the Python repositories.

**Workaround:**
1. In the Quick Start Edition installation directory, locate the `Ansible/streamsdockerCentos7.yaml` file and open it in a text editor.
1. Locate the following section:
    ```
    ######### Python Module installation ####################################

    name: install Streams prereq packages with yum
    pip: name={{item}} state=latest
    with_items:

    readline
    requests
    future
    dill
    ```
1. Change `requests` to `request`.
1. Save the file.
1. Remove the old container:
    ```
    docker stop streamsdocker4300
    docker rm streamsdocker4300
    ```
7. Reinstall Quick Start Edition.

#### **Description**: Streams Studio Project Explorer: Right-clicking a file or folder, and then selecting **Show in \> System Explorer** throws a dbus error.

**Cause**: CentOS 6 Nautilus is not compatible with dbus API.

**Workaround**:

1.  Open Streams Studio.

2.  Go to **Window \> Preferences \> General \> Workspace**.

3.  Set **Command for launching system explorer** as follows:  
    ```
    nautilus "${selected_resource_parent_loc}"
    ```

## Getting help
If your problem is not discussed in the known issues section, you can ask a question on the [Streamsdev forum](https://developer.ibm.com/answers/smart-spaces/22/streamsdev.html).
