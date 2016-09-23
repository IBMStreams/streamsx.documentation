---
layout: docs
title:  Installing Streams Quick Start Edition Docker
description:  Installation Guide for IBM Streams Quick Start Edition Docker
weight: 30
published: false
---

**(Coming Soon...)**

The Streams Quick Start Editor can help you get started with Streams quickly, without having to install a Streams cluster environment.

{% include download.html%}

## System Requirements

| Components  | Minimum Requirements | Comments |
| ----------- | -------------------- | -------------|
| Operating System  | 64-bit operating system that supports Docker  | Streams Quick Start Docker image is supported on the following operating systems: <br>- Apple Mac OS X<br>- Microsoft Windows
| Memory	  |8 GB	                 |The amount of memory that is required by IBM Streams is dependent on the applications that are developed and deployed.  This minimum requirement is based on the memory requirements of the Commodity Purchasing sample application and other samples that are provided with the product.     
| Disk space  | 50 GB |  |
| Docker product | Docker Toolbox 1.9.0b or newer	| |

<p>
<div class="alert alert-danger" role="alert"><b>IMPORTANT:</b> If you already have boot2docker installed, remove all components (docker, Git, and Oracle VirtualBox) before installing 'Docker Toolbox'</div>

<div class="alert alert-danger" role="alert"><b>IMPORTANT:</b> If you have 'Docker Toolbox' already installed remove older version of Streams4Docker images and containers, and if there already exists a VirtualBox VM names 'streams4100', delete that as well. </div>
</p>

## Windows

1.  Install Dockertoolbox
    * See Docker Toolbox page for instructions:  https://www.docker.com/toolbox
1.  Install using all defaults for a 'Full Installation'
1.  Download the Streams4Docker.zip archive
1.  Extract the Streams4Docker.zip archive to preferred location
1.  Open Windows PowerShell
    * Application Menu-> All Programs -> Accessories -> Windows Powershell -> Windows PowerShell
    * `cd <Directory where Streams4Docker downloaded>/Docker`
    * `powershell -ExecutionPolicy ByPass -File Streams-windows-build.ps1`

Note: default build is 4096 MB Memory; 4 CPUs; 50000 Bytes disk.

To change defaults, for example to 8192 MB Memory; 2 CPUs; 60000 Bytes of disk run

~~~~~~
powershell -ExecutionPolicy ByPass -File Streams-windows-build.ps1 8192 2 60000
~~~~~~

<div class="alert alert-warning" role="alert">
Building and running of the Docker container will take about 20 minutes.
You may be prompted for Administration Authentication several times.
When completed the Powershell terminal will be sitting at the root prompt inside the Docker container.
It is recommended that you leave the terminal open.
</div>

## Mac OSx

1.  Install Dockertoolbox
    * See Docker Toolbox page for instructions:  https://www.docker.com/toolbox
1.  Install using all defaults for a 'Full Installation'
1.  Download the Streams4Docker.zip.  
1.  Copy the zip file to your home directory or any directory under your home directory:  `cp Streams4Docker.zip /Users/<userid>`
1.  Extract the zip file:  `unzip Streams4Docker.zip`
1.  Open a terminal and change to the Docker directory:  `cd Docker`
1.  Run the script to build the docker image:  `./Streams-OSX-build.sh`


Note: default build is 4096 MB Memory; 4 CPUs; 50000 Bytes disk.

To change defaults, for example to 8192 MB Memory; 2 CPUs; 60000 Bytes of disk run

~~~~~~
./Streams-OSX-build.sh 8192 2 60000
~~~~~~

<div class="alert alert-warning" role="alert">
Build and Run of Docker Container will take about 20 minutes. When completed the terminal will be sitting at the root prompt inside the Docker container.  It is recommended that you leave the terminal open.
</div>

## Accessing the IBM Streams Docker container

The Streams Docker container is set up with the following user id and password:

* User ID:  streamsadmin
* Password:  passw0rd
* Root:  passw0rd

After the containers finish the startup process, you should be able to access the container via:

* Remote Desktop Support from OSx:
    1. Open Finder Window
    1. Select Go -> Connect to Server...
    1. In the Server Address field, enter:  **vnc://127.0.0.1:5901**
    1. Click "+"
    1. Click "Connect"
* VNC Client:
    1. If not already installed, installed a VNC client.
    1. Start the VNC client
    1. Connect to **127.0.0.1:5901**

## Streams Console

You may use the Streams Console outside of the docker container.  To open Streams Console:

1.  Open a browser on your machine (Firefox or Chrome)
1.  Open this URL:  https://127.0.0.1:8443/streams/domain/console

## Streams Studio

Streams Studio may be accessed via a VNC session.  To use Streams Studio:

1.  Connect to the Streams Docker desktop using Remote Desktop or VNC.
1.  On the desktop, double click on the Streams Studio icon.

## Remote Streams Studio

Remote Streams Studio, connecting to docker is supported on Windows.  It is not supported on OSx.

When connecting Streams Studio to the docker container:

* Connect to localhost or 127.0.0.1
* Make sure you use 4022 as the SSH port
* When making a connection, check the "Establish SSH Tunnel' check box
* Keep everything else as defaults.

## Attaching to a Running Docker Container

In case you have closed the powershell, you may need to attach to the running docker container again.  Please note that attaching to the container will cause the domain and instances to be restarted.

Follow these commands to attach to a container:

For Windows:

1.  `docker-machine env streams4100 --shell powershell |Invoke-Expression`
2.  `docker attach streams4100`

For Mac OSx:

1.  `eval "$(/usr/local/bin/docker-machine env streams4100)"`
2.  `docker attach streams4100`

## Restarting Docker Image

To restart the docker image, follow these commands:

For Windows:

1.  `docker-machine stop streams4100`
1.  `docker-machine start streams4100`
1.  `docker-machine env streams4100 --shell powershell |Invoke-Expression`
1.  `docker restart streams4100`

For Mac OSx:

1.  `docker-machine stop streams4100`
1.  `docker-machine start streams4100`
1.  `eval "$(/usr/local/bin/docker-machine env streams4100)"`
1.  `docker restart streams4100`

Note:  After the restart, you may need to wait for about 30 seconds before attempting to VNC into the docker image.  You may also need to manually force the Streams domain and instances to be restarted to assure all services come up properly.

To restart the domain:

1.  open the streamsadmin terminal
1.  `streamstool stopdomain -d streamsdomain --force`
1.  `streamstool startdomain -d streamsdomain`

# Useful Docker Commands
~~~~~~
  docker images    (list local images)
  docker ps        (list running containers)
  docker ps -a     (list all containers)
  docker rm <container name/ID>  (delete a container)
  docker rmi <image name/ID>     (delete an image)
  docker restart <container name/ID>  (restart an existing stopped container - same ports and volumes will be used as when the container was created.)
  docker attach <container name/ID> (attach to a running container)
~~~~~~

# Useful Docker Machine Commands

~~~~~~
  docker-machine ls    (list machines and state)
  docker-machine start <VM>  (start a VM)
  docker-machine stop <VM>   (stop VM)
  docker-machine rm <VM>     (delete the VM, use '--force' at end of command to force delete)

  To set environment variables for docker to access for VM 'streams4100':
  On Window:  docker-machine env streams4100 --shell powershell |Invoke-Expression
  On Mac OSx: eval "$(/usr/local/bin/docker-machine env streams4100)"

~~~~~~

## What to do next

Explore the Streams QSE VMWare image following the [Quick Start Edition VM Getting Started Guide](/streamsx.documentation/docs/4.1/qse-getting-started/)
