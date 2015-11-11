---
layout: docs
title:  Installing Streams Quick Start Edition Docker 
weight: 20
---

# Installing Streams Quick Start Edition Docker Image

<div class="alert alert-danger" role="alert"><b>IMPORTANT:</b> If you already have boot2docker installed, remove all components (docker, Git, and Oracle VirtualBox) before installing 'Docker Toolbox'</div>

<div class="alert alert-danger" role="alert"><b>IMPORTANT:</b> If you have 'Docker Toolbox' already installed remove older version of Streams4Docker images and containers, and if there already exists a VirtualBox VM names 'streams4100', delete that as well. </div>

## Windows

1.  Install Dockertoolbox
    * See Docker Toolbox page for instructions:  https://www.docker.com/toolbox
1.  Install using all defaults for a 'Full Installation'
1.  Download the Streams4Docker.zip archive 
1.  Extract the Streams4Docker.zip archive to preferred location
1.  Open Windows PowerShell
    * Application Menu-> All Programs -> Accessories -> Windows Powershell -> Windows PowerShell
    * `cd <Directory where Streams4Docker downloaded>/Docker`
    * `powershell -ExecutionPolicy ByPass -File Streams-build.ps1`
    
    
    Note: default build is 4096 MB memORY; 4 cpus; 50000 Bytes disk. 
    
    To change defaults, for example to 8192 MB mem; 2 cups; 60000 Bytes of disk run 
           "powershell -ExecutionPolicy ByPass -File Streams-build.ps1 8192 2 60000"

<div class="alert alert-warning" role="alert">
Building and running of the Docker container will take about 20 minutes. 
You may be prompted for Administration Authentication several times. 
When completed the Powershell terminal will be sitting at the root prompt inside the Docker container.
</div>

## Mac OSx

1.  Install Dockertoolbox
    * See Docker Toolbox page for instructions:  https://www.docker.com/toolbox
1.  Install using all defaults for a 'Full Installation'
1.  Download the Streams4Docker.zip.  
1.  Copy the zip file to your home directory or any directory under your home directory:  `cp Streams4Docker.zip /home/<userid>`
1.  Extract the zip file:  `unzip Streams4Docker.zip`
1.  Open a terminal and change to the Docker directory:  `cd Streams4Docker/Docker`
1.  Run the script to build the docker image:  `./Streams-OSX-build.sh`

    Note: default build is 4096 MB mem; 4 cpus; 50000 Bytes disk. 
          
    To change defaults, for example to 8192 MB mem; 2 cups; 60000 Bytes of disk run 
    
    `"./Streams-OSX-build.sh 8192 2 60000"`

<div class="alert alert-warning" role="alert">
Build and Run of Docker Container will take about 20 minutes. You may be prompted for Administration Authentication several times. When completed the Powershell terminal will be sitting at the root prompt inside the Docker container.
</div>

## Accessing the IBM Streams Docker container

The Streams Docker container is set up with the following user id and password:

* User ID:  streamsadmin
* Password:  passw0rd
* Root:  passw0rd

After the containers finish the stratup process, you should be able to access the container via:

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

# Useful Docker Commands
~~~~~~
  docker images    (list local images)
  docker ps        (list running containers)
  docker ps -a     (list all containers)
  docker rm <container name/ID>  (delete a container)
  docker rmi <image name/ID>     (delte an image)
  docker restart <container name/ID>  (restart an existing stopped container - same ports and volumes will be used as when the container was created.)
~~~~~~

# Useful Docker Machine Commands

~~~~~~
  docker-machine ls    (list machines and state)
  docker-machine start <VM>  (start a VM
  docker-machine stop <VM>   (stop VM)
  docker-machine rm <VM>     (delete the VM, use '--force' at end of command to force delete)
  docker-machine env streams4100 --shell powershell |Invoke-Expression    (set the enviroment vars for docker to access for VM 'streams4100')
~~~~~~

## What to do next

Explore the Streams QSE VMWare image following the [Quick Start Edition VM Getting Started Guide](/streamsx.documentation/docs/4.1/qse-getting-started/)
