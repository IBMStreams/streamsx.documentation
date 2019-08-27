---
layout: docs
title:  Import your code into Atom
description:  Steps to configure Atom for SPL development
navlevel: 2
tag: atom
prev:
  file: atom-guide-1a-configure
  title: Configure Atom
next:
  file: atom-guide-3-editor
  title: Reviewing SPL code in Atom
---

After you [configure Atom](/streamsx.documentation/docs/spl/atom/atom-guide-1a-configure), you can start working with some code.

To get the most out of this guide, it is a good idea to import the sample application.

You can also go to the section that best describes your use case:
* Import an existing project (including Streams Studio projects)
*	Import a project from GitHub
*	Creating a project in Atom

Import the sample project for this guide
----------------------------------------
To follow along with this guide, download the [BusAlerts application ](https://streams-github-samples.mybluemix.net/?get=QuickStart%2FBusAlerts).
* Extract the files into a folder
*	Import it into Atom: click **File > Add Project Folder**. Browse to the project folder and click **Open** (Linux/Mac) or **Select folder** (Windows&reg;).


The following sections describe other ways to start development by importing your own code from a folder or GitHub, or creating a new project.


Import an existing project (Including Streams Studio Projects)
--------------------------

To import any SPL project, from Atom, click **File** > **Add Project Folder**. Browse to the project folder and click **Open (Linux)** or **Select folder** (Windows&reg;).

Import a project from GitHub
----------------------------

If you have existing SPL code on GitHub, you can clone the repository from within Atom.

From the Command Palette, search for and select the **GitHub Clone** option.

    ![git clone](/streamsx.documentation/images/atom/jpg/githubclone.jpg)

Enter the repository URL into the URL field and click **Clone**.

 ![git clone uri](/streamsx.documentation/images/atom/jpg/github-clone-uri.jpg)

The project is added to the project pane.

Whether you imported an existing application or created one from scratch, it is a good idea to explore the Atom editor to learn about
useful editing features.
- [Import a project from GitHub](/streamsx.documentation/docs/spl/atom/atom-guide-2-import-code/#import-a-project-from-github)

- [Creating a project in Atom](/streamsx.documentation/docs/spl/atom/atom-guide-2-import-code/#creating-a-new-project)
