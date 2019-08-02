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

After you configure Atom, you can start working with some code. In order to get the most out of this guide, you can follow the instructions to import the sample application in the **Import an Existing Project** section. The archive file for the sample BusAlerts application can be downloaded by following this \[LINK\]

Import an Existing Project (Including Streams Studio Projects)
--------------------------

If you have an existing Streams project in an archive, you can use Atom to work on the project by doing the following:

1. Extract the contents of the archive into a folder of your choice.
2. From Atom go to **File > Open Folder** and navigate to the folder which contains your project, then press open.

Import a project from GitHub
----------------------------
If you have an existing SPL or Streams Studio project on GitHub, you can import the project into Atom by doing the following steps:
1. Use the keyboard shortcut **CMD + Shift + P ** on Mac or **Ctrl + Shift + P** on Windows&reg; to open the command palette in Atom.
2. In the command palette search for and select the **GitHub Clone** option.
    ![git clone](/streamsx.documentation/images/atom/jpg/githubclone.jpg)
3. Paste the repository URL into the URL field and click **Clone**.

 ![git clone uri](/streamsx.documentation/images/atom/jpg/github-clone-uri.jpg)

The project should be automatically added to the project pane.


Whether you imported an existing application or are creating one from
scratch, it is a good idea to explore the Atom editor to learn about
useful editing features.
- [Import a project from GitHub](/streamsx.documentation/docs/spl/atom/atom-guide-2-import-code/#import-a-project-from-github)

- [Creating a project in Atom](/streamsx.documentation/docs/spl/atom/atom-guide-2-import-code/#creating-a-new-project)
