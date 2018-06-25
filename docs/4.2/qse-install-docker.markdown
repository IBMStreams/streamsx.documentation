---
layout: docs
title:  Installing Streams Quick Start Edition with Docker
description:  Installation Guide for IBM Streams Quick Start Edition Docker
weight: 30
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

## Introduction

This document describes the installation, configuration, first steps,
and common Docker management scenarios for IBM® Streams Quick Start
Edition running in a Docker environment.

### Overview
Here's an overview of the steps to get up and running:
 * [Download and install Docker](https://www.docker.com/community-edition)
 * Configure Docker's storage requirements:
    * Instructions for  <a href="#winconf">Windows</a>, <a href="#macconf">MacOS</a>, and <a href="#linuxconf">Linux</a>.  
 * (Optional, but recommended):  <a href="#map">Set up a mapped directory </a>on your local host filesystem for the Docker container.
 * <a href="#getqse">Download and install the Streams Quick Start Edition</a>
 * <a href="#conf">Configure your *hosts* file.</a>
 *  Access the Streams Quick Start Edition:
    * Use a <a href="#vnc"> VNC client</a>
    * Via <a href="#ssh">Secure Shell (SSH)</a>.
 * <a href="#manage">Managing the Docker container</a>
 * <a href="#known-issues">Known issues</a>
 * <a href="#getting-help">Getting help</a>

## Supported environments

Windows 10, running Docker Community Edition 17.03.1-ce or later.

MacOS El Capitan 10.11 or later, running Docker Community Edition
17.03.1-ce or later.

Linux: It is recommended to use a systemd-based distribution with Docker
Community Edition 17.03.1-ce or later. If you use the Standard Docker
(Red Hat), you will need to adjust the Docker environment manually for
50 GB of Docker storage.

## Docker configuration requirements

Configure your Docker environment as follows.


|                      | Minimum        | Recommended |
| -------------------- | -------------------- | ----------------|
| CPUs | 2 | 4 |
| Memory | 4 GB  | 8 GB |
|Disk space | 20 GB   | 50 GB or greater depending upon number and size of projects. |

<a id="winconf"></a>

## Installing and configuring Docker on Windows

1.  Download and install Docker-CE 17.03.1 or later from:  

    [https://www.docker.com/community-edition](https://www.docker.com/community-edition)

    Note: Installing Docker may conflict with settings required for other
 VM technologies such as Oracle VM VirtualBox. The installation may
 also require that you set your VM technology settings in your BIOS
 settings. If this is necessary, Docker will warn you when you try to
 start it and tell you which settings to change.

2.  After you install Docker, configure it as follows:

    a.  Right-click the Docker icon in the system tray, and then select    **Settings**.

    b.  Under **Settings**, select **Shared Drives,** and then share       your hard disk drive (usually your C: drive).

    c.  Under **Settings**, select **Advanced**, and then configure the    CPUs (minimum 2, recommended 4) and Memory (minimum 4 GB,   recommended 8 GB).

3.  Open a PowerShell session from the Windows menu and test that Docker is set up correctly by running this command:

    **docker run hello-world**

    You should receive a response that includes this text:
  <pre>
   Hello from Docker!
   This message shows that your installation appears to be working
   correctly.
    </pre>

<a  id="macconf"></a>
## Installing and configuring Docker on MacOS

1.  Download and install Docker Community Edition for Mac from:

    [https://store.docker.com/editions/community/docker-ce-desktop-mac](https://store.docker.com/editions/community/docker-ce-desktop-mac)

2.  After you install Docker, configure it as follows:

    a.  From the Docker icon in the menu, click **Preferences >         Advanced**.

    b.  Configure the CPUs (minimum 2, recommended 4) and Memory         (minimum 4 GB, recommended 8 GB).

3.  Open a Terminal session and test that Docker is set up correctly by
    running this command:

    **docker run hello-world**

    You should receive a response that includes this text:
  <pre>
   Hello from Docker!
   This message shows that your installation appears to be working
   correctly.
    </pre>

<a id="linuxconf"></a>
## Installing and configuring Docker on Linux

1.  Use the OS package manager to install Docker-ce (or for Red Hat,
    install the standard Docker).

2.  Confirm that the Docker installation has enough storage space for
    the Streams Quick Start Edition image.

    Red Hat's Standard Docker storage space is set to 10 GB. You will
 need to increase the storage space.

    Docker-ce is usually set to 20 GB. Depending on whether you will map
 directories to the local file system and the amount and the size of
your applications and data, you might need to increase that limit
before you install the Streams Quick Start Edition image.

    During the Streams Quick Start Edition installation, you will be
 prompted if you want to map two Docker directories, **/home/streamsadmin/workspace** and **/home/streamsadmin/hostdir**, to local host directories.

    -   If you will be leaving the **/home/streamsadmin/workspace**
    directory in the Docker image, then set the storage space to at
    least 50 GB.

    -   If you will be mapping the **/home/streamsadmin/workspace** to a
    local host directory, then you can set the Docker storage to 20 GB
    because projects and data can be stored on your local drive instead
    of inside the Docker container.

    To set the Docker default image size, continue with the following steps:

3.  Log in as **root** or use **sudo** to create or edit the
    **/etc/docker/daemon.json** file. The file should contain the
    following code where *XX* represents the default image size in GB:

     <pre>       {
           "storage-opts": ["dm.basesize=XXG"]
           }
     </pre>

4.  Verify the setting by restarting the docker service and confirming
    the Base Device Size by running these commands:

      **sudo systemctl restart docker**  
      **docker info \|grep "Base Device Size:"**

<a id="map"></a>

## Mapping Docker container directories to the local host file system

During the Streams Quick Start Edition installation, you will be
prompted if you want to map two Docker directories,
**/home/streamsadmin/workspace** and **/home/streamsadmin/hostdir**, to
local host directories.

Because the container has limited space, in most cases the best option
is to map to external directories. Doing so will help prevent the
container from exceeding its internal disk limits and make it easier for
you to back up your project data and upgrade your Streams Docker
container in the future.

1.  Create a new directory on your host machine where you can keep both
    mapped directories isolated from other host machine files. For
    example:  

    **&lt;HOME DIRECTORY\>/mappedDockerFiles**

    Important: Do not map the Docker files to the top-level user home
    directory.

2.  Make note of the directory. You will need to provide it during
    installation.

The installation will create the mapped directories in your local host
file system under **&lt;HOME DIRECTORY>/mappedDockerFiles** for the
internal **workspace** and **hostdir** subdirectories. During
installation, you will be prompted for the names that you want to use
under **&lt;HOME DIRECTORY\>/mappedDockerFiles**.

When you create Streams projects, the data files will be
located in the **workspace** directory. If this directory is mapped to the local host file system,
the files and directories will be stored there instead in the internal
Docker container. If later you upgrade your Streams4Docker installation,
you can reuse this directory for easy recovery of your projects. For
example, if you use the Import function of Streams Studio and point to
the **workspace** directory, the program will recognize all your project
data. You can import all your projects using **overwrite** option.

The **hostdir** directory begins as an empty directory where you can add
files that you want to share between your Docker container and your
local host. Keep any large files used in your Streams4Docker container
in this directory when possible because files in this directory do not
use up space inside the Docker container.


<a id="getqse"></a>

## Download and install the Streams Quick Start Edition
After configuring Docker and mapping your directories, you are now ready to download and install the Quick Start Edition.

You have 2 options:
 * [Download and install from Docker Hub](#hubinstall)
 * [Download the container manually](#manual)

## Download and install from Docker Hub
Below are sample commands for each major operating system.

### Downloading and starting the container on Mac or Linux


**Container with mapped directories:**

The command is based on setting the `MAPPED_WORKSPACE` and `MAPPED_HOSTDIR` variables to the mapped directories you created, e.g.
```
export MAPPED_WORKSPACE=/home/<user>/Documents/DockerMapped/workspace
export MAPPED_HOSTDIR=/home/<user>/Documents/DockerMapped/hostdir
```
Then run
```
docker run --privileged -d -v /sys/fs/cgroup:/sys/fs/cgroup:ro -v $MAPPED_WORKSPACE:/home/streamsadmin/workspace -v $MAPPED_HOSTDIR:/home/streamsadmin/hostdir -p 8443:8443 -p 9975:9975 -p 8006-8016:8006-8016 -p 8444:8444 -p 8080:80 -p 5905:5901 -p 4022:22 --name streamsdocker4240 -h 'streamsqse.localdomain' ibmcom/streams-qse:4.2.4.0 INSTALL
```

**Container without mapped directories:**
```
docker run --privileged -d -v /sys/fs/cgroup:/sys/fs/cgroup:ro -p 8443:8443 -p 9975:9975 -p 8006-8016:8006-8016 -p 8444:8444 -p 8080:80 -p 5905:5901 -p 4022:22 --name streamsdocker4240 -h 'streamsqse.localdomain' ibmcom/streams-qse:4.2.4.0 INSTALL
```

#### Downloading and starting the container on Windows

Container with mapped directories:

The command is based on using the following mapped directories:

**C:\<user>\Documents\DockerMapped\workspace**
**C:\<user>\Documents\DockerMapped\hostdir**
```
docker run --privileged -d -v /sys/fs/cgroup:/sys/fs/cgroup:ro -v //c/<user>/Documents/DockerMapped/workspace:/home/streamsadmin/workspace -v //c/<user>/Documents/DockerMapped/hostdir:/home/streamsadmin/hostdir -p 8443:8443 -p 9975:9975 -p 8006-8016:8006-8016 -p 8444:8444 -p 8080:80 -p 5905:5901 -p 4022:22 --name streamsdocker4240 -h 'streamsqse.localdomain' ibmcom/streams-qse:4.2.4.0 INSTALL
```

**Container without mapped directories**
```
docker run --privileged -d -v /sys/fs/cgroup:/sys/fs/cgroup:ro -p 8443:8443 -p 9975:9975 -p 8006-8016:8006-8016 -p 8444:8444 -p 8080:80 -p 5905:5901 -p 4022:22 --name streamsdocker4240 -h 'streamsqse.localdomain' ibmcom/streams-qse:4.2.4.0 INSTALL
```


## Manual download and installation
{% include download.html%}
Download the QSE using the link above, and then follow the instructions below for Windows, and <a href="#macinstall">Mac/Linux</a>


## Installing Streams Quick Start Edition manually on Windows

   Prerequisite: Make sure you are connected to the Internet.

1.  Unzip the **Docker&lt;version\>.zip** file into a preferred directory.

2.  Open PowerShell, and change to the **streams4docker&lt;version\>**
    directory.

3.  Confirm you have permissions to run a PowerShell script:

    a.  In the PowerShell window, determine your PowerShell execution policy:

      **get-executionpolicy**

    b.  If your permissions are restricted, change them to unrestricted:

      **set-executionpolicy unrestricted**

    c.  Optional: Reset your execution policy back to restricted:

      **set-executionpolicy restricted**

4.  Run the install script:

    **./streamsdockerInstall.ps1**

5.  Read and accept the license agreement page, and then the Notices
    page.

6.  Choose whether to map host local directories into Docker container.
    See [**Mapping Docker container directories** **to the local host
    file
    system**](#mapping-docker-container-directories-to-the-local-host-file-system)
    information above.

7.  Confirm the directories and install.

 The installation will continue automatically and take from 25 minutes
 to an hour or more depending on your host system configuration. When
 the installation completes, you are returned to a `Streams4Docker`
 command prompt.

<a id="macinstall"></a>
## Installing Streams Quick Start Edition on MacOS or Linux

Prerequisite: Make sure you are connected to the Internet.

1.  Unzip the **Docker&lt;version\>.zip** file into your preferred
    directory.

2.  From your Terminal session, change to the
    **streams4docker&lt;version>** directory.

3.  Run the install script:

    **./streamsdockerInstall.sh**

4.  Read and accept the license agreement page, and then the Notices
    page.

5.  Choose whether to map host local directories into Docker container.
    See [**Mapping Docker container directories to the local host file
    system**](#mapping-docker-container-directories-to-the-local-host-file-system)
    information above.

6.  Confirm the directories and install.

 The installation will continue automatically and take from 25 minutes
 to an hour or more depending on your host system configuration. When
 the installation completes, you are returned to a `Streams4Docker`
 command prompt.


<a id="conf"></a>
## Configuring the hosts file

Before accessing Streams Quick Start Edition, you need to set the
**hosts** file to point the hostname **streamsqse.localdomain** to the
127.0.0.1 loopback address. Streams operates using a hostname and
usually expects DNS to provide the conversion from hostname to IP
address. Because Streams Quick Start Edition does not have a DNS server,
we will simulate one using the **hosts** file.

1.  Open your text editor:

    -   Windows: Find Notepad in your Windows menu, right-click it and
    select **Run as Administrator**.

    -   MacOS or Linux: Open a text editor with **root** authority.

2.  Locate and open the **hosts** file:

    -   Windows: In Notepad open:
    **C:\\Windows\\System32\\drivers\\etc\\hosts**
    (Set Notepad filename filter to "All Files" to see the **hosts**
    file.)

    -   MacOS or Linux: Open the **/etc/hosts** file.

3.  Append `streamsqse streamsqse.localdomain` to the line that has the
    loopback address. For example:

    <pre>
    127.0.0.1 localhost streamsqse streamsqse.localdomain
    </pre>

4.  Save and close the file.


<a id="vnc"></a>
## Accessing Streams Quick Start Edition with a VNC client

Use port **5905** to access Streams Quick Start Edition in the Docker
container with a VNC client.

1.  Open your preferred VNC Client and connect to:

    **streamsqse.localdomain:5905**

2.  When prompted for a password use:

    **passw0rd**

 The default user name for the Console is **streamsadmin**.

 On the Streams desktop, you access the Streams applications from the
 **Applications** menu.


 <a id="ssh"></a>
## Accessing Streams Quick Start Edition with Secure Shell (SSH)

You can use **ssh** to access the container by specifying **streamsqse.localdomain** and using port **4022**. For example:

 **ssh -p 4022 streamsadmin@streamsqse.localdomain**

By default, all passwords are **passw0rd** within an ssh session. If you
are using the user name **streamsadmin** and you want to run a command
as **root**, you can use one of two methods:

-   **sudo \[command\]** Provide your **streamsadmin** password when
    prompted. You run commands using sudo and return to streamsadmin ID
    after the command is completed.

-   **sudo su -** Provide your **streamsadmin** password when prompted.
    You will be logged in as **root**. To return to the **streamsadmin**
    user ID, type: **exit**.

<a id="manage"></a>
## Managing the Docker container

Following are some useful commands for managing your Docker container
with Streams Quick Start Edition.

### Opening a session on Docker


You can use the **attach** command or the **exec** command to open a
session on Docker.

The difference between the **attach** and **exec** commands is that the
**attach** command takes you into the main root session, which may be
busy doing other functions (for example, it might be in the process of
starting streams), which will prevent you from doing useful work, but
will allow for better troubleshooting in case of a problem; whereas the
**exec** command opens a new separate root session.

#### Attaching to a running Docker container

1.  Open a PowerShell (Windows) or Terminal (MacOS or Linux).

2.  Determine the name of the session by typing **docker ps**. You
    should see the container **streamsdocker4240** as `running`.

3.  Attach by running this command:

    **docker attach streamsdocker4240**

This will take you to the Docker container Linux promote.

#### Running a command in a running container with the exec command

Docker **exec** command:

  **docker exec -ti streamsdocker4240 /bin/bash**

### Detaching from the container


From within your attached Docker session, you can detach from the
session gracefully, while leaving the session active by using the key
combination **Ctrl-q-p**. (Windows and Linux) or **command-q-p**.
(MacOS).

Note: If you are attached and type **exit**, it might cause the
container to stop.

You can now close the PowerShell or Terminal session.

### Pausing and unpausing the container

Often you might want to pause a container when it is not in use. Then
you can unpause the container when you need it.

1.  Open a PowerShell (Windows) or Terminal (MacOS or Linux).

2.  If you are running external programs that are connected to the
    container, close them.

3.  To pause the container, type **docker pause streamsdocker4240**. The
    container will go to sleep. All activity inside the container stops.

4.  When you are ready to return to using the container, open PowerShell
    (Windows) or Terminal (MacOS or Linux) and type **docker unpause
    streamsdocker4240**.

### Stopping and restarting the container

Ordinarily, stopping and restarting the container is not a recommended
way to manage the container. But sometimes you might need to do it. For
example, for a reboot.

To stop a container, open PowerShell (Windows) or Terminal (MacOS or
Linux), and type:

   **docker stop streamsdocker4240**

To start a container, open PowerShell (Windows) or Terminal (MacOS or
Linux), and type:

   **docker restart streamsdocker4240**

When restarting a container, it takes a few minutes for the system to
come back up and start the domains. The recommended practice is to use
VNC to access the desktop where you can see the yellow desktop icon
(Streams Domain Starting) while the domain is being started. The icon
turns green (Streams Domain Started) when the domain is ready, and then
eventually disappears.

## Adjusting the desktop screen size for VNC

When you first access Streams Quick Start Edition with VNC you will see
the Streams desktop.

If you are accustomed to earlier versions of Streams Quick Start
Edition, you will notice that there are no longer any desktop Icons. All
Streams Quick Start Edition resources have been moved to the
**Applications \> Favorites** menu, which you can access from the top
left of the screen. There you will find the Streams applications and
links to resource web pages.

To adjust the display size to closer match your physical display, follow
these steps:

1.  Go to **Applications \> System Tools \> Settings**.

2.  Click the **Displays** icon.

3.  In the **Displays** app, click **Unknown Display**.

4.  Click **Resolution** and select the resolution that best matches
    your physical display, and then click **Apply**.

5.  Click **Keep Changes.**

## Known issues

1. **Description**: Running `streamsdockerInstall.sh` fails with the following message:

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

    **Cause**: This seems to be caused by a change in the Python repositories.

    **Workaround:**
    1. Go to the QSE install directory and locate the `Ansible/streamsdockerCentos7.yaml` file.
    2. Open the `streamsdockerCentos7.yaml` file in your favorite editor.
    3. Locate the following section:
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
    4. Change `requests` to `request`.
    5. Save the file.
    6. Remove the old container:
        ```
        docker stop streamsdocker4240
        docker rm streamsdocker4240
        ```
    7. Re-run the installation.

2. **Description**: Streams Studio Project Explorer: Right-clicking a file
or folder, and then selecting **Show in \> System Explorer** throws a
dbus error.

    **Cause**: CentOS 6 Nautilus is not compatible with dbus API.

    **Workaround**:

    1.  Open Streams Studio.

    2.  Go to **Window \> Preferences \> General \> Workspace**.

    3.  Set **Command for launching system explorer** to:  

        <pre>nautilus "${selected_resource_parent_loc}"</pre>

## Getting Help
If your problem is not discussed in the known issues section above, <a href="https://developer.ibm.com/answers/smart-spaces/22/streamsdev.html">please ask a question on the forums</a>.
